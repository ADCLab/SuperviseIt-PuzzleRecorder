"""The Window for the GUI."""

import tkinter
import tkinter.messagebox
from datetime import datetime

from utils import DataMedium

BACKGROUND_COLOR = "gray"


class Window:
    """The GUI Window."""

    def __init__(self):
        """Initialize the window."""
        self.create_window()
        self.create_header_frame()
        self.create_input_frame()
        self.create_button_frame()

    def create_window(self):
        """Create and initialize the close frame."""
        self.window = tkinter.Tk()
        self.window.title("Cluster Tracking")
        self.window.geometry("500x650")
        self.window.configure(background=BACKGROUND_COLOR)
        self.window.iconphoto(False, tkinter.PhotoImage(file="TheTab_KGrgb_72ppi.png"))

        self.window.bind("<Control_L>", self.mark_date)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

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
            text="File:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.file_label.pack()

        self.file_input = tkinter.StringVar()
        self.file_entry = tkinter.Entry(
            self.input_frame,
            textvariable=self.file_input,
            font=("Arial", 12),
        )
        self.file_entry.focus_set()
        self.file_entry.pack(pady=(0, 10))

        # Sorting
        self.sorting_label = tkinter.Label(
            self.input_frame,
            text="Sorting Clusters:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.sorting_label.pack()

        self.sorting_input = tkinter.StringVar()
        self.sorting_entry = tkinter.Entry(
            self.input_frame,
            textvariable=self.sorting_input,
            font=("Arial", 12),
        )
        self.sorting_entry.pack(pady=(0, 10))

        # Placing
        self.placing_label = tkinter.Label(
            self.input_frame,
            text="Placing Clusters:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.placing_label.pack()

        self.placing_input = tkinter.StringVar()
        self.placing_entry = tkinter.Entry(
            self.input_frame,
            textvariable=self.placing_input,
            font=("Arial", 12),
        )
        self.placing_entry.pack(pady=(0, 10))

        # Enter Button
        self.input_button = tkinter.Button(
            self.input_frame,
            text="Set Input",
            font=("Arial Bold", 10),
        )
        self.input_button.bind("<Button-1>", self.set_input)
        self.input_button.bind("<Return>", self.set_input)
        self.input_button.pack(pady=10)

        self.input_frame.pack()

    def create_button_frame(self):
        """Create the frame for cluster input."""
        self.button_frame = tkinter.Frame(self.window, background=BACKGROUND_COLOR)

        # Trial Button
        self.trial_button = tkinter.Button(
            self.button_frame,
            text="Start",
            font=("Arial Bold", 10),
            background="light gray",
            foreground="black",
            width=20,
            height=10,
            state="disabled",
        )
        self.trial_button.bind("<Button-1>", self.trial)
        self.trial_button.bind("<Return>", self.trial)
        self.trial_button.pack()

        # Cluster Label
        self.current_cluster_label = tkinter.Label(
            self.button_frame,
            text="",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.current_cluster_label.pack(pady=(10, 0))

        # Piece Label
        self.current_piece_label = tkinter.Label(
            self.button_frame,
            text="",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.current_piece_label.pack(pady=(10, 0))

        self.button_frame.pack(pady=(40, 0))

    def set_input(self, event=None):
        """Check and set the cluster numbers."""
        # Get the input
        file_input = self.file_input.get()
        sorting_input = self.sorting_input.get()
        placing_input = self.placing_input.get()

        # Parse the file input
        if file_input.endswith(".csv") is False:
            tkinter.messagebox.showwarning(
                "Wait!", 'Please enter a file name ending in ".csv".'
            )
            self.file_input.set("")
            self.sorting_input.set("")
            self.placing_input.set("")
            self.file_entry.focus_set()
            return

        # Parse the clusters input
        try:
            num_sorting_clusters = int(sorting_input)
            num_placing_clusters = int(placing_input)

            if num_sorting_clusters < 1 or num_placing_clusters < 1:
                raise ValueError

        except ValueError:
            tkinter.messagebox.showwarning(
                "Wait!", "Please enter a whole number for the clusters."
            )
            self.file_input.set("")
            self.sorting_input.set("")
            self.placing_input.set("")
            self.file_entry.focus_set()
            return

        DataMedium.set_input(file_input, num_sorting_clusters, num_placing_clusters)

        # Configure widgets as necessary
        self.sorting_label.config(text=f"Sorting Clusters: {num_sorting_clusters}")
        self.placing_label.config(text=f"Placing Clusters: {num_placing_clusters}")
        self.current_cluster_label.config(text="Sorting Cluster 1")
        self.current_piece_label.config(text="Sorted Pieces: 0")

        self.file_entry.config(state="disabled")
        self.sorting_entry.config(state="disabled")
        self.placing_entry.config(state="disabled")
        self.input_button.config(state="disabled")
        self.trial_button.config(state="normal", background="green", activebackground="dark green")

    def trial(self, event=None):
        """Change the trial state."""
        # Check if the trial is ongoing
        if DataMedium.is_in_trial is False:

            # Change the button
            self.trial_button.config(text="Stop", background="red", activebackground="dark red")
            DataMedium.is_in_trial = True

        else:

            # Change the button
            self.trial_button.config(text="Start", background="green", activebackground="dark green")
            DataMedium.is_in_trial = False

            self.stop_trial()

    def stop_trial(self):
        """Stop a trial."""
        # Determine if this is a sorting or placing trial
        if DataMedium.is_on_sorting():

            DataMedium.num_sorted_clusters += 1
            DataMedium.piece_num = 1

            # Change the button names
            if DataMedium.is_on_sorting():
                self.current_cluster_label.config(
                    text=f"Sorting Cluster {DataMedium.num_sorted_clusters + 1}"
                )
                self.current_piece_label.config(text="Sorted Pieces: 0")
            else:
                self.current_cluster_label.config(text="Placing Cluster 1")
                self.current_piece_label.config(text="Placed Pieces: 0")

        elif DataMedium.is_on_placing():

            DataMedium.num_placed_clusters += 1
            DataMedium.piece_num = 1

            # Change the button names
            if DataMedium.is_on_placing():
                self.current_cluster_label.config(
                    text=f"Placing Cluster {DataMedium.num_placed_clusters + 1}"
                )
                self.current_piece_label.config(text="Placed Pieces: 0")

    def mark_date(self, event=None):
        """Mark the date in a trial."""
        # Return if there is not a trial ongoing
        if DataMedium.is_in_trial is False:
            return

        DataMedium.piece_num += 1

        # Determine if this is a sorting or placing trial
        if DataMedium.is_on_sorting():

            DataMedium.sorting_clusters_times[DataMedium.num_sorted_clusters].append(
                datetime.now()
            )
            self.current_piece_label.config(text=f"Sorted Pieces: {DataMedium.piece_num - 1}")

        elif DataMedium.is_on_placing():

            DataMedium.placing_clusters_times[DataMedium.num_placed_clusters].append(
                datetime.now()
            )
            self.current_piece_label.config(text=f"Placed Pieces: {DataMedium.piece_num - 1}")

    def start(self):
        """Start the window main loop."""
        self.window.mainloop()

    def on_closing(self):
        """Handle closing the window."""
        self.window.quit()
