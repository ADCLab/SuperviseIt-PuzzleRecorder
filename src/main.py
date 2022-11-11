"""Main file."""

import csv
from datetime import datetime
from threading import Thread

from utils import DataMedium
from window import Window


def main():
    """Run the program."""
    # Get the current date for entry
    current_date = datetime.now()
    date_string = current_date.strftime("%m/%d/%Y")

    # Wait for the clusters numbers to be entered in the GUI
    while DataMedium.is_trials_complete is False:
        pass

    # Declare clusters
    sorting_clusters: list[list[list]] = []
    placing_clusters: list[list[list]] = []

    for times in DataMedium.sorting_clusters_times:
        cluster = list()
        set_cluster_data(cluster, times, date_string)
        sorting_clusters.append(cluster)

    for times in DataMedium.placing_clusters_times:
        cluster = list()
        set_cluster_data(cluster, times, date_string)
        placing_clusters.append(cluster)

    # Create rows
    row1 = []
    row2 = []
    data_rows = []
    set_rows(row1, row2, data_rows, sorting_clusters, placing_clusters)

    # Write to the file
    with open(DataMedium.filename, "w", newline="") as file:
        writer = csv.writer(file)

        # Header
        writer.writerow(row1)
        writer.writerow(row2)

        # Data
        writer.writerows(data_rows)

        # Errors
        writer.writerow([])
        writer.writerow(["Missorted", "Unsorted"])
        writer.writerow([DataMedium.num_missorted, DataMedium.num_unsorted])

    DataMedium.is_finished_main = True


def set_cluster_data(cluster: list[list[str]], times: list[datetime], date_string: str):
    """Set cluster data."""
    start_time = None
    piece_num = 1
    for current_time in times:

        # Insert a Piece line
        if start_time:
            interval = current_time - start_time
            cluster.append(
                [
                    f"Piece {piece_num}",
                    date_string,
                    current_time.strftime("%H:%M:%S"),
                    f"{(interval.seconds + interval.microseconds / (10**6)):.3f}",
                ]
            )
            piece_num += 1

        # Insert the Initiation line
        else:
            cluster.append(
                ["Initiation", date_string, current_time.strftime("%H:%M:%S"), ""]
            )

        # Reset the start time for interval comparison
        start_time = current_time


def set_rows(
    row1: list[str],
    row2: list[str],
    data_rows: list[list[str]],
    sorting_clusters: list[list[list[str]]],
    placing_clusters: list[list[list[str]]],
):
    """Fill out the rows."""
    # Fill out the header rows
    for i in range(DataMedium.num_sorting_clusters):
        row1 += [f"Sorting Cluster {i+1}", "", "", ""]
        row2 += ["#", "Date", "Time", "Interval"]

    for i in range(DataMedium.num_placing_clusters):
        row1 += [f"Placing Cluster {i+1}", "", "", ""]
        row2 += ["#", "Date", "Time", "Interval"]

    # Fill out the data rows
    counter = 0
    while True:
        data_rows.append([])
        more_rows_needed = False

        # Get the data from the next row in all sorting clusters
        for cluster in sorting_clusters:

            if counter < len(cluster):
                data_rows[counter] += cluster[counter]
                more_rows_needed = True
            else:
                data_rows[counter] += ["", "", "", ""]

        # Get the data from the next row in all placing clusters
        for cluster in placing_clusters:

            if counter < len(cluster):
                data_rows[counter] += cluster[counter]
                more_rows_needed = True
            else:
                data_rows[counter] += ["", "", "", ""]

        counter += 1

        # Check if no new data was input
        if more_rows_needed is False:
            del data_rows[-1]
            break


# Run the program
if __name__ == "__main__":

    # Main thread
    main_thread = Thread(target=main)
    main_thread.daemon = True
    main_thread.start()

    # GUI
    window = Window()
    window.start()
