"""
_processing/ai.py
========================

.. module:: ai
   :platform: Unix
   :synopsis: Provides methods for `smart` data analysis.

Module Overview
---------------

This module includes functions for provessing data cubes.

Analyzing hyperspectral data often involves dimensionality reduction, clustering, and classification techniques. Similar to K-means, other algorithms can be used depending on the specific goals, such as visualizing data, segmenting regions, or identifying patterns. Here's a list of algorithms categorized by purpose:

---

### **Clustering Algorithms**
- **Hierarchical Clustering**:
  Groups pixels based on their spectral similarity without a predefined number of clusters. It can provide a dendrogram for visualizing relationships.
  - Example: `scipy.cluster.hierarchy`

- **Gaussian Mixture Models (GMM)**:
  Fits data to a mixture of Gaussian distributions, allowing for soft clustering (probability of belonging to each cluster).
  - Example: `sklearn.mixture.GaussianMixture`

- **Spectral Clustering**:
  Uses the graph Laplacian and eigenvalues to identify clusters in non-linear, high-dimensional spaces. It works well for hyperspectral data with complex structures.
  - Example: `sklearn.cluster.SpectralClustering`

- **DBSCAN (Density-Based Spatial Clustering)**:
  Groups pixels into clusters based on the density of data points, identifying noise and outliers effectively.
  - Example: `sklearn.cluster.DBSCAN`

---

### **Dimensionality Reduction**
- **Principal Component Analysis (PCA)**:
  Reduces dimensionality while preserving maximum variance, often used for visualizing hyperspectral data or preprocessing for clustering.
  - Example: `sklearn.decomposition.PCA`

- **t-SNE (t-Distributed Stochastic Neighbor Embedding)**:
  Non-linear dimensionality reduction for visualizing high-dimensional data in 2D or 3D. Useful for understanding clustering in spectral data.
  - Example: `sklearn.manifold.TSNE`

- **UMAP (Uniform Manifold Approximation and Projection)**:
  Similar to t-SNE but faster and better at preserving global structures in the data.
  - Example: `umap-learn` package

- **Independent Component Analysis (ICA)**:
  Extracts statistically independent components, often used to separate mixed sources in hyperspectral data.
  - Example: `sklearn.decomposition.FastICA`

---

### **Segmentation Algorithms**
- **Watershed Segmentation**:
  A region-growing algorithm for segmenting hyperspectral images based on local intensity gradients.
  - Example: `skimage.segmentation.watershed`

- **Superpixel Algorithms (e.g., SLIC)**:
  Groups nearby pixels into superpixels for efficient analysis and segmentation.
  - Example: `skimage.segmentation.slic`

---

### **Anomaly Detection**
- **Isolation Forest**:
  Identifies anomalous points by isolating them in the data distribution. Useful for finding rare spectral patterns.
  - Example: `sklearn.ensemble.IsolationForest`

- **RX Detector (Reed-Xiaoli)**:
  Specifically designed for hyperspectral anomaly detection by comparing each pixel's spectrum to its neighborhood.

---

### **Classification Techniques**
- **Support Vector Machines (SVM)**:
  A supervised learning method to classify pixels based on their spectral signatures.
  - Example: `sklearn.svm.SVC`

- **Random Forests**:
  A robust, ensemble-based classification algorithm for multi-class spectral data.
  - Example: `sklearn.ensemble.RandomForestClassifier`

- **Neural Networks**:
  Deep learning models, such as Convolutional Neural Networks (CNNs), are often used for hyperspectral image classification and feature extraction.
  - Frameworks: TensorFlow, PyTorch

---

### **Matrix Factorization**
- **Non-negative Matrix Factorization (NMF)**:
  Decomposes the data into additive components, making it interpretable for hyperspectral unmixing.
  - Example: `sklearn.decomposition.NMF`

- **Vertex Component Analysis (VCA)**:
  Specialized for hyperspectral data to extract spectral endmembers and their abundances.

---

### **Advanced Techniques**
- **Self-Organizing Maps (SOMs)**:
  A type of neural network for clustering and visualization of high-dimensional data.
  - Library: `MiniSom`

- **Affinity Propagation**:
  Identifies representative clusters based on similarity measures.
  - Example: `sklearn.cluster.AffinityPropagation`

- **Graph-based Methods**:
  Analyzes the data as a graph structure, such as Graph Neural Networks (GNNs) for classification or segmentation.

---

Each of these techniques has specific strengths and limitations. The choice of algorithm depends on:
1. The size and complexity of your data.
2. Your goal (clustering, classification, anomaly detection, etc.).
3. The computational resources available.

Would you like help implementing any of these methods?

"""

from sklearn.cluster import KMeans
# from .._core import DataCube
from wizard import DataCube
import wizard

from skimage import filters, segmentation, morphology, color
from skimage.feature import peak_local_max
from scipy import ndimage as ndi

def kmeans(dc: DataCube, n_clusters, n_init, *args, **kwargs):
    """
    Perform K-means clustering on a 3D data cube.

    This function reshapes a 3D data cube into a 2D array for clustering,
    applies the K-means algorithm, and then reshapes the clustered labels
    back into the original 2D spatial dimensions.

    Parameters
    ----------
    dc : DataCube
        The input data cube to be clustered. It is expected to have a
        `.cube` attribute representing the 3D array and a `.shape` attribute
        providing the dimensions (bands, height, width).
    n_clusters : int
        The number of clusters to form as well as the number of centroids
        to generate.
    n_init : int
        Number of time the K-means algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of inertia.
    *args : tuple
        Additional positional arguments passed to the KMeans constructor.
    **kwargs : dict
        Additional keyword arguments passed to the KMeans constructor.

    Returns
    -------
    ndarray
        A 2D array of shape `(height, width)` containing the cluster labels
        for each pixel.

    Notes
    -----
    - The input data cube is flattened across the spatial dimensions, and
      clustering is performed on this 2D representation.
    - After clustering, the flat label array is reshaped to match the
      spatial dimensions of the input cube.
    """
    flat_cube = dc.cube.reshape(dc.shape[0], -1).T

    kmeans = KMeans(init="k-means++", n_clusters=n_clusters, n_init=n_init)
    y_flat = kmeans.fit_predict(flat_cube)

    y = y_flat.reshape(dc.shape[1], dc.shape[2])
    return y

def watershed_segmentation(dc: DataCube)

if __name__ == '__main__':
    import numpy as np
    from matplotlib import pyplot as plt
    dc = wizard.read('/Users/flx/Documents/data/Tom_MA/Measurement_09_03_2024')
    print(dc.shape)

    plt.imshow(dc[0])
    plt.show()

    y = kmeans(dc, n_clusters=4, n_init=25)
    plt.imshow(y)
    plt.show()