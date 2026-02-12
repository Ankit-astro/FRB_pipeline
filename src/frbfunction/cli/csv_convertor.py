#!/usr/bin/env python3

import argparse
import os
import your
import pandas as pd
import numpy as np
def main():

    parser = argparse.ArgumentParser(description="Convert .fil and .injinf/.singlepulse files to CSV file for candidate h5 files.")
    parser.add_argument("-f", "--fil_file", required=True, nargs='+', help="Paths to input filterbank files")
    parser.add_argument("-i", "--info_file", required=True, nargs='+', help="Paths to .injinf or .singlepulse files")
    parser.add_argument("-o", "--output_dir", required=True, help="Directory to save output CSV file")
    parser.add_argument("-cm","--channel_mask", type=str, default=None, help="if you have channel mask files corresponding to filterbank files")

    args = parser.parse_args()

    # Resolve paths
    fil_files = [os.path.abspath(f) for f in args.fil_file]
    info_files = [os.path.abspath(f) for f in args.info_file]
    output_dir = os.path.abspath(args.output_dir)

    #checking input file extension
    name, extension = os.path.splitext(os.path.basename(info_files[0]))
    if extension not in ['.injinf', '.singlepulse']:
        raise ValueError("Info files must have .injinf or .singlepulse extension.")
    
    
    # Sanity check
    if len(fil_files) != len(info_files):
        raise ValueError("Number of .fil and .injinf files must be equal.")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Determine output filename
    base_name = os.path.splitext(os.path.basename(fil_files[0]))[0]

    if len(fil_files) > 1:
        csv_file_path = os.path.join(output_dir, base_name + "combined" + ".csv")
    else:
        csv_file_path = os.path.join(output_dir, base_name + ".csv")

    dataframes = []

    for fil_file, info_file in zip(fil_files, info_files):
        print(f"Processing filterbank file : {fil_file}")
        print(f"With info file : {info_file}")

        # Load .injinf file
        info_df = pd.read_csv(info_file, sep='\s+')

        # Extract data
        DM = info_df.iloc[:, 0].values 
        snr = info_df.iloc[:, 1].values
        stime = info_df.iloc[:, 2].values
        width_time = info_df.iloc[:, 3].values
        width_in_samp = info_df.iloc[:, 4].values
        label = np.zeros(len(DM), dtype=int) # Placeholder for label column
        chan_mask_path = args.channel_mask 
        # Process .fil file
        your_object = your.Your(fil_file)
        tsamp = your_object.your_header.tsamp
        width_samp = (width_time / tsamp) #converting sample width from sec to samples 
        


        if extension == '.injinf':
            width = np.array([int(np.log2(i)) for i in width_samp])
        else:
            width = np.array([int(np.log2(i)) for i in width_in_samp])

            
        df = pd.DataFrame({
            "file": [fil_file] * len(DM),
            "snr": snr,
            "width": width,
            "dm": DM,
            "label": label,
            "stime": stime,
            "chan_mask_path": chan_mask_path,
            "num_files": 1
        })

        dataframes.append(df)

    # Combine and save
    final_df = pd.concat(dataframes, ignore_index=True)
    final_df.to_csv(csv_file_path, index=False)

    print(f"CSV file saved at: {csv_file_path}")

if __name__ == "__main__":
    main()
