#!/usr/bin/env python3
import pandas as pd
import numpy as np
import glob

# Useful functions for clustering scripts

def DM_delay(DM, f1, BW):
    """
    Calculate the dispersion delay in seconds between two frequencies.
    
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
    delay_s = 4.15e3 * DM * (f1**-2 - f2**-2) 
    return delay_s

def load_singlepulse(path, verbose=True):
    """
    Load all PRESTO .singlepulse files into a single DataFrame.

    Parameters
    ----------
    path : str
        Path to directory containing .singlepulse files, e.g.
        '/home/ankit_linux/project2.0/bb_inj/singlepulse'

    verbose : bool
        Print summary statistics if True

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with columns ['DM', 'Sigma', 'Time', 'Sample', 'Downfact']
    """
    files = glob.glob(path + '/*.singlepulse')

    if verbose:
        print(f"Loading {len(files)} singlepulse files...")

    all_candidates = []

    for f in files:
        try:
            data = np.loadtxt(f, comments='#')

            # Handle single-row files
            if data.ndim == 1 and data.size == 5:
                data = data.reshape(1, -1)

            if data.size > 0:
                all_candidates.append(data)

        except Exception:
            # Skip unreadable or empty files
            continue

    if all_candidates:
        all_candidates = np.vstack(all_candidates)
        df = pd.DataFrame(all_candidates, columns=['DM', 'Sigma', 'Time', 'Sample', 'Downfact'])
    else:
        df = pd.DataFrame(columns=['DM', 'Sigma', 'Time', 'Sample', 'Downfact'])

    if verbose and len(df) > 0:
        print(f"\nLoaded {len(df):,} candidates")
        print(f"DM range   : {df['DM'].min():.2f} – {df['DM'].max():.2f} pc/cm³")
        print(f"Time range : {df['Time'].min():.2f} – {df['Time'].max():.2f} s")
        print(f"Sigma range: {df['Sigma'].min():.2f} – {df['Sigma'].max():.2f}")

    return df

if __name__ == "__main__":
    print("This file contains utility functions for clustering scripts. Please import and use the functions as needed.")