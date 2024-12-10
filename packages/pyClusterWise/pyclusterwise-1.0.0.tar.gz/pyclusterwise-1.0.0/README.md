# pyClusterWise

**pyClusterWise** is a Python package designed for dynamic clustering analysis with multiple methods, evaluation metrics, and uncertainty quantification. It allows users to analyze datasets containing geospatial and numerical data efficiently, with support for common clustering techniques such as K-Means, K-Medoids, DBSCAN, and Hierarchical Clustering.

---

## Key Features

- **Flexible Input**: Works with any dataset containing geospatial coordinates and numerical columns, regardless of column names.
- **Multiple Clustering Methods**:
  - K-Means
  - K-Medoids
  - DBSCAN
  - Hierarchical Clustering
- **Evaluation Metrics**:
  - Silhouette Score
  - Davies-Bouldin Score
  - Calinski-Harabasz Index
  - Elbow Method (Inertia)
  - Bayesian Information Criterion (BIC)
- **Uncertainty Quantification**:
  - Compares clustering methods based on their uncertainties.
  - Evaluates reliability of clustering evaluation metrics.
- **Interactive Element Selection**: Users can select specific elements (numerical columns) for analysis.

---

## Installation

To install the package, run the following command after uploading it to PyPI:

```bash
pip install pyClusterWise
