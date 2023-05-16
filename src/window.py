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
        self.create_errors_frame()

    def create_window(self):
        """Create and initialize the close frame."""
        self.window = tkinter.Tk()
        self.window.title("Cluster Tracking")
        self.window.geometry("600x900")
        self.window.configure(background=BACKGROUND_COLOR)
        self.window.iconphoto(
            False, tkinter.PhotoImage(file=resource_path("TheTab_KGrgb_72ppi.png"))
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
        self.file_input = tkinter.StringVar(value=DataMedium.filename)
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

    def create_errors_frame(self):
        """Create the frame for errors."""
        self.errors_frame = tkinter.Frame(self.window, background=BACKGROUND_COLOR)

        # Misplaced
        self.misplaced_frame = tkinter.Frame(
            self.errors_frame, background=BACKGROUND_COLOR
        )
        self.misplaced_label = tkinter.Label(
            self.misplaced_frame,
            text="Misplaced:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.misplaced_label.pack(side=tkinter.LEFT)

        self.misplaced_input = tkinter.StringVar(value="0")
        self.misplaced_entry = tkinter.Entry(
            self.misplaced_frame,
            textvariable=self.misplaced_input,
            font=("Arial", 12),
            state="disabled",
            width=5,
        )
        self.misplaced_entry.pack(side=tkinter.RIGHT)

        self.misplaced_frame.pack(pady=(0, 10))

        # Unplaced
        self.unplaced_frame = tkinter.Frame(
            self.errors_frame, background=BACKGROUND_COLOR
        )
        self.unplaced_label = tkinter.Label(
            self.unplaced_frame,
            text="Unplaced:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.unplaced_label.pack(side=tkinter.LEFT)

        self.unplaced_input = tkinter.StringVar(value="0")
        self.unplaced_entry = tkinter.Entry(
            self.unplaced_frame,
            textvariable=self.unplaced_input,
            font=("Arial", 12),
            state="disabled",
            width=5,
        )
        self.unplaced_entry.pack(side=tkinter.RIGHT)

        self.unplaced_frame.pack(pady=(0, 10))

        # Enter Button
        self.error_input_button = tkinter.Button(
            self.errors_frame,
            text="Submit Errors",
            font=("Arial Bold", 10),
            command=self.submit_errors,
            state="disabled",
        )

        self.error_input_button.pack(pady=(0, 10))
        self.errors_frame.pack()

    def submit_errors(self, event=None):
        """Check and set the errors."""
        # Get the input
        misplaced_input = self.misplaced_input.get()
        unplaced_input = self.unplaced_input.get()

        # Parse the clusters input
        try:
            misplaced = int(misplaced_input)
            unplaced = int(unplaced_input)

            # Check for valid input
            if misplaced < 0 or unplaced < 0:
                raise ValueError

        except ValueError:
            tkinter.messagebox.showwarning(
                "Wait!", "Please enter a whole number for the errors."
            )
            self.misplaced_input.set("")
            self.unplaced_input.set("")
            self.misplaced_entry.focus_set()
            return

        # Send the values
        DataMedium.num_misplaced = misplaced
        DataMedium.num_unplaced = unplaced
        self.close()

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

            # self.close()
            self.misplaced_entry.config(state="normal")
            self.unplaced_entry.config(state="normal")
            self.error_input_button.config(state="normal")
            DataMedium.is_trials_complete = True

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

        DataMedium.placing_clusters_times[WindowData.num_placed_clusters] = []
        self.current_piece_label.config(text="Placed Pieces: 0")

        WindowData.piece_num = 1

    def start(self):
        """Start the window main loop."""
        self.window.mainloop()

    def close(self):
        """Handle closing the window."""
        # Check closing type
        if DataMedium.is_trials_complete is False:
            res = tkinter.messagebox.askquestion(
                "Exit Program", "Do you want to save the current data?"
            )
            if res == "no":
                self.window.quit()
                return

        # Wait for main to finish writing to the file
        DataMedium.is_trials_complete = True
        while DataMedium.is_finished_main is False:
            pass

        self.window.quit()
