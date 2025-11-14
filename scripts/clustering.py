#!/usr/bin/env python3
import pandas as pd
import hdbscan
import glob
import argparse
from sklearn.preprocessing import StandardScaler
import os


def main():
    parser = argparse.ArgumentParser(
        description="Clustering single-pulse candidates using HDBSCAN.."
    )

    parser.add_argument(
        "-s", "--single_path",
        type=str,
        required=True,
        help="Path containing .singlepulse files."
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="clustered.singlepulse",
        help="Output .singlepulse file name (default: clustered.singlepulse)."
    )

    parser.add_argument(
        "--min_cluster_size",
        type=int,
        default=5,
        help="Minimum cluster size for HDBSCAN (default: 5)."
    )

    parser.add_argument(
        "--min_samples",
        type=int,
        default=None,
        help="min_samples parameter for HDBSCAN (default: None)."
    )

    args = parser.parse_args()
    path = os.path.join(args.single_path, "")

    # Find .singlepulse files
    files = glob.glob(path + "*.singlepulse")
    if not files:
        print(f"No .singlepulse files found in: {path}")
        return

    print(f"Found {len(files)} .singlepulse files.")

    # Load files
    dfs = []
    for f in files:
        df = pd.read_csv(
            f, sep=r"\s+", comment="#",
            names=["DM", "Sigma", "Time", "Sample", "Downfact"]
        )
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)
    print(f"Total candidates: {len(df_all)}")

    # Scale features
    X = df_all[["DM", "Time"]]
    X_scaled = StandardScaler().fit_transform(X)

    # HDBSCAN clustering
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=args.min_cluster_size,
        min_samples=args.min_samples
    )

    labels = clusterer.fit_predict(X_scaled)
    df_all["cluster"] = labels

    # Summary
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print(f"Clusters found (excluding noise): {n_clusters}")

    if n_clusters == 0:
        print("No clusters found. Exiting.")
        return

    # Filter out noise (-1)
    df_clusters = df_all[df_all["cluster"] != -1]

    # Keep highest-SNR candidate from each cluster
    idx = df_clusters.groupby("cluster")["Sigma"].idxmax()
    df_best = df_clusters.loc[idx].reset_index(drop=True)

    #print(f"Candidates selected (one per cluster): {len(df_best)}")

    # Save output file
    output_file = args.output
    if not output_file.endswith(".singlepulse"):
        output_file += ".singlepulse"

    with open(output_file, "w") as f:
        f.write("# DM      Sigma      Time (s)     Sample    Downfact\n")
        df_best[["DM", "Sigma", "Time", "Sample", "Downfact"]].to_string(
            f, index=False, header=False, float_format="%.8f"
        )

    print(f"Saved cleaned candidates to: {output_file}")


if __name__ == "__main__":
    main()
