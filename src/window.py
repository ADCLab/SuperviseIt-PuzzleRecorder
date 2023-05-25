"""The Window for the GUI."""

import tkinter
import tkinter.messagebox
from datetime import datetime

from utils import DataMedium, WindowData, resource_path

BACKGROUND_COLOR = "gray"


class Window:
    """The GUI Window."""

    def __init__(self):
        """Initialize the window."""
        self.create_window()

        self.create_header_frame()
        self.create_input_frame()
        self.create_button_frame()
        self.create_progress_frame()

    def create_window(self):
        """Create and initialize the close frame."""
        self.window = tkinter.Tk()
        self.window.title("Cluster Tracking")
        self.window.geometry("600x900")
        self.window.configure(background=BACKGROUND_COLOR)
        self.window.iconphoto(
            False, tkinter.PhotoImage(file=resource_path("src/TheTab_KGrgb_72ppi.png"))
        )

        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def create_header_frame(self):
        """Create and initialize the header."""
        self.header_frame = tkinter.Frame(
            self.window, pady=10, background=BACKGROUND_COLOR
        )

        self.title_label = tkinter.Label(
            self.header_frame,
            text="Cluster Tracking",
            font=("Times New Roman", 40),
            background=BACKGROUND_COLOR,
        )
        self.title_label.pack()

        self.header_frame.pack()

    def create_input_frame(self):
        """Create the frame for cluster input."""
        self.input_frame = tkinter.Frame(self.window, background=BACKGROUND_COLOR)

        # File name
        self.file_label = tkinter.Label(
            self.input_frame,
            text="Filename:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.file_input = tkinter.StringVar(value=f"{DataMedium.participantId}.csv")
        self.file_entry = tkinter.Entry(
            self.input_frame,
            textvariable=self.file_input,
            font=("Arial", 12),
            state="disabled",
        )
        self.file_label.pack()
        self.file_entry.pack(pady=(0, 10))

        # Cluster Order
        self.cluster_order_label = tkinter.Label(
            self.input_frame,
            text="Cluster Order:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.cluster_order_input = tkinter.StringVar(
            value="".join(DataMedium.cluster_order)
        )
        self.cluster_order_entry = tkinter.Entry(
            self.input_frame,
            textvariable=self.cluster_order_input,
            font=("Arial", 12),
            state="disabled",
        )
        self.cluster_order_label.pack()
        self.cluster_order_entry.pack(pady=(0, 10))

        # Copy id button
        def copy_id():
            self.window.clipboard_clear()
            self.window.clipboard_append(DataMedium.participantId)

        self.copyid_button = tkinter.Button(
            self.input_frame,
            text="Copy ID to Clipboard",
            font=("Arial Bold", 10),
            background="light gray",
            activebackground="dark gray",
            width=20,
            height=3,
            command=copy_id
        )
        self.copyid_button.pack(pady=(20, 10))

        self.input_frame.pack()

    def create_button_frame(self):
        """Create the frame for trial change."""
        self.button_frame = tkinter.Frame(self.window, background=BACKGROUND_COLOR)
        self.button_main_frame = tkinter.Frame(
            self.button_frame, background=BACKGROUND_COLOR
        )

        # Trial Button
        self.start_button = tkinter.Button(
            self.button_main_frame,
            text="Start Trial",
            font=("Arial Bold", 10),
            background="green",
            activebackground="dark green",
            foreground="black",
            width=20,
            height=10,
            command=self.start_trial,
        )
        self.start_button.pack(side=tkinter.LEFT, padx=(0, 10))

        self.stop_button = tkinter.Button(
            self.button_main_frame,
            text="Stop Trial",
            font=("Arial Bold", 10),
            background="light gray",
            activebackground="dark red",
            foreground="black",
            width=20,
            height=10,
            state="disabled",
            command=self.stop_trial,
        )
        self.stop_button.pack(side=tkinter.RIGHT, padx=(10, 10))

        self.button_main_frame.pack(side=tkinter.LEFT)

        self.reset_button = tkinter.Button(
            self.button_frame,
            text="Reset Trial",
            font=("Arial Bold", 7),
            background="yellow",
            activebackground="gold",
            foreground="black",
            width=10,
            height=15,
            command=self.reset_trial,
        )
        self.reset_button.pack(side=tkinter.RIGHT, padx=(10, 0))

        self.button_frame.pack(pady=(40, 0))

    def create_progress_frame(self):
        """Create the frame for progress display."""
        self.progress_frame = tkinter.Frame(self.window, background=BACKGROUND_COLOR)

        # Cluster Label
        self.current_cluster_label = tkinter.Label(
            self.progress_frame,
            text=f"Current Cluster: {DataMedium.cluster_order[0]}",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.current_cluster_label.pack(pady=(10, 0))

        # Piece Label
        self.current_piece_label = tkinter.Label(
            self.progress_frame,
            text="Placed Pieces: 0",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.current_piece_label.pack(pady=(10, 0))

        self.progress_frame.pack(pady=(0, 10))

    def start_trial(self, event=None):
        """Start a trial."""
        # Change the button
        self.start_button.config(state="disabled", background="light gray")
        self.stop_button.config(state="normal", background="red")
        self.current_cluster_label.config(
            text=f"Current Cluster: {DataMedium.cluster_order[WindowData.num_placed_clusters]}"
        )
        self.current_piece_label.config(text="Placed Pieces: 0")
        WindowData.is_in_trial = True

    def stop_trial(self):
        """Stop a trial."""
        # Save snapshot
        self.save_snapshot(DataMedium.cluster_order[WindowData.num_placed_clusters])

        # Change cluster
        WindowData.num_placed_clusters += 1

        if WindowData.num_placed_clusters < DataMedium.num_clusters:
            WindowData.piece_num = 1

            # Change the button
            self.start_button.config(state="normal", background="green")
            self.stop_button.config(state="disabled", background="light gray")

        # Move on to errors
        else:
            self.start_button.config(state="disabled", background="light gray")
            self.stop_button.config(state="disabled", background="light gray")

            DataMedium.is_trials_complete = True
            self.close()

        WindowData.is_in_trial = False

    def mark_date(self):
        """Mark the date in a trial."""
        # Return if there is not a trial ongoing
        if WindowData.is_in_trial is False:
            return

        WindowData.piece_num += 1

        DataMedium.cluster_times[WindowData.num_placed_clusters].append(datetime.now())
        self.current_cluster_label.config(
            text=f"Current Cluster: {DataMedium.cluster_order[WindowData.num_placed_clusters]}"
        )
        self.current_piece_label.config(
            text=f"Placed Pieces: {WindowData.piece_num - 1}"
        )

    def reset_trial(self, event=None):
        """Reset the date in a trial."""
        # Return if there is not a trial ongoing
        if WindowData.is_in_trial is False:
            return

        DataMedium.cluster_times[WindowData.num_placed_clusters] = []
        self.current_piece_label.config(text="Placed Pieces: 0")

        WindowData.piece_num = 1

    def start(self):
        """Start the window main loop."""
        self.window.mainloop()

    def close(self):
        """Handle closing the window."""
        # Check closing type
        if DataMedium.is_trials_complete is False:
            res = tkinter.messagebox.askyesnocancel(
                "Exit Program", "Do you want to save the current data?"
            )
            if res is None:
                return
            elif res is False:
                self.window.quit()
                return
            else:
                DataMedium.is_trials_complete = True

        # Wait for main to finish writing to the file
        while DataMedium.is_finished_main is False:
            pass

        self.window.quit()
