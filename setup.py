from setuptools import setup, find_packages

setup(
    name="cluster_tools",
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
            "cluster_dbscan = cluster_tools.cli.clustering_dbscan:main",
            "cluster_hdbscan = cluster_tools.cli.clustering_hdbscan:main",
            "csv_convert = cluster_tools.cli.csv_convertor:main",
            "dedisperse = cluster_tools.cli.DDplan_dedisperse:main",
        ]
    },
)