"""Main file."""

import csv
import sys
from datetime import datetime

from utils import get_cluster_name


def main():
    """Run the entry code."""
    # Return if the arguments are not provided
    if len(sys.argv) < 4:
        print("Not enough information provided.\nPlease use the format:\n")
        print(f"python {sys.argv[0]} [filename] [# of sorting clusters] [# of placing clusters]")
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

    # Execute the main loop of trials
    print("Press the Button to start!")
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        # Loop through every cluster
        for cluster_num in range(1, 3):
            writer.writerow([get_cluster_name(cluster_num)])
            writer.writerow(["#", "Date", "Time", "Interval"])
            trial_loop(writer, date_string)


def trial_loop(writer, date_string):
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

        # Insert the Initiation line
        if start_time:
            interval = current_time - start_time
            writer.writerow(
                [
                    f"Piece {piece_num}",
                    date_string,
                    current_time.strftime("%H:%M:%S"),
                    f"{interval.seconds + interval.microseconds / (10**6):.3f}"
                ]
            )
            piece_num += 1

        # Insert a Piece line
        else:
            writer.writerow(
                ["Initiation", date_string, current_time.strftime("%H:%M:%S"), ""]
            )

        # Reset the start time for interval comparison
        start_time = current_time


# Run the program
if __name__ == "__main__":
    main()
