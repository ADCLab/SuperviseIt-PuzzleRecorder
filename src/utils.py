"""Utility refactored from main."""

import os
import sys
from datetime import datetime


class DataMedium:
    """A class to transfer data between the main program and window."""

    num_clusters: int = 5
    filename: str = f"{datetime.now().strftime('%m_%d_%Y')}.csv"
    cluster_order: list[str] = ["A", "B", "C", "D", "E"]
    cluster_times: list[list[datetime]] = [list() for _ in range(num_clusters)]

    num_misplaced: int = 0
    num_unplaced: int = 0

    is_trials_complete: bool = False
    is_finished_main: bool = False


class WindowData:
    """A class to hold data for the window."""

    piece_num: int = 1
    num_placed_clusters: int = 0

    is_in_trial: bool = False


def resource_path(relative_path: str):
    """Get absolute path to resource."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
