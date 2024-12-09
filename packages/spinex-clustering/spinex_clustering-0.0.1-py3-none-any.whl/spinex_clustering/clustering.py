import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics.pairwise import rbf_kernel, cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.metrics import homogeneity_score, completeness_score, v_measure_score
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
from sklearn.decomposition import PCA
import time
from sklearn.manifold import TSNE
from umap import UMAP
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from numba import njit
import hashlib

@njit
def multi_level_clustering(sim_matrix, initial_threshold, levels=3):
    n = sim_matrix.shape[0]
    clusters = np.arange(n)
    prev_num_clusters = n
    thresholds = np.full(levels, initial_threshold)
    prev_variance = np.var(sim_matrix)
    for level in range(levels):
        subclusters = merge_clusters_optimized(sim_matrix, thresholds[level])
        unique_clusters = np.unique(subclusters)
        num_clusters = len(unique_clusters)
        inverse = np.zeros(n, dtype=np.int64)
        for i, c in enumerate(unique_clusters):
            inverse[subclusters == c] = i
        if num_clusters == 1 or num_clusters == prev_num_clusters:
            break  # Stop if no more merging is possible
        new_sim_matrix = np.zeros((num_clusters, num_clusters))
        # Efficiently update new similarity matrix
        for i in range(num_clusters):
            for j in range(i+1, num_clusters):
                mask_i = (inverse == i)
                mask_j = (inverse == j)
                sim_values = sim_matrix[mask_i][:, mask_j]
                sim_value = np.mean(sim_values) if sim_values.size > 0 else 0
                new_sim_matrix[i, j] = new_sim_matrix[j, i] = sim_value
        # Update thresholds
        current_variance = np.var(new_sim_matrix)
        variance_change = current_variance / prev_variance if prev_variance != 0 else 1
        cluster_change = num_clusters / prev_num_clusters
        thresholds[level+1:] *= np.clip(1 + 0.1 * (1 - cluster_change), 0.9, 1.1)
        thresholds[level+1:] *= 0.95 if variance_change < 1 else 1.05
        # Prepare for the next iteration
        prev_variance = current_variance
        prev_num_clusters = num_clusters
        sim_matrix = new_sim_matrix
        clusters = unique_clusters[inverse]
    return clusters

@njit
def should_merge_optimized(cluster1, cluster2, sim_matrix, threshold):
    if cluster1.size == 0 or cluster2.size == 0:
        return False
    total_sim = 0.0
    count = 0
    for i in cluster1:
        for j in cluster2:
            total_sim += sim_matrix[i, j]
            count += 1
    return (total_sim / count) > threshold if count > 0 else False

@njit
def merge_clusters_optimized(sim_matrix, threshold):
    n = sim_matrix.shape[0]
    clusters = np.arange(n)
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if i != clusters[i]:
                continue
            for j in range(i + 1, n):
                if j != clusters[j]:
                    continue
                cluster_i = np.where(clusters == i)[0]
                cluster_j = np.where(clusters == j)[0]
                if should_merge_optimized(cluster_i, cluster_j, sim_matrix, threshold):
                    clusters[clusters == j] = i
                    changed = True
                    break
            if changed:
                break
    return clusters

@njit
def dynamic_threshold(sim_matrix, initial_threshold, decay_rate=0.95, max_iterations=100):
    threshold = initial_threshold
    n = sim_matrix.shape[0]
    for _ in range(max_iterations):
        clusters = merge_clusters_optimized(sim_matrix, n, threshold)
        if len(np.unique(clusters)) == 1:
            threshold /= decay_rate
        else:
            break
    return threshold

def composite_score(metrics, evaluation_tier, ground_truth):
    if evaluation_tier == 1:
        return metrics['Silhouette'] * 0.33 + metrics['Calinski-Harabasz'] * 0.33 - metrics['Davies-Bouldin'] * 0.34
    elif evaluation_tier == 2 and ground_truth is not None:
        return metrics['Homogeneity'] * 0.33 + metrics['Completeness'] * 0.33 + metrics['V-Measure'] * 0.34
    elif evaluation_tier == 3 and ground_truth is not None:
        return (metrics['Silhouette'] * 0.165 + metrics['Calinski-Harabasz'] * 0.165 - metrics['Davies-Bouldin'] * 0.165 +
                metrics['Homogeneity'] * 0.165 + metrics['Completeness'] * 0.165 + metrics['V-Measure'] * 0.175)
    return -np.inf

