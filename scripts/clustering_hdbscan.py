#!/usr/bin/env python3
import pandas as pd
import hdbscan
import glob
import argparse
from sklearn.preprocessing import StandardScaler
import os

def DM_delay(DM, f1, BW):
    """
    Calculate the dispersion delay in milliseconds between two frequencies.
    
    Parameters:
    DM : float
        Dispersion Measure in pc cm^-3
    f1 : float
        Lower frequency in MHz
    BW : float
        Bandwidth in MHz
    
    Returns:
    float
        Dispersion delay in seconds
    """
    f2 = f1 + BW
    delay_s = 4.15e3 * DM * (f1**-2 - f2**-2)  # Convert to seconds
    return delay_s


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
        help="Outputs a .singlepulse file with Highest SNR candidate from each cluster (default: clustered.singlepulse)."
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

    parser.add_argument(
        "--snr",
        type=float,
        default=6,
        help="snr threshold value"
    )

    parser.add_argument(
        "-f_low", "--frequency_low",
        type=float,
        default=550.0,
        help="Lower frequency in MHz (default: 550.0 MHz)."
    )

    parser.add_argument(
        "-bw", "--bandwidth",
        type=float,
        default=200.0,
        help="Bandwidth in MHz (default: 200.0 MHz)."
    )

    parser.add_argument(
        "--store_all",
        action="store_true",
        help="Store all candidates with their cluster labels in an output file (default: only highest SNR per cluster)."
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

    # Filter by SNR
    #df_all = df_all[df_all["Sigma"] > args.snr] 
    #print(f"Candidates after SNR > {args.snr} filter: {len(df_all)}")   

    # Calculate dispersion delay
    df_all["Delay_s"] = DM_delay(df_all["DM"], args.frequency_low, args.bandwidth)
   
    X = df_all[["Delay_s", "Time"]]

    # HDBSCAN clustering
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=args.min_cluster_size,
        min_samples=args.min_samples
    )

    labels = clusterer.fit_predict(X)
    df_all["cluster"] = labels

    # Summary
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print(f"Clusters found (excluding noise): {n_clusters}")

    if n_clusters == 0:
        print("No clusters found. Exiting.")
        return

    if args.store_all:
        df_all.to_csv("all_candidates_with_clusters.csv", index=False)
        print("Saved all candidates with cluster labels to: all_candidates_with_clusters.csv")
    
    # Filter out noise (-1)
    df_clusters = df_all[df_all["cluster"] != -1]

    # Keep highest-SNR candidate from each cluster
    idx = df_clusters.groupby("cluster")["Sigma"].idxmax()
    df_best = df_clusters.loc[idx].reset_index(drop=True)
    df_best = df_best[df_best["Sigma"] > args.snr]

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

    print(f"Saved candidates to: {output_file}")


if __name__ == "__main__":
    main()
