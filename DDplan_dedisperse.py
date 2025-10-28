#!/usr/bin/env python3
# Script to dedisperse data based on DDplan output
from builtins import zip
import pandas as pd
import os
import argparse


def myexecute(cmd):
    print("'%s'"%cmd)
    os.system(cmd)

def main():
    parser = argparse.ArgumentParser(description="Script to dedisperse data based on DDplan output")

    parser.add_argument('-f', '--fil_file', type= str, help='Filterbank file path ', required=True)
    parser.add_argument('-m', '--mask_file', type= str, help='RFI mask file path ', required=True)
    parser.add_argument('-p', '--parameters_file', type= str, help='DDplan parameters file path ', required=True)

    args = parser.parse_args()

    basename = os.path.splitext(os.path.basename(args.fil_file))[0] # Base name for output files
    rawfiles = args.fil_file # Input filterbank file path
    mask = args.mask_file # RFI mask file path


    df = pd.read_csv(args.parameters_file, sep='\s+')
    print(df)
    print(df.shape)

    #if the max DM is greater than 1000, output subbands
    if df["High_DM"].max() > 1000:
        outsubs = True # By default, do not output subbands
    else:
        outsubs = False 


    nsub = 32 # Number of subbands

    # dDM steps from DDplan.py
    dDMs        = df["dDM"].tolist()
    # dsubDM steps
    dsubDMs     = df["dsubDM"].tolist()
    # downsample factors
    downsamps   = df["DownSamp"].tolist()
    # number of calls per set of subbands
    subcalls    = df["calls"].tolist()
    # The low DM for each set of DMs
    startDMs    = df["Low_DM"].tolist()
    # DMs/call
    dmspercalls = df["DM_call"].tolist()


    for dDM, dsubDM, dmspercall, downsamp, subcall, startDM in zip(dDMs, dsubDMs, dmspercalls, downsamps, subcalls, startDMs):
        # Loop over the number of calls
        for ii in range(subcall):
            subDM = startDM + (ii+0.5)*dsubDM
            loDM = startDM + ii*dsubDM
            if outsubs:
                # Get our downsampling right
                subdownsamp = downsamp // 2
                datdownsamp = 2
                if downsamp < 2: subdownsamp = datdownsamp = 1
                # First create the subbands
                myexecute("prepsubband -sub -subdm %.2f -nsub %d -downsamp %d -o %s %s" %
                        (subDM, nsub, subdownsamp, basename, rawfiles))
                # And now create the time series
                subnames = basename+"_DM%.2f.sub[0-9]*"%subDM
                myexecute("prepsubband -lodm %.2f -dmstep %.2f -numdms %d -downsamp %d -mask %s -o %s %s -nobary" %
                        (loDM, dDM, dmspercall, datdownsamp, mask, basename, subnames))
            else:
                myexecute("prepsubband -nsub %d -lodm %.2f -dmstep %.2f -numdms %d -downsamp %d -mask %s -o %s %s -nobary" %
                        (nsub, loDM, dDM, dmspercall, downsamp, mask, basename, rawfiles))


if __name__ == "__main__":
    main()


