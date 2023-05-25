"""Main file."""

import csv
import random
import time
import uuid
import webbrowser
from datetime import datetime
from threading import Thread

import gspread
import numpy as np
import pyrealsense2 as rs
from PIL import Image
from pynput import keyboard

from utils import DataMedium
from window import Window


def main(participantId: str):
    """Run the program."""
    # Get the current date for entry
    current_date = datetime.now()
    date_string = current_date.strftime("%m/%d/%Y")

    # Wait for the clusters numbers to be entered in the GUI
    while DataMedium.is_trials_complete is False:
        pass

    clusters: list[list[list]] = []
    for times in DataMedium.cluster_times:
        cluster = list()
        set_cluster_data(cluster, times, date_string)
        clusters.append(cluster)

    # Create rows
    row1 = []
    row2 = []
    data_rows = []
    set_rows(row1, row2, data_rows, clusters)

    # Write to the file
    with open(f"{DataMedium.participantId}.csv", "w", newline="") as file:
        writer = csv.writer(file)

        # Header
        writer.writerow(
            [
                f"Cluster Order: {''.join(DataMedium.cluster_order)}",
            ]
        )
        writer.writerow(row1)
        writer.writerow(row2)

        # Data
        writer.writerows(data_rows)

    # Google Sheets
    gc = gspread.service_account(filename="sheetsCredentials.json")
    wks = gc.open("FOW Puzzle Task Errors").sheet1

    for cluster in DataMedium.cluster_order:
        wks.append_row(
            [f"{current_date.strftime('%B%d')} {participantId} {cluster}", 0, 0, 0]
        )

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
    placing_clusters: list[list[list[str]]],
):
    """Fill out the rows."""
    for i in range(DataMedium.num_clusters):
        row1 += [f"Cluster {DataMedium.cluster_order[i]}", "", "", ""]
        row2 += ["#", "Date", "Time", "Interval"]

    # Fill out the data rows
    counter = 0
    while True:
        data_rows.append([])
        more_rows_needed = False

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
    with open("participants.txt", "r+") as file:
        # Get the current and new participants
        participantsSet = set([line.strip() for line in file.readlines()])

        while (participantId := (uuid.uuid4().hex[:10])) in participantsSet:
            pass

        file.write(f"{participantId}\n")

        # Get the first letter of the order
        firstLetter = chr(65 + len(participantsSet) % 5)
        allLetters = ["A", "B", "C", "D", "E"]
        allLetters.remove(firstLetter)

        # Set the fields
        DataMedium.participantId = participantId
        DataMedium.cluster_order: list[str] = [firstLetter] + random.sample(
            allLetters, 4
        )

    # GUI
    window = Window()
    webbrowser.open("https://ucf.qualtrics.com/jfe/form/SV_a4CaLHGsRyrG5fw", new=1)

    # Camera
    try:
        # Reset camera in case it is occupied
        """
        NOTE breaks on lab computer. Meant to reset camera if it incorrectly thinks it is streaming

        ctx = rs.context()
        for device in ctx.query_devices():
            device.hardware_reset()
        time.sleep(1)
        """

        # Set up pipeline
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
        config.enable_record_to_file(f"{participantId}.bag")

        # Set up alignment
        align_to = rs.stream.color
        align = rs.align(align_to)

        # Start pipeline
        pipeline.start(config)

        def save_snapshot(identifier: str):
            """Save a picture from the camera."""
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            color_frame = aligned_frames.get_color_frame()

            color_image = np.asanyarray(color_frame.get_data())
            im = Image.fromarray(color_image)
            im.save(f"{participantId}_{identifier}.png")

        time.sleep(1)
        save_snapshot(0)

        window.save_snapshot = save_snapshot

    except Exception as e:
        print(e)
        exit(1)

    # Keyboard
    def on_release(key):
        """Mark date on keyboard ctrl_l release."""
        if key == keyboard.Key.ctrl_l:
            window.mark_date()

    listener = keyboard.Listener(on_release=on_release)
    listener.daemon = True
    listener.start()

    # Main thread
    main_thread = Thread(target=main, args=(participantId,))
    main_thread.daemon = True
    main_thread.start()

    window.start()

    # Stop camera
    del config  # Will not work without this line
    pipeline.stop()
