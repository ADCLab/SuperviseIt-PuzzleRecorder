"""Main file."""

import csv
import sys
from datetime import datetime


def main():
    """Run the entry code."""
    # Return if the arguments are not provided
    if len(sys.argv) < 4:
        print("Not enough information provided.\nPlease use the format:\n")
        print(
            f"python {sys.argv[0]} [filename] [# of sorting clusters] [# of placing clusters]"
        )
        return

    # Get the arguments
    filename = sys.argv[1]
    if filename.endswith(".csv") is False:
        print("Please enter a csv file.")
        return

    try:
        # Convert the cluster numbers to int types
        num_sorting_clusters = int(sys.argv[2])
        num_placing_clusters = int(sys.argv[3])

        # Make sure that there is at least 1 of each type of cluster
        if num_sorting_clusters < 1 or num_placing_clusters < 1:
            raise ValueError

    except ValueError:
        print("Please enter a whole number for the # of clusters.")
        return

    # Get the current date for entry
    current_date = datetime.now()
    date_string = current_date.strftime("%m/%d/%Y")

    # Declare clusters
    sorting_clusters: list[list[list]] = []
    placing_clusters: list[list[list]] = []

    print("Press the Button to start Sorting Clusters")
    for i in range(num_sorting_clusters):
        sorting_clusters.append(list())
        trial_loop(sorting_clusters[i], date_string)
        print(sorting_clusters[i])

    print("Press the Button to start Placing Clusters")
    for i in range(num_placing_clusters):
        placing_clusters.append(list())
        trial_loop(placing_clusters[i], date_string)
        print(placing_clusters[i])

    # Create header rows
    row1 = []
    row2 = []
    for i in range(num_sorting_clusters):
        row1 += [f"Sorting Cluster {i+1}", "", "", ""]
        row2 += ["#", "Date", "Time", "Interval"]

    for i in range(num_placing_clusters):
        row1 += [f"Placing Cluster {i+1}", "", "", ""]
        row2 += ["#", "Date", "Time", "Interval"]

    # Create data rows
    data_rows = []
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

    # Execute the main loop of trials
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(row1)
        writer.writerow(row2)
        writer.writerows(data_rows)


def trial_loop(sorting_cluster: list, date_string: str):
    """Run the loop to capture trials."""
    # Main trial loop
    start_time = None
    piece_num = 1
    while True:

        # Wait for a button press or exit command
        # Return if the entry was not an empty button press
        if input() != "":
            return

        # Get the current time
        current_time = datetime.now()

        # Insert a Piece line
        if start_time:
            interval = current_time - start_time
            sorting_cluster.append(
                [
                    f"Piece {piece_num}",
                    date_string,
                    current_time.strftime("%H:%M:%S"),
                    f"{interval.seconds + interval.microseconds / (10**6):.3f}",
                ]
            )
            piece_num += 1

        # Insert the Initiation line
        else:
            sorting_cluster.append(
                ["Initiation", date_string, current_time.strftime("%H:%M:%S"), ""]
            )

        # Reset the start time for interval comparison
        start_time = current_time


# Run the program
if __name__ == "__main__":
    main()
