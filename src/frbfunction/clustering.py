import pandas as pd
import hdbscan
from sklearn.cluster import DBSCAN

def DBSCAN_clustering(df, cluster_column =['Delay_s', 'Time'], eps=0.05, min_samples=5, verbose=False):
    # Perform DBSCAN clustering on the specified columns of the DataFrame.
    X = df[cluster_column]
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(X)
    result = df.copy()
    result["cluster"] = labels
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    if verbose:
        print(f"DBSCAN found {n_clusters} clusters (excluding noise).")

    return result
    
def HDBSCAN_clustering(df, cluster_column =['Delay_s', 'Time'], min_cluster_size=5, min_samples=None, verbose=False):
    # Perform HDBSCAN clustering on the specified columns of the DataFrame.
    X = df[cluster_column]
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples)
    labels = clusterer.fit_predict(X)
    result = df.copy()
    result["cluster"] = labels
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    if verbose:
        print(f"HDBSCAN found {n_clusters} clusters (excluding noise).")
    
    return result