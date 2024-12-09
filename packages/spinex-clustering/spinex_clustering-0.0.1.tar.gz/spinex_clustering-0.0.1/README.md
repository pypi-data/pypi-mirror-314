# File: README.md
# SPINEX Clustering

SPINEX (Similarity-based Predictions and Explainable Neighbors Exploration) Clustering is an advanced clustering algorithm that combines multiple similarity measures with multi-level analysis capabilities.

## Features

- Multiple similarity methods (correlation, spearman, kernel, cosine)
- Multi-level clustering capabilities
- Parallel processing support
- Explainable results with similarity and neighbor analysis
- Automatic threshold determination
- PCA dimensionality reduction option
- Comprehensive evaluation metrics

## Installation

```bash
pip install spinex-clustering
```

## Quick Start

```python
from spinex_clustering import SPINEX_Clustering
import numpy as np

# Create sample data
X = np.random.randn(100, 10)

# Initialize and fit the clustering model
model = SPINEX_Clustering(
    threshold='auto',
    use_multi_level=True,
    enable_similarity_analysis=True
)

# Get cluster labels
labels = model.fit_predict(X)

# Print first few labels to verify it worked
print("First few cluster labels:", labels[:10])
```

## Documentation

For detailed documentation and examples, visit [documentation link].

## License

This project is licensed under the MIT License - see the LICENSE file for details.
