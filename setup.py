from setuptools import setup, find_packages

setup(
    name="frbfunction",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "hdbscan",
        "your",
    ],
    entry_points={
        "console_scripts": [
            "cluster_dbscan = frbfunction.cli.clustering_dbscan:main",
            "cluster_hdbscan = frbfunction.cli.clustering_hdbscan:main",
            "csv_convert = frbfunction.cli.csv_convertor:main",
            "dedisperse = frbfunction.cli.DDplan_dedisperse:main",
        ]
    },
)