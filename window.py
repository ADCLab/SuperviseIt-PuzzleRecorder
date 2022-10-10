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
        self.window.geometry("500x600")
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
        self.sorting_entry.focus_set()
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
            text="Set Clusters",
            font=("Arial Bold", 10),
        )
        self.input_button.bind("<Button-1>", self.set_clusters)
        self.input_button.bind("<Return>", self.set_clusters)
        self.input_button.pack(pady=10)

        self.input_frame.pack()

    def create_button_frame(self):
        """Create the frame for cluster input."""
        self.button_frame = tkinter.Frame(self.window, background=BACKGROUND_COLOR)

        # Cluster Label
        self.current_cluster_label = tkinter.Label(
            self.button_frame,
            text="",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.current_cluster_label.pack(pady=(0, 10))

        # Start Button
        self.start_button = tkinter.Button(
            self.button_frame,
            text="Start",
            font=("Arial Bold", 10),
            background="cyan",
            activebackground="cyan",
            foreground="black",
            width=20,
            height=10,
            state="disabled",
        )
        self.start_button.bind("<Button-1>", self.start_trial)
        self.start_button.bind("<Return>", self.start_trial)
        self.start_button.pack(side=tkinter.LEFT, padx=(0, 20))

        # Stop Button
        self.stop_button = tkinter.Button(
            self.button_frame,
            text="Stop",
            font=("Arial Bold", 10),
            background="cyan",
            foreground="black",
            width=20,
            height=10,
            state="disabled",
        )
        self.stop_button.bind("<Button-1>", self.stop_trial)
        self.stop_button.bind("<Return>", self.stop_trial)
        self.stop_button.pack(side=tkinter.RIGHT, padx=(20, 0))

        self.button_frame.pack(pady=(40, 0))

    def set_clusters(self, event=None):
        """Check and set the cluster numbers."""
        # Get the input
        sorting_input = self.sorting_input.get()
        placing_input = self.placing_input.get()

        # Parse the input
        try:
            num_sorting_clusters = int(sorting_input)
            num_placing_clusters = int(placing_input)

            if num_sorting_clusters < 1 or num_placing_clusters < 1:
                raise ValueError

        except ValueError:
            tkinter.messagebox.showwarning("Wait!", "Please enter a whole number.")
            self.sorting_input.set("")
            self.placing_input.set("")
            self.sorting_entry.focus_set()
            return

        DataMedium.set_clusters(num_sorting_clusters, num_placing_clusters)

        # Configure widgets as necessary
        self.sorting_label.config(text=f"Sorting Clusters: {num_sorting_clusters}")
        self.placing_label.config(text=f"Placing Clusters: {num_placing_clusters}")
        self.current_cluster_label.config(text="Sorting Cluster 1")

        self.sorting_entry.config(state="disabled")
        self.placing_entry.config(state="disabled")
        self.input_button.config(state="disabled")
        self.start_button.config(state="normal")

    def start_trial(self, event=None):
        """Start a trial."""
        # Configure buttons
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_trial(self, event=None):
        """Stop a trial."""
        # Determine if this is a sorting or placing trial
        if DataMedium.is_on_sorting():

            DataMedium.num_sorted_clusters += 1
            self.start_button.config(state="normal")

            # Change the button names
            if DataMedium.is_on_sorting():
                self.current_cluster_label.config(
                    text=f"Sorting Cluster {DataMedium.num_sorted_clusters + 1}"
                )
            else:
                self.current_cluster_label.config(text="Placing Cluster 1")

        elif DataMedium.is_on_placing():

            DataMedium.num_placed_clusters += 1
            self.start_button.config(state="normal")

            # Change the button names
            if DataMedium.is_on_placing():
                self.current_cluster_label.config(
                    text=f"Placing Cluster {DataMedium.num_placed_clusters + 1}"
                )

        self.stop_button.config(state="disabled")

    def mark_date(self, event=None):
        """Mark the date in a trial."""
        # Return if there is not a trial ongoing
        if self.start_button["state"] == "normal":
            return

        # Determine if this is a sorting or placing trial
        if DataMedium.is_on_sorting():

            DataMedium.sorting_clusters_times[DataMedium.num_sorted_clusters].append(
                datetime.now()
            )

        elif DataMedium.is_on_placing():

            DataMedium.placing_clusters_times[DataMedium.num_placed_clusters].append(
                datetime.now()
            )

    def start(self):
        """Start the window main loop."""
        self.window.mainloop()

    def on_closing(self):
        """Handle closing the window."""
        self.window.quit()
