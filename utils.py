"""Utility functions refactored from main."""


def get_cluster_name(cluster_num):
    """Convert a cluster number to a name."""
    if cluster_num <= 5:
        return f"Sorting Cluster {cluster_num}"
    else:
        return f"Placing Cluster {cluster_num-5}"
