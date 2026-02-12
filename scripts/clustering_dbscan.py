#!/usr/bin/env python3
import pandas as pd
from sklearn.cluster import DBSCAN
import glob
import argparse
import os
from frbfunction.io import DM_delay, load_singlepulse
from frbfunction.clustering import DBSCAN_clustering

def main():
    parser = argparse.ArgumentParser(
        description="Clustering single-pulse candidates using DBSCAN.."
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
        default="clustered_candidates.singlepulse",
        help="Outputs a .singlepulse file with Highest SNR candidate from each cluster (default: clustered.singlepulse)."
    )

    parser.add_argument(
        "-e","--eps",
        type=float,
        default=0.05,
        help="eps parameter for DBSCAN (default: 0.05)."
    )

    parser.add_argument(
        "--min_samples",
        type=int,
        default=5,
        help="min_samples parameter for DBSCAN (default: 5)."
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

    df_all = load_singlepulse(args.single_path, verbose=True)
    print(f"Total candidates: {len(df_all)}")
  
    # Calculate dispersion delay
    df_all["Delay_s"] = DM_delay(df_all["DM"], args.frequency_low, args.bandwidth)
   
    X = df_all[["Delay_s", "Time"]]

    # DBSCAN clustering
    df_all = DBSCAN_clustering(
        df_all,
        cluster_column=["Delay_s", "Time"],
        eps=args.eps,
        min_samples=args.min_samples,
        verbose=True
    )

    if args.store_all:
        df_all.to_csv(f"all_candidates_with_clusters_eps{args.eps}_min_samples{args.min_samples}.csv", index=False)
        print(f"Saved all candidates with cluster labels to: all_candidates_with_clusters_eps{args.eps}_min_samples{args.min_samples}.csv")
    
    # Filter out noise (-1)
    df_clusters = df_all[df_all["cluster"] != -1]

    # Keep highest-SNR candidate from each cluster
    idx = df_clusters.groupby("cluster")["Sigma"].idxmax()
    df_best = df_clusters.loc[idx].reset_index(drop=True)

    # Filter by SNR
    df_best = df_best[df_best["Sigma"] > args.snr] 
    print(f"Candidates after SNR > {args.snr} filter: {len(df_best)}") 

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
