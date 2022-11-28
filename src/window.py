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
        self.init_menu()

    def init_menu(self):
        """Initialize the menu."""
        self.create_menu_header()
        self.create_menu_buttons()

    def create_menu_header(self):
        """Create the menu header."""
        self.menu_header_frame = tkinter.Frame(
            self.window, pady=10, background=BACKGROUND_COLOR
        )

        self.menu_title_label = tkinter.Label(
            self.menu_header_frame,
            text="Cluster Tracking",
            font=("Times New Roman", 40),
            background=BACKGROUND_COLOR,
        )
        self.menu_title_label.pack()

        self.menu_subtitle_label = tkinter.Label(
            self.menu_header_frame,
            text="Choose which type of experiment you will be running",
            font=("Times New Roman", 15),
            background=BACKGROUND_COLOR,
        )
        self.menu_subtitle_label.pack(pady=(30, 0))

        self.menu_header_frame.pack()

    def create_menu_buttons(self):
        """Create the cluster options."""
        self.menu_button_frame = tkinter.Frame(self.window, background=BACKGROUND_COLOR)

        self.sorting_button = tkinter.Button(
            self.menu_button_frame,
            text="Sorting\nOnly",
            font=("Arial Bold", 10),
            background="light green",
            activebackground="green",
            foreground="black",
            width=10,
            height=5,
            state="normal",
            command=self.menu_only_sorting,
        )
        self.sorting_button.pack(side=tkinter.LEFT, padx=(0, 10))

        self.both_button = tkinter.Button(
            self.menu_button_frame,
            text="Both",
            font=("Arial Bold", 10),
            background="light green",
            activebackground="green",
            foreground="black",
            width=10,
            height=5,
            state="normal",
            command=self.menu_both,
        )
        self.both_button.pack(side=tkinter.RIGHT, padx=(10, 0))

        self.placing_button = tkinter.Button(
            self.menu_button_frame,
            text="Placing\nOnly",
            font=("Arial Bold", 10),
            background="light green",
            activebackground="green",
            foreground="black",
            width=10,
            height=5,
            state="normal",
            command=self.menu_only_placing,
        )
        self.placing_button.pack(padx=(10, 10))

        self.menu_button_frame.pack(pady=(10, 0))

    def menu_only_sorting(self, event=None):
        """Set only sorting."""
        DataMedium.is_only_sorting = True
        self.init_main()

    def menu_only_placing(self, event=None):
        """Set only placing."""
        DataMedium.is_only_placing = True
        self.init_main()

    def menu_both(self, event=None):
        """Set both."""
        self.init_main()

    def init_main(self):
        """Initialize the main window."""
        # Delete the menu
        for widget in self.window.winfo_children():
            widget.destroy()

        # Create the main
        self.create_header_frame()
        self.create_input_frame()
        self.create_button_frame()
        self.create_progress_frame()
        self.create_errors_frame()

    def create_window(self):
        """Create and initialize the close frame."""
        self.window = tkinter.Tk()
        self.window.title("Cluster Tracking")
        self.window.geometry("500x800")
        self.window.configure(background=BACKGROUND_COLOR)
        self.window.iconphoto(
            False, tkinter.PhotoImage(file=resource_path("TheTab_KGrgb_72ppi.png"))
        )

        self.window.bind("<Control_L>", self.mark_date)
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
        self.file_input = tkinter.StringVar()
        self.file_entry = tkinter.Entry(
            self.input_frame,
            textvariable=self.file_input,
            font=("Arial", 12),
        )
        self.file_entry.focus_set()
        self.file_label.pack()
        self.file_entry.pack(pady=(0, 10))

        # Sorting
        self.sorting_label = tkinter.Label(
            self.input_frame,
            text="Sorting Clusters:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.sorting_input = tkinter.StringVar()
        self.sorting_entry = tkinter.Entry(
            self.input_frame,
            textvariable=self.sorting_input,
            font=("Arial", 12),
        )

        if DataMedium.is_only_placing is False:
            self.sorting_label.pack()
            self.sorting_entry.pack(pady=(0, 10))

        # Placing
        self.placing_label = tkinter.Label(
            self.input_frame,
            text="Placing Clusters:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.placing_input = tkinter.StringVar()
        self.placing_entry = tkinter.Entry(
            self.input_frame,
            textvariable=self.placing_input,
            font=("Arial", 12),
        )

        if DataMedium.is_only_sorting is False:
            self.placing_label.pack()
            self.placing_entry.pack(pady=(0, 10))

        # Cluster Order
        self.cluster_order_label = tkinter.Label(
            self.input_frame,
            text="Cluster Order:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.cluster_order_input = tkinter.StringVar()
        self.cluster_order_entry = tkinter.Entry(
            self.input_frame,
            textvariable=self.cluster_order_input,
            font=("Arial", 12),
        )
        self.cluster_order_label.pack()
        self.cluster_order_entry.pack(pady=(0, 10))

        # Asc/Desc
        self.piece_order_label = tkinter.Label(
            self.input_frame,
            text="Ascending / Descending",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.piece_order_input = tkinter.StringVar()
        self.piece_order_entry = tkinter.Entry(
            self.input_frame,
            textvariable=self.piece_order_input,
            font=("Arial", 12),
        )
        self.piece_order_label.pack()
        self.piece_order_entry.pack(pady=(0, 10))

        # Enter Button
        self.input_button = tkinter.Button(
            self.input_frame,
            text="Set Input",
            font=("Arial Bold", 10),
            command=self.set_input,
        )
        self.input_button.pack(pady=(10, 0))

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
            background="light gray",
            activebackground="dark green",
            foreground="black",
            width=20,
            height=10,
            state="disabled",
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
            text="",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.current_cluster_label.pack(pady=(10, 0))

        # Piece Label
        self.current_piece_label = tkinter.Label(
            self.progress_frame,
            text="",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.current_piece_label.pack(pady=(10, 0))

        self.progress_frame.pack(pady=(0, 10))

    def create_errors_frame(self):
        """Create the frame for errors."""
        self.errors_frame = tkinter.Frame(self.window, background=BACKGROUND_COLOR)

        # Create the frames
        self.errors_input_frame = tkinter.Frame(
            self.errors_frame, background=BACKGROUND_COLOR
        )
        if DataMedium.is_only_placing is False:
            self.create_sorting_errors_frame()
        if DataMedium.is_only_sorting is False:
            self.create_placing_errors_frame()
        self.errors_input_frame.pack()

        # Pack the frames
        # NOTE - This is to temporarily disable the placing errors
        """
        if DataMedium.is_only_sorting is False and DataMedium.is_only_placing is False:
            self.sorting_errors_frame.pack(side=tkinter.LEFT, padx=(0, 10))
            self.placing_errors_frame.pack(side=tkinter.RIGHT, padx=(10, 0))

        elif DataMedium.is_only_sorting is True:
            self.sorting_errors_frame.pack()
        elif DataMedium.is_only_placing is True:
            self.placing_errors_frame.pack()
        """
        if DataMedium.is_only_placing is False:
            self.sorting_errors_frame.pack()

        # Enter Button
        self.error_input_button = tkinter.Button(
            self.errors_frame,
            text="Submit Errors",
            font=("Arial Bold", 10),
            command=self.submit_errors,
            state="disabled",
        )

        # NOTE - This if statement is to temporarily disable the placing errors
        if DataMedium.is_only_placing is False:
            self.error_input_button.pack(pady=(0, 10))

        self.errors_frame.pack()

    def create_sorting_errors_frame(self):
        """Create the frame for sorting errors."""
        self.sorting_errors_frame = tkinter.Frame(
            self.errors_input_frame, background=BACKGROUND_COLOR
        )

        # Missorted
        self.missorted_frame = tkinter.Frame(
            self.sorting_errors_frame, background=BACKGROUND_COLOR
        )
        self.missorted_label = tkinter.Label(
            self.missorted_frame,
            text="Missorted:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.missorted_label.pack(side=tkinter.LEFT)

        self.missorted_input = tkinter.StringVar()
        self.missorted_entry = tkinter.Entry(
            self.missorted_frame,
            textvariable=self.missorted_input,
            font=("Arial", 12),
            state="disabled",
            width=5,
        )
        self.missorted_entry.pack(side=tkinter.RIGHT)

        self.missorted_frame.pack(pady=(0, 10))

        # Unsorted
        self.unsorted_frame = tkinter.Frame(
            self.sorting_errors_frame, background=BACKGROUND_COLOR
        )
        self.unsorted_label = tkinter.Label(
            self.unsorted_frame,
            text="Unsorted:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.unsorted_label.pack(side=tkinter.LEFT)

        self.unsorted_input = tkinter.StringVar()
        self.unsorted_entry = tkinter.Entry(
            self.unsorted_frame,
            textvariable=self.unsorted_input,
            font=("Arial", 12),
            state="disabled",
            width=5,
        )
        self.unsorted_entry.pack(side=tkinter.RIGHT)

        self.unsorted_frame.pack(pady=(0, 10))

    def create_placing_errors_frame(self):
        """Create the frame for placing errors."""
        self.placing_errors_frame = tkinter.Frame(
            self.errors_input_frame, background=BACKGROUND_COLOR
        )

        # Missorted
        self.misplaced_frame = tkinter.Frame(
            self.placing_errors_frame, background=BACKGROUND_COLOR
        )
        self.misplaced_label = tkinter.Label(
            self.misplaced_frame,
            text="Misplaced:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.misplaced_label.pack(side=tkinter.LEFT)

        self.misplaced_input = tkinter.StringVar()
        self.misplaced_entry = tkinter.Entry(
            self.misplaced_frame,
            textvariable=self.misplaced_input,
            font=("Arial", 12),
            state="disabled",
            width=5,
        )
        self.misplaced_entry.pack(side=tkinter.RIGHT)

        self.misplaced_frame.pack(pady=(0, 10))

        # Unsorted
        self.unplaced_frame = tkinter.Frame(
            self.placing_errors_frame, background=BACKGROUND_COLOR
        )
        self.unplaced_label = tkinter.Label(
            self.unplaced_frame,
            text="Unplaced:",
            font=("Arial Bold", 12),
            background=BACKGROUND_COLOR,
        )
        self.unplaced_label.pack(side=tkinter.LEFT)

        self.unplaced_input = tkinter.StringVar()
        self.unplaced_entry = tkinter.Entry(
            self.unplaced_frame,
            textvariable=self.unplaced_input,
            font=("Arial", 12),
            state="disabled",
            width=5,
        )
        self.unplaced_entry.pack(side=tkinter.RIGHT)

        self.unplaced_frame.pack(pady=(0, 10))

    def set_input(self, event=None):
        """Check and set the cluster numbers."""
        # Get the input
        file_input = self.file_input.get()
        sorting_input = self.sorting_input.get()
        placing_input = self.placing_input.get()
        cluster_order: str = self.cluster_order_input.get()
        piece_order = self.piece_order_input.get()

        # Ensure that a file name was entered
        if len(file_input) == 0:
            tkinter.messagebox.showwarning("Wait!", "Please provide a file name.")
            self.file_entry.focus_set()
            return

        # Add the extension
        if file_input.endswith(".csv") is False:
            file_input += ".csv"

        # Parse the clusters input
        try:
            # Set 0 if there are no sorting
            if DataMedium.is_only_placing:
                num_sorting_clusters = 0
            else:
                num_sorting_clusters = int(sorting_input)

            # Set 0 if there are no placing
            if DataMedium.is_only_sorting:
                num_placing_clusters = 0
            else:
                num_placing_clusters = int(placing_input)

            # Check for valid input
            if (num_sorting_clusters < 0 or num_placing_clusters < 0) or (
                num_sorting_clusters == 0 and num_placing_clusters == 0
            ):
                raise ValueError

        except ValueError:
            tkinter.messagebox.showwarning(
                "Wait!", "Please enter a whole number for the clusters."
            )
            self.sorting_input.set("")
            self.placing_input.set("")
            self.sorting_entry.focus_set()
            return

        # Check cluster order
        if len(cluster_order) != num_placing_clusters:
            tkinter.messagebox.showwarning(
                "Wait!",
                "Please enter a cluster order with the same number of clusters as indicated.",
            )
            self.cluster_order_entry.focus_set()
            return

        # Check piece order
        if len(piece_order) == 0 or piece_order.lower()[0] not in ["a", "d"]:
            tkinter.messagebox.showwarning(
                "Wait!", 'Please enter a piece order of "ascending" or "descending".'
            )
            self.piece_order_entry.focus_set()
            return

        DataMedium.set_input(
            file_input,
            num_sorting_clusters,
            num_placing_clusters,
            cluster_order,
            piece_order,
        )

        # Configure widgets as necessary
        self.sorting_label.config(text=f"Sorting Clusters: {num_sorting_clusters}")
        self.placing_label.config(text=f"Placing Clusters: {num_placing_clusters}")

        # Disable input
        self.file_entry.config(state="disabled")
        self.sorting_entry.config(state="disabled")
        self.placing_entry.config(state="disabled")
        self.input_button.config(state="disabled")

        # Button
        self.start_button.config(state="normal", background="green")

        # Progress label text
        if WindowData.is_on_sorting():
            self.current_cluster_label.config(text="Sorting Cluster 1")
            self.current_piece_label.config(text="Sorted Pieces: 0")
        else:
            self.current_cluster_label.config(text="Placing Cluster 1")
            self.current_piece_label.config(text="Placed Pieces: 0")

    def submit_errors(self, event=None):
        """Check and set the errors."""
        # Get the input
        missorted_input = 0
        unsorted_input = 0
        misplaced_input = 0
        unplaced_input = 0

        if DataMedium.is_only_placing is False:
            missorted_input = self.missorted_input.get()
            unsorted_input = self.unsorted_input.get()

        # NOTE - This is to temporarily disable the placing errors
        """
        if DataMedium.is_only_sorting is False:
            misplaced_input = self.misplaced_input.get()
            unplaced_input = self.unplaced_input.get()
        """

        # Parse the clusters input
        try:

            missorted = int(missorted_input)
            unsorted = int(unsorted_input)
            misplaced = int(misplaced_input)
            unplaced = int(unplaced_input)

            # Check for valid input
            if missorted < 0 or unsorted < 0 or misplaced < 0 or unplaced < 0:
                raise ValueError

        except ValueError:
            tkinter.messagebox.showwarning(
                "Wait!", "Please enter a whole number for the errors."
            )
            self.missorted_input.set("")
            self.unsorted_input.set("")
            self.misplaced_input.set("")
            self.unplaced_input.set("")
            self.missorted_entry.focus_set()
            return

        # Send the values
        DataMedium.num_missorted = missorted
        DataMedium.num_unsorted = unsorted
        DataMedium.num_misplaced = misplaced
        DataMedium.num_unplaced = unplaced
        self.close()

    def start_trial(self, event=None):
        """Start a trial."""
        # Change the button
        self.start_button.config(state="disabled", background="light gray")
        self.stop_button.config(state="normal", background="red")
        WindowData.is_in_trial = True

    def stop_trial(self):
        """Stop a trial."""
        # Determine if this is a sorting or placing trial
        if WindowData.is_on_sorting():

            WindowData.num_sorted_clusters += 1
            WindowData.piece_num = 1

            # Change the button names
            if WindowData.is_on_sorting():
                self.current_cluster_label.config(
                    text=f"Sorting Cluster {WindowData.num_sorted_clusters + 1}"
                )
                self.current_piece_label.config(text="Sorted Pieces: 0")

            # Move to the placing clusters
            elif WindowData.is_on_placing():
                self.current_cluster_label.config(text="Placing Cluster 1")
                self.current_piece_label.config(text="Placed Pieces: 0")

            # No placing clusters, move on to errors
            else:
                self.start_button.config(state="disabled", background="light gray")
                self.stop_button.config(state="disabled", background="light gray")

                if DataMedium.is_only_placing is False:
                    self.missorted_entry.config(state="normal")
                    self.unsorted_entry.config(state="normal")
                if DataMedium.is_only_sorting is False:
                    self.misplaced_entry.config(state="normal")
                    self.unplaced_entry.config(state="normal")

                self.error_input_button.config(state="normal")
                return

        elif WindowData.is_on_placing():

            WindowData.num_placed_clusters += 1
            WindowData.piece_num = 1

            # Change the button names
            if WindowData.is_on_placing():
                self.current_cluster_label.config(
                    text=f"Placing Cluster {WindowData.num_placed_clusters + 1}"
                )
                self.current_piece_label.config(text="Placed Pieces: 0")

            # Move on to errors
            else:
                self.start_button.config(state="disabled", background="light gray")
                self.stop_button.config(state="disabled", background="light gray")

                if DataMedium.is_only_placing is False:
                    self.missorted_entry.config(state="normal")
                    self.unsorted_entry.config(state="normal")

                # NOTE - This is to temporarily disable the placing errors
                """
                if DataMedium.is_only_sorting is False:
                    self.misplaced_entry.config(state="normal")
                    self.unplaced_entry.config(state="normal")
                """
                if DataMedium.is_only_placing is True:
                    self.close()

                self.error_input_button.config(state="normal")
                return

        # Change the button
        self.start_button.config(state="normal", background="green")
        self.stop_button.config(state="disabled", background="light gray")
        WindowData.is_in_trial = False

    def mark_date(self, event=None):
        """Mark the date in a trial."""
        # Return if there is not a trial ongoing
        if WindowData.is_in_trial is False:
            return

        WindowData.piece_num += 1

        # Determine if this is a sorting or placing trial
        if WindowData.is_on_sorting():

            DataMedium.sorting_clusters_times[WindowData.num_sorted_clusters].append(
                datetime.now()
            )
            self.current_piece_label.config(
                text=f"Sorted Pieces: {WindowData.piece_num - 1}"
            )

        elif WindowData.is_on_placing():

            DataMedium.placing_clusters_times[WindowData.num_placed_clusters].append(
                datetime.now()
            )
            self.current_piece_label.config(
                text=f"Placed Pieces: {WindowData.piece_num - 1}"
            )

    def reset_trial(self, event=None):
        """Reset the date in a trial."""
        # Return if there is not a trial ongoing
        if WindowData.is_in_trial is False:
            return

        # Determine if this is a sorting or placing trial
        if WindowData.is_on_sorting():
            DataMedium.sorting_clusters_times[WindowData.num_sorted_clusters] = []
            self.current_piece_label.config(text="Sorted Pieces: 0")

        elif WindowData.is_on_placing():
            DataMedium.placing_clusters_times[WindowData.num_placed_clusters] = []
            self.current_piece_label.config(text="Placed Pieces: 0")

        WindowData.piece_num = 1

    def start(self):
        """Start the window main loop."""
        self.window.mainloop()

    def close(self):
        """Handle closing the window."""
        # Check if no trials have started
        if DataMedium.is_input_set is False:
            self.window.quit()
            return

        # Wait for main to finish writing to the file
        DataMedium.is_trials_complete = True
        while DataMedium.is_finished_main is False:
            pass

        self.window.quit()
