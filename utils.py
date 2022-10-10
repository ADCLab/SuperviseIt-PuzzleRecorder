"""Utility refactored from main."""
from datetime import datetime


class DataMedium:
    """A class to transfer data between the main program and window."""

    num_sorting_clusters: int = 0
    num_placing_clusters: int = 0
    received_clusters: bool = False

    num_sorted_clusters: int = 0
    num_placed_clusters: int = 0

    sorting_clusters_times: list[list[datetime]] = []
    placing_clusters_times: list[list[datetime]] = []

    @classmethod
    def set_clusters(cls, num_sorting_clusters: int, num_placing_clusters: int):
        """Set the cluster numbers."""
        # Set the class variables
        DataMedium.num_sorting_clusters = num_sorting_clusters
        DataMedium.num_placing_clusters = num_placing_clusters
        DataMedium.received_clusters = True

        # Initialize the times
        for _ in range(DataMedium.num_sorting_clusters):
            DataMedium.sorting_clusters_times.append(list())

        for _ in range(DataMedium.num_placing_clusters):
            DataMedium.placing_clusters_times.append(list())

    @classmethod
    def is_on_sorting(cls) -> bool:
        """Check if the trial is a sorting trial."""
        return DataMedium.num_sorted_clusters < DataMedium.num_sorting_clusters

    @classmethod
    def is_on_placing(cls) -> bool:
        """Check if the trial is a placing trial."""
        return (
            DataMedium.num_placed_clusters < DataMedium.num_placing_clusters
            and not DataMedium.is_on_sorting()
        )
