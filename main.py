"""Main file."""

import csv
import sys
from datetime import datetime

from utils import get_cluster_name


def main():
    """Run the entry code."""
    # Return if the filename is not provided
    if len(sys.argv) < 2:
        print("Please enter a file name for this participant.")
        return

    # Get the current date for entry
    current_date = datetime.now()
    date_string = current_date.strftime("%m/%d/%Y")

    # Execute the main loop of trials
    print("Press the Button to start!")
    with open(sys.argv[1], "w", newline="") as file:
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
