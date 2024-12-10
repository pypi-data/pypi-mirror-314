import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.mixture import GaussianMixture

# Define a function to analyze clustering with dynamic data handling
def analyze_clustering(data_path, x_column=None, y_column=None, element_columns=None):
    # Load the dataset
    dataset = pd.read_csv(data_path)

    # Infer coordinate columns if not provided
    if not x_column or not y_column:
        x_column, y_column = dataset.columns[:2]  # Default to the first two columns

    # Infer element columns if not provided
    if not element_columns:
        element_columns = [col for col in dataset.columns if col not in [x_column, y_column]]

    results = {}

    for element in element_columns:
        print(f"Analyzing element: {element}")

        # Prepare data for clustering
        data = dataset[[element]].dropna()
        scaler = StandardScaler()
        data[element] = scaler.fit_transform(data[element].values.reshape(-1, 1))

        # Step 3: Determine the optimal number of clusters
        X = data

        bic_scores_kmeans = []
        inertia = []
        silhouette_scores_kmeans = []
        davies_bouldin_scores_kmeans = []
        calinski_harabasz_scores_kmeans = []
        K = range(2, 11)

        for k in K:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(X)
            labels = kmeans.labels_

            gmm = GaussianMixture(n_components=k, random_state=42)
            gmm.fit(X)
            bic_scores_kmeans.append(gmm.bic(X))
            inertia.append(kmeans.inertia_)
            silhouette_scores_kmeans.append(silhouette_score(X, labels))
            davies_bouldin_scores_kmeans.append(davies_bouldin_score(X, labels))
            calinski_harabasz_scores_kmeans.append(calinski_harabasz_score(X, labels))

        # Plot the results of the different metrics
        plt.figure(figsize=(15, 10))
        plt.subplot(2, 3, 1)
        plt.plot(K, inertia, 'bx-')
        plt.title('Elbow Method')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Inertia')

        plt.subplot(2, 3, 2)
        plt.plot(K, silhouette_scores_kmeans, 'bx-')
        plt.title('Silhouette Method')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Silhouette Score')

        plt.subplot(2, 3, 3)
        plt.plot(K, davies_bouldin_scores_kmeans, 'bx-')
        plt.title('Davies-Bouldin Method')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Davies-Bouldin Score')

        plt.subplot(2, 3, 4)
        plt.plot(K, calinski_harabasz_scores_kmeans, 'bx-')
        plt.title('Calinski-Harabasz Method')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Calinski-Harabasz Score')

        plt.subplot(2, 3, 5)
        plt.plot(K, bic_scores_kmeans, 'bx-')
        plt.title('BIC Method')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('BIC Score')

        plt.tight_layout()
        plt.show()

        optimal_k = 4  # Default optimal cluster number

        kmeans = KMeans(n_clusters=optimal_k, random_state=42)
        kmeans_labels = kmeans.fit_predict(X)

        # Custom K-medoids implementation
        def k_medoids(X, n_clusters, max_iter=300, random_state=42):
            np.random.seed(random_state)
            medoid_indices = np.random.choice(len(X), n_clusters, replace=False)
            medoids = X.iloc[medoid_indices]
            labels = np.zeros(len(X))

            for _ in range(max_iter):
                labels = pairwise_distances_argmin_min(X, medoids)[0]
                new_medoids = []
                for cluster_idx in range(n_clusters):
                    cluster_points = X[labels == cluster_idx]
                    if len(cluster_points) > 0:
                        distances = cdist(cluster_points, cluster_points)
                        new_medoid_idx = np.argmin(distances.sum(axis=1))
                        new_medoids.append(cluster_points.iloc[new_medoid_idx])
                    else:
                        new_medoids.append(X.sample(1, random_state=random_state))
                new_medoids = pd.concat(new_medoids)

                if new_medoids.equals(medoids):
                    break
                medoids = new_medoids

            return np.array(labels), medoids

        kmedoids_labels, _ = k_medoids(X, n_clusters=optimal_k)

        # DBSCAN
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        dbscan_labels = dbscan.fit_predict(X)

        # Hierarchical Clustering
        hierarchical = AgglomerativeClustering(n_clusters=optimal_k)
        hierarchical_labels = hierarchical.fit_predict(X)

        # Evaluate clustering methods
        kmeans_silhouette = silhouette_score(X, kmeans_labels)
        kmedoids_silhouette = silhouette_score(X, kmedoids_labels)
        dbscan_silhouette = silhouette_score(X, dbscan_labels) if len(set(dbscan_labels)) > 1 else None
        hierarchical_silhouette = silhouette_score(X, hierarchical_labels)

        kmeans_davies_bouldin = davies_bouldin_score(X, kmeans_labels)
        kmedoids_davies_bouldin = davies_bouldin_score(X, kmedoids_labels)
        dbscan_davies_bouldin = davies_bouldin_score(X, dbscan_labels) if len(set(dbscan_labels)) > 1 else None
        hierarchical_davies_bouldin = davies_bouldin_score(X, hierarchical_labels)

        kmeans_calinski_harabasz = calinski_harabasz_score(X, kmeans_labels)
        kmedoids_calinski_harabasz = calinski_harabasz_score(X, kmedoids_labels)
        dbscan_calinski_harabasz = calinski_harabasz_score(X, dbscan_labels) if len(set(dbscan_labels)) > 1 else None
        hierarchical_calinski_harabasz = calinski_harabasz_score(X, hierarchical_labels)

        # Uncertainty Evaluation
        clustering_uncertainty = {
            'K-Means': np.std([kmeans_silhouette, kmeans_davies_bouldin, kmeans_calinski_harabasz]),
            'K-Medoids': np.std([kmedoids_silhouette, kmedoids_davies_bouldin, kmedoids_calinski_harabasz]),
            'DBSCAN': np.std([dbscan_silhouette, dbscan_davies_bouldin, dbscan_calinski_harabasz]),
            'Hierarchical': np.std([hierarchical_silhouette, hierarchical_davies_bouldin, hierarchical_calinski_harabasz])
        }

        plt.figure(figsize=(10, 5))
        plt.bar(clustering_uncertainty.keys(), clustering_uncertainty.values())
        plt.title(f'Clustering Method Uncertainty for {element}')
        plt.ylabel('Uncertainty')
        plt.show()

        metric_uncertainty = {
            'Silhouette': np.std([kmeans_silhouette, kmedoids_silhouette, dbscan_silhouette, hierarchical_silhouette]),
            'Davies-Bouldin': np.std([kmeans_davies_bouldin, kmedoids_davies_bouldin, dbscan_davies_bouldin, hierarchical_davies_bouldin]),
            'Calinski-Harabasz': np.std([kmeans_calinski_harabasz, kmedoids_calinski_harabasz, dbscan_calinski_harabasz, hierarchical_calinski_harabasz])
        }

        plt.figure(figsize=(10, 5))
        plt.bar(metric_uncertainty.keys(), metric_uncertainty.values())
        plt.title(f'Evaluation Metric Uncertainty for {element}')
        plt.ylabel('Uncertainty')
        plt.show()

        results[element] = {
            'kmeans': kmeans_labels,
            'kmedoids': kmedoids_labels,
            'dbscan': dbscan_labels,
            'hierarchical': hierarchical_labels,
            'clustering_uncertainty': clustering_uncertainty,
            'metric_uncertainty': metric_uncertainty
        }

    return results

# Example Usage:
# results = analyze_clustering('data.csv', x_column='Easting', y_column='Northing', element_columns=['Element1', 'Element2'])