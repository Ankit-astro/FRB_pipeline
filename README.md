# FRB Search and Classification Pipeline

A complete, production-ready pipeline for searching and classifying Fast Radio Burst (FRB) candidates in telescope filterbank data with built-in CLI support.

## Overview

This pipeline is a one-stop solution for:
- **Pre-processing**: Dedispersion and single-pulse detection using [PRESTO](https://github.com/scottransom/presto)
- **Clustering**: Advanced candidate clustering using HDBSCAN and DBSCAN algorithms
- **Candidate Creation**: DM-time plot analysis using modified [your-NB](https://github.com/Ankit-astro/your-NB.git) for better classification
- **Classification**: Automated narrowband burst identification using trained [fetch-NB](https://github.com/Ankit-astro/fetch-NB.git) models

## Features

✨ **Easy to Use CLI**
- Simple command-line interface with four main commands
- Comprehensive help documentation for all commands
- Support for both DBSCAN and HDBSCAN clustering algorithms

📦 **Modular Design**
- Clean, importable Python modules for use in scripts
- Organized package structure with CLI wrappers
- Well-documented utility functions

🔧 **Flexible Configuration**
- Customizable clustering parameters
- Multi-file processing support
- SNR filtering and candidate ranking

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- (Optional) PRESTO for full pipeline functionality

### Quick Install

#### Using Virtual Environment (Recommended)

```bash
# Clone the repository
git clone https://github.com/Ankit-astro/cluster-tools.git
cd cluster-tools

# Create and activate a virtual environment
python3 -m venv frb_env
source frb_env/bin/activate  # On Linux/macOS
# or
frb_env\Scripts\activate     # On Windows

# Install the package
pip install -e .
```

#### Using Conda

```bash
# Clone the repository
git clone https://github.com/Ankit-astro/cluster-tools.git
cd cluster-tools

# Create and activate conda environment
conda create -n frb python=3.10
conda activate frb

# Install the package
pip install -e .
```

### Verify Installation

```bash
# Check if CLI commands are available
cluster_dbscan --help
cluster_hdbscan --help
csv_convert --help
dedisperse --help
```

## Quick Start

### Using CLI Commands

#### 1. DBSCAN Clustering
Cluster single-pulse candidates using DBSCAN algorithm:

```bash
cluster_dbscan -s /path/to/singlepulse/files \
               -o clustered_output.singlepulse \
               -e 0.05 \
               --snr 6 \
               -f_low 550.0 \
               -bw 200.0
```

#### 2. HDBSCAN Clustering
Cluster candidates using the more robust HDBSCAN algorithm:

```bash
cluster_hdbscan -s /path/to/singlepulse/files \
                -o clustered_output.singlepulse \
                --min_cluster_size 5 \
                --snr 6 \
                -f_low 550.0 \
                -bw 200.0
```

#### 3. CSV Conversion
Convert filterbank and candidate files to CSV format:

```bash
csv_convert -f data.fil \
            -i candidates.singlepulse \
            -o output_directory/ \
            -cm channel_mask.mask
```

#### 4. Dedispersion
Perform dedispersion based on DDplan parameters:

```bash
dedisperse -f data.fil \
           -m rfi_mask.rfimask \
           -p ddplan_parameters.txt
```

### Using as Python Module

```python
from cluster_tools.io import DM_delay, load_singlepulse
from cluster_tools.clustering import DBSCAN_clustering, HDBSCAN_clustering
import pandas as pd

# Load singlepulse candidates
df = load_singlepulse("/path/to/singlepulse/files", verbose=True)

# Calculate dispersion delay
DM = 300.5  # Dispersion measure
f_low = 550.0  # MHz
bandwidth = 200.0  # MHz
delay = DM_delay(DM, f_low, bandwidth)

# Perform clustering
df_clustered = HDBSCAN_clustering(
    df,
    cluster_column=['Delay_s', 'Time'],
    min_cluster_size=5,
    verbose=True
)

print(f"Found {df_clustered['cluster'].nunique()} clusters")
```

## Project Structure

```
FRB-pipe/
├── src/cluster_tools/              # Main package
│   ├── __init__.py              # Package initialization
│   ├── io.py                    # I/O utilities (DM_delay, load_singlepulse)
│   ├── clustering.py            # Clustering algorithms (DBSCAN, HDBSCAN)
│   └── cli/                     # CLI command modules
│       ├── __init__.py
│       ├── clustering_dbscan.py
│       ├── clustering_hdbscan.py
│       ├── csv_convertor.py
│       └── DDplan_dedisperse.py
├── scripts/                      # Alternative script versions
│   ├── clustering_dbscan.py
│   ├── clustering_hdbscan.py
│   ├── csv_convertor.py
│   ├── DDplan_dedisperse.py
│   └── disp_parameter.sh
├── example/                      # Example data and configuration
│   ├── channels_to_remove.txt
├── setup.py                      # Package setup configuration
├── pyproject.toml               # Project metadata and CLI entry points
└── README.md                    # Documentation
```

## Command Reference

### cluster_dbscan

Cluster single-pulse candidates using DBSCAN algorithm.

```
Usage: cluster_dbscan [OPTIONS]

Options:
  -s, --single_path PATH          Path containing .singlepulse files [required]
  -o, --output FILE              Output .singlepulse file [default: clustered_candidates.singlepulse]
  -e, --eps FLOAT                eps parameter for DBSCAN [default: 0.05]
  --min_samples INT              min_samples parameter for DBSCAN [default: 5]
  --snr FLOAT                    SNR threshold value [default: 6]
  -f_low, --frequency_low FLOAT  Lower frequency in MHz [default: 550.0]
  -bw, --bandwidth FLOAT         Bandwidth in MHz [default: 200.0]
  --store_all                    Store all candidates with cluster labels in CSV
  -h, --help                     Show help message
```

### cluster_hdbscan

Cluster single-pulse candidates using HDBSCAN algorithm.

```
Usage: cluster_hdbscan [OPTIONS]

Options:
  -s, --single_path PATH          Path containing .singlepulse files [required]
  -o, --output FILE              Output .singlepulse file [default: clustered_candidates.singlepulse]
  --min_cluster_size INT         Minimum cluster size for HDBSCAN [default: 5]
  --min_samples INT              min_samples parameter for HDBSCAN [default: None]
  --snr FLOAT                    SNR threshold value [default: 6]
  -f_low, --frequency_low FLOAT  Lower frequency in MHz [default: 550.0]
  -bw, --bandwidth FLOAT         Bandwidth in MHz [default: 200.0]
  --store_all                    Store all candidates with cluster labels in CSV
  -h, --help                     Show help message
```

### csv_convert

Convert .fil and .singlepulse/.injinf files to CSV format.

```
Usage: csv_convert [OPTIONS]

Options:
  -f, --fil_file PATH             Paths to input filterbank files [required]
  -i, --info_file PATH            Paths to .injinf or .singlepulse files [required]
  -o, --output_dir PATH           Directory to save output CSV file [required]
  -cm, --channel_mask FILE        Channel mask file path [optional]
  -h, --help                      Show help message
```

### dedisperse

Dedisperse data based on DDplan output parameters.

```
Usage: dedisperse [OPTIONS]

Options:
  -f, --fil_file PATH             Filterbank file path [required]
  -m, --mask_file PATH            RFI mask file path [required]
  -p, --parameters_file PATH      DDplan parameters file path [required]
  -h, --help                      Show help message
```

## Dependencies

### Core Dependencies
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning utilities
- **hdbscan**: Hierarchical DBSCAN clustering

### Optional Dependencies
- **PRESTO**: For dedispersion and singlepulse search 
- **your-NB**: Modified version for narrowband burst detection
- **fetch-NB**: Trained model for automated burst classification

## Troubleshooting

### CLI Commands Not Found

After installation, if CLI commands are not found:

```bash
# Reinstall the package
pip uninstall -y cluster_tools
pip install -e .

# Verify installation
which cluster_dbscan
```

### Import Errors

If you encounter import errors:

```bash
# Make sure you're in the correct environment
source /path/to/venv/bin/activate

# Reinstall with dependencies
pip install -e . --force-reinstall
```

### Python Module Usage Issues

If importing from the module doesn't work:

```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install in development mode
pip install -e .
```