class SPINEX_Clustering:
    def __init__(self, threshold='auto', n_clusters=None, use_pca=False, n_components=None,
                 enable_similarity_analysis=False, enable_neighbor_analysis=False,
                 similarity_methods=None, evaluation_tier=1, ground_truth=None,
                 use_approximation=False, approximation_method='random_sampling', sample_size=0.5,
                 use_parallel=False, parallel_threshold=5000, max_workers=None,use_multi_level=False, multi_level_params=None, max_features=100):
        self.threshold = threshold
        self.similarity_methods = similarity_methods or ['correlation', 'spearman', 'kernel', 'cosine']
        self.use_pca = use_pca
        self.n_components = n_components
        self.enable_similarity_analysis = enable_similarity_analysis
        self.enable_neighbor_analysis = enable_neighbor_analysis
        self.evaluation_tier = evaluation_tier
        self.use_approximation = use_approximation
        self.approximation_method = approximation_method
        self.sample_size = sample_size
        self.decision_log = []
        self.explainability_results = {}
        self.ground_truth = ground_truth.tolist() if isinstance(ground_truth, np.ndarray) else ground_truth
        self.use_parallel = use_parallel
        self.parallel_threshold = parallel_threshold
        self.max_workers = mp.cpu_count() if use_parallel else 1
        self.n_clusters = n_clusters
        self.max_workers = max_workers if max_workers is not None else (mp.cpu_count() if use_parallel else 1)
        self.similarity_cache = {}  # Cache for storing similarity matrices
        self.use_multi_level = use_multi_level
        self.multi_level_params = multi_level_params or {'levels': 3, 'initial_threshold': 0.5}
        self.max_features = max_features

    def hash_matrix(self, matrix):
        """Create a hash for a matrix."""
        m_hash = hashlib.sha256()
        m_hash.update(matrix.data.tobytes())
        return m_hash.hexdigest()

    def get_similarity_matrix(self, X, method):
        """Calculate or retrieve a cached similarity matrix based on the method."""
        if X.shape[1] < 2 and (method == 'correlation' or method == 'spearman'):
            similarity_matrix = np.ones((X.shape[0], X.shape[0]))  # Perfect similarity
        else:
            matrix_hash = self.hash_matrix(X)
            cache_key = (matrix_hash, method)
            if cache_key in self.similarity_cache:
                similarity_matrix = self.similarity_cache[cache_key]
                self.log_decision(f"Retrieved {method} similarity matrix from cache.")
            else:
                if method == 'correlation':
                    similarity_matrix = self.calculate_correlation_matrix(X)
                elif method == 'spearman':
                    similarity_matrix = self.calculate_spearman_matrix(X)
                elif method == 'kernel':
                    similarity_matrix = self.calculate_kernel_matrix(X)
                elif method == 'cosine':
                    similarity_matrix = self.calculate_cosine_matrix(X)
                else:
                    raise ValueError(f"Invalid similarity method: {method}")

                self.similarity_cache[cache_key] = similarity_matrix
                self.log_decision(f"Computed and cached {method} similarity matrix.")
        # Ensure the similarity matrix is 2D
        if similarity_matrix.ndim == 0:
            similarity_matrix = np.array([[similarity_matrix]])
        elif similarity_matrix.ndim == 1:
            similarity_matrix = similarity_matrix.reshape(1, -1)
        return similarity_matrix

    def log_decision(self, message):
        self.decision_log.append(message)

    @staticmethod
    def calculate_correlation_matrix(X):
        if X.shape[1] < 2:
            return np.ones((X.shape[0], X.shape[0]))
        return np.corrcoef(X)

    @staticmethod
    def calculate_spearman_matrix(X):
        if X.shape[1] < 2:
            return np.ones((X.shape[0], X.shape[0]))
        return spearmanr(X)[0]

    @staticmethod
    def calculate_kernel_matrix(X, gamma=1.0):
        return rbf_kernel(X, gamma=gamma)

    @staticmethod
    def calculate_cosine_matrix(X):
        return cosine_similarity(X)

    def apply_approximation(self, X):
        if self.use_approximation:
            if self.approximation_method == 'random_sampling':
                sample_indices = np.random.choice(X.shape[0], int(X.shape[0] * self.sample_size), replace=False)
                X = X[sample_indices]
                self.log_decision(f"Data reduced to {X.shape[0]} samples using random sampling.")
            elif self.approximation_method == 'pca':
                pca = PCA(n_components=self.n_components if self.n_components is not None else 0.95)
                X = pca.fit_transform(X)
                self.log_decision(f"Data reduced to {pca.n_components_} dimensions using PCA.")
            elif self.approximation_method == 'tsne':
                tsne = TSNE(n_components=self.n_components if self.n_components is not None else 2)
                X = tsne.fit_transform(X)
                self.log_decision("Data projected to lower dimensions using t-SNE.")
            elif self.approximation_method == 'umap':
                umap = UMAP(n_components=self.n_components if self.n_components is not None else 2)
                X = umap.fit_transform(X)
                self.log_decision("Data projected to lower dimensions using UMAP.")
        return X

    def set_threshold(self, sim_matrix):
        if self.threshold == 'auto':
            median_val = np.median(sim_matrix)
            above_median = sim_matrix[sim_matrix > median_val]
            if len(above_median) > 0:
                std_dev = np.std(above_median)
                threshold_value = median_val + std_dev
            else:
                threshold_value = np.max(sim_matrix)
            self.log_decision(f"Adaptive threshold set using density-based approach: {threshold_value}")
        elif isinstance(self.threshold, str) and self.threshold.endswith('%'):
            percentile = float(self.threshold[:-1])
            threshold_value = np.percentile(sim_matrix.flatten(), percentile)
            self.log_decision(f"Threshold set using percentile: {threshold_value}")
        elif isinstance(self.threshold, (int, float)):
            threshold_value = self.threshold
            self.log_decision(f"Threshold set using fixed value: {threshold_value}")
        else:
            raise ValueError("Invalid threshold specified")
        return threshold_value

    def all_similarity_clustering(self, X):
        if self.use_parallel and X.shape[0] >= self.parallel_threshold:
            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {method: executor.submit(self.improved_similarity_clustering, X, method)
                          for method in self.similarity_methods}
                results = {method: future.result() for method, future in futures.items()}
        else:
            results = {method: self.improved_similarity_clustering(X, method)
                      for method in self.similarity_methods}

        return {method: {'n_clusters': len(np.unique(labels)), 'labels': labels}
                for method, (labels, _) in results.items()}

    def calculate_metrics(self, X, labels, method):
        # Create a hash for the data and labels to serve as a cache key
        data_hash = self.hash_matrix(X)
        labels_hash = self.hash_matrix(labels)
        cache_key = (data_hash, labels_hash, method)
        # Check if metrics are already calculated and stored in cache
        if cache_key in self.similarity_cache:
            self.log_decision(f"Metrics retrieved from cache for method: {method}")
            return self.similarity_cache[cache_key]
        # Compute metrics if not in cache
        n_clusters = len(np.unique(labels))
        metrics = {
            'n_clusters': n_clusters,
            'labels': labels,
            'Silhouette': np.nan,
            'Calinski-Harabasz': np.nan,
            'Davies-Bouldin': np.nan,
            'Homogeneity': np.nan,
            'Completeness': np.nan,
            'V-Measure': np.nan
        }
        if 1 < n_clusters < len(X):
            try:
                if self.evaluation_tier in [1, 3]:
                    metrics['Silhouette'] = silhouette_score(X, labels)
                    metrics['Calinski-Harabasz'] = calinski_harabasz_score(X, labels)
                    metrics['Davies-Bouldin'] = davies_bouldin_score(X, labels)
                if self.evaluation_tier in [2, 3] and self.ground_truth is not None:
                    metrics['Homogeneity'] = homogeneity_score(self.ground_truth, labels)
                    metrics['Completeness'] = completeness_score(self.ground_truth, labels)
                    metrics['V-Measure'] = v_measure_score(self.ground_truth, labels)
            except Exception as e:
                self.log_decision(f"Error calculating metrics for {method}: {str(e)}")
        # Cache the calculated metrics
        self.similarity_cache[cache_key] = metrics
        self.log_decision(f"Metrics computed and cached for method: {method}")
        return metrics

    def find_best_clustering(self, X):
        results = self.all_similarity_clustering(X)
        if len(results) == 1:
            best_method = list(results.keys())[0]
            return results[best_method]['labels'], best_method
        if self.use_parallel and X.shape[0] >= self.parallel_threshold:
            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {method: executor.submit(self.calculate_metrics, X, results[method]['labels'], method)
                          for method in results}
                detailed_results = {method: future.result() for method, future in futures.items()}
        else:
            detailed_results = {method: self.calculate_metrics(X, results[method]['labels'], method)
                                for method in results}
        scored_results = {method: composite_score(metrics, self.evaluation_tier, self.ground_truth)
                          for method, metrics in detailed_results.items()}
        best_method = max(scored_results, key=scored_results.get)
        return detailed_results[best_method]['labels'], best_method

    def apply_pca(self, X):
        if self.use_pca:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            matrix_hash = self.hash_matrix(X_scaled)  # Hash the scaled data
            cache_key = ('PCA', matrix_hash)
            if cache_key in self.similarity_cache:
                pca_result = self.similarity_cache[cache_key]
                self.log_decision("Retrieved PCA results from cache.")
            else:
                pca = PCA(n_components=self.n_components if self.n_components is not None else 0.95)
                pca_result = pca.fit_transform(X_scaled)
                self.similarity_cache[cache_key] = pca_result  # Cache the PCA result
                self.log_decision(f"Computed and cached PCA results. Reduced dimensions to {pca.n_components_}.")
            return pca_result
        return X

    def improved_similarity_clustering(self, X, similarity_method='correlation'):
        if self.use_pca:
            X = self.apply_pca(X)
        self.log_decision(f"Shape of X before similarity matrix calculation: {X.shape}")
        if similarity_method not in self.similarity_methods:
            raise ValueError(f"Invalid similarity method. Choose from {', '.join(self.similarity_methods)}.")
        sim_matrix = self.get_similarity_matrix(X, similarity_method)
        self.log_decision(f"Similarity matrix shape: {sim_matrix.shape}")
        threshold = self.set_threshold(sim_matrix)
        labels = self.cluster_from_similarity(sim_matrix, X.shape[0], threshold)
        return labels, similarity_method

    def cluster_from_similarity(self, sim_matrix, n, threshold):
        if np.isscalar(sim_matrix) or sim_matrix.size == 1:
            return np.zeros(n, dtype=int) 
        if self.use_multi_level:
            self.log_decision("Using multi-level clustering")
            try:
                clusters = multi_level_clustering(sim_matrix,
                                                  self.multi_level_params['initial_threshold'],
                                                  levels=self.multi_level_params['levels'])
                self.log_decision(f"Multi-level clustering completed with {len(np.unique(clusters))} clusters")
            except Exception as e:
                self.log_decision(f"Error in multi-level clustering: {str(e)}. Falling back to default clustering.")
                clusters = merge_clusters_optimized(sim_matrix, float(threshold) if threshold is not None else 0.5)
            return clusters
        if self.n_clusters is not None and self.n_clusters < n and sim_matrix.size > 1:
            # Use hierarchical clustering when n_clusters is set
            distance_matrix = 1 - np.clip(sim_matrix, -1, 1)
            np.fill_diagonal(distance_matrix, 0)
            distance_matrix = (distance_matrix + distance_matrix.T) / 2
            distance_matrix = np.maximum(distance_matrix, 0)
            try:
                linkage_matrix = linkage(squareform(distance_matrix), method='complete')
                cluster_labels = fcluster(linkage_matrix, t=self.n_clusters, criterion='maxclust')
                return cluster_labels - 1
            except ValueError as e:
                print(f"Error in hierarchical clustering: {e}")
                return np.zeros(n)
        else:
            # Use optimized merging method
            clusters = merge_clusters_optimized(sim_matrix, float(threshold) if threshold is not None else 0.5)
            return clusters

    def should_merge(self, cluster1, cluster2, sim_matrix, threshold):
        return should_merge_optimized(cluster1, cluster2, sim_matrix, threshold)

    def get_decision_log(self):
        return self.decision_log

    def similarity_contribution_analysis(self, X, observation_index):
        n_features = X.shape[1]
        sim_matrix = self.calculate_correlation_matrix(X)
        observation_similarities = sim_matrix[observation_index]
        obs_value = X[observation_index]
        differences = np.abs(X - obs_value)
        contributions = {f'Feature_{i}': differences[:, i] for i in range(n_features)}
        return observation_similarities, contributions

    def nearest_neighbor_analysis(self, X, observation_index, k=5):
        sim_matrix = self.get_similarity_matrix(X, self.similarity_methods[0])
        observation_similarities = sim_matrix[observation_index]
        nearest_neighbors = np.argsort(observation_similarities)[::-1][1:k+1]
        obs_value = X[observation_index]
        neighbor_values = X[nearest_neighbors]
        contributions = np.abs(neighbor_values - obs_value)
        neighbor_contributions = {
            int(neighbor_index): {f'Feature_{i}': contributions[j, i] for i in range(X.shape[1])}
            for j, neighbor_index in enumerate(nearest_neighbors)
        }
        return nearest_neighbors.tolist(), neighbor_contributions

    def fit_predict(self, X):
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        elif X.ndim > 2:
            raise ValueError("Input array X should be 1D or 2D.")
        # If there are too many features, use PCA to reduce dimensionality
        if X.shape[1] > self.max_features:
            self.log_decision(f"Reducing features from {X.shape[1]} to {self.max_features} using PCA")
            pca = PCA(n_components=self.max_features)
            X = pca.fit_transform(X)
        labels, best_method = self.find_best_clustering(X)
        if self.use_multi_level:
            self.log_decision("Applying multi-level clustering to best similarity matrix")
            sim_matrix = self.get_similarity_matrix(X, best_method)
            labels = self.cluster_from_similarity(sim_matrix, X.shape[0], None)
        self.log_decision(f"Best clustering method: {best_method}")
        if self.enable_similarity_analysis or self.enable_neighbor_analysis:
            if self.use_parallel and X.shape[0] >= self.parallel_threshold:
                with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = []
                    for i in range(X.shape[0]):
                        if self.enable_similarity_analysis:
                            futures.append(executor.submit(self.similarity_contribution_analysis, X, i))
                        if self.enable_neighbor_analysis:
                            futures.append(executor.submit(self.nearest_neighbor_analysis, X, i, k=5))
                    results = [future.result() for future in futures]
                    results_index = 0
                    for i in range(X.shape[0]):
                        self.explainability_results[i] = {}
                        if self.enable_similarity_analysis:
                            similarities, contributions = results[results_index]
                            self.explainability_results[i]['similarity_analysis'] = {
                                'similarities': similarities.tolist(),
                                'contributions': {k: v.tolist() for k, v in contributions.items()}
                            }
                            results_index += 1
                        if self.enable_neighbor_analysis:
                            nearest_neighbors, neighbor_contributions = results[results_index]
                            self.explainability_results[i]['neighbor_analysis'] = {
                                'nearest_neighbors': nearest_neighbors,
                                'neighbor_contributions': neighbor_contributions
                            }
                            results_index += 1
            else:
                for i in range(X.shape[0]):
                    self.explainability_results[i] = {}
                    if self.enable_similarity_analysis:
                        similarities, contributions = self.similarity_contribution_analysis(X, i)
                        self.explainability_results[i]['similarity_analysis'] = {
                            'similarities': similarities.tolist(),
                            'contributions': {k: v.tolist() for k, v in contributions.items()}
                        }
                    if self.enable_neighbor_analysis:
                        nearest_neighbors, neighbor_contributions = self.nearest_neighbor_analysis(X, i, k=5)
                        self.explainability_results[i]['neighbor_analysis'] = {
                            'nearest_neighbors': nearest_neighbors,
                            'neighbor_contributions': neighbor_contributions
                        }
        return labels

    def get_explainability_results(self):
        return self.explainability_results