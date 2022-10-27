"""Utility refactored from main."""

import os
import sys
from datetime import datetime


class DataMedium:
    """A class to transfer data between the main program and window."""

    num_sorting_clusters: int = 0
    num_placing_clusters: int = 0

    filename: str
    sorting_clusters_times: list[list[datetime]] = []
    placing_clusters_times: list[list[datetime]] = []

    received_input: bool = False
    is_in_trial: bool = False
    is_trials_complete: bool = False
    is_finished_main: bool = False

    @classmethod
    def set_input(cls, filename: str, num_sorting_clusters: int, num_placing_clusters: int):
        """Set the input values."""
        # Set the class variables
        DataMedium.filename = filename
        DataMedium.num_sorting_clusters = num_sorting_clusters
        DataMedium.num_placing_clusters = num_placing_clusters
        DataMedium.received_input = True

        # Initialize the times
        for _ in range(DataMedium.num_sorting_clusters):
            DataMedium.sorting_clusters_times.append(list())

        for _ in range(DataMedium.num_placing_clusters):
            DataMedium.placing_clusters_times.append(list())


class WindowData:
    """A class to hold data for the window."""

    piece_num: int = 1
    num_sorted_clusters: int = 0
    num_placed_clusters: int = 0

    @classmethod
    def is_on_sorting(cls) -> bool:
        """Check if the trial is a sorting trial."""
        return WindowData.num_sorted_clusters < DataMedium.num_sorting_clusters

    @classmethod
    def is_on_placing(cls) -> bool:
        """Check if the trial is a placing trial."""
        return WindowData.num_sorted_clusters < DataMedium.num_sorting_clusters


def resource_path(relative_path: str):
    """Get absolute path to resource."""
    try:
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
