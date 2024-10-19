import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, messagebox
from setting_management.SettingClient import SettingClient
from setting_management.ProcessSettings import ProcessSettings
import asyncio
import os

class SettingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Settings GUI")
        self.client = SettingClient()

        # Initialize settings dictionary (will be fetched from SettingClient)
        self.settings = None

        # Initialize process settings dictionary
        self.process_settings = {}

        # Create a notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create main settings tab
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Main Settings")

        # Create process management tab
        self.process_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.process_frame, text="Process Management")

        # Create widgets for main settings
        self.create_widgets()

        # Create widgets for process management
        self.create_process_widgets()

        # Initially fetch the settings from the server asynchronously
        self.root.after(0, self.fetch_settings)

    def create_widgets(self):
        # Use grid layout for main settings to control positioning
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)

        # Interaction intensity
        self.intensity_label = tk.Label(self.main_frame, text="Interaction Intensity:")
        self.intensity_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.intensity_scale = tk.Scale(self.main_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.intensity_scale.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # Notification frequency (minutes)
        self.notif_freq_label = tk.Label(self.main_frame, text="Notification Frequency (minutes):")
        self.notif_freq_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.notif_freq_entry = tk.Entry(self.main_frame)
        self.notif_freq_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        # Quotes (True/False)
        self.quotes_label = tk.Label(self.main_frame, text="Enable Quotes:")
        self.quotes_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.quotes_var = tk.BooleanVar()
        self.quotes_check = tk.Checkbutton(self.main_frame, text="Quotes", variable=self.quotes_var)
        self.quotes_check.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Goals (True/False)
        self.goals_label = tk.Label(self.main_frame, text="Enable Goals:")
        self.goals_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.goals_var = tk.BooleanVar()
        self.goals_check = tk.Checkbutton(self.main_frame, text="Goals", variable=self.goals_var)
        self.goals_check.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # Default warning time (minutes)
        self.warning_time_label = tk.Label(self.main_frame, text="Default Warning Time (minutes):")
        self.warning_time_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.warning_time_entry = tk.Entry(self.main_frame)
        self.warning_time_entry.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)

        # Reset times (hour and day)
        self.reset_time_label = tk.Label(self.main_frame, text="Reset Time (Hour of day):")
        self.reset_time_label.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.reset_time_entry = tk.Entry(self.main_frame)
        self.reset_time_entry.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=5)

        self.reset_day_label = tk.Label(self.main_frame, text="Reset Day (0=Monday, 6=Sunday):")
        self.reset_day_label.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.reset_day_entry = tk.Entry(self.main_frame)
        self.reset_day_entry.grid(row=6, column=1, sticky=tk.EW, padx=5, pady=5)

        # Submit button for main settings
        self.submit_button = tk.Button(self.main_frame, text="Save Changes", command=self.submit_settings)
        self.submit_button.grid(row=7, column=0, columnspan=2, pady=10)

    def create_process_widgets(self):
        # Use grid layout for process management
        self.process_frame.columnconfigure(0, weight=1)

        # Process list
        self.process_list = tk.Listbox(self.process_frame)
        self.process_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Button to add process
        self.add_process_button = tk.Button(self.process_frame, text="Add Process", command=self.add_process)
        self.add_process_button.pack(pady=5)

        # Button to delete selected process
        self.delete_process_button = tk.Button(self.process_frame, text="Delete Selected Process", command=self.delete_process)
        self.delete_process_button.pack(pady=5)

        # Bind double click to edit
        self.process_list.bind("<Double-Button-1>", self.edit_process)

        # Submit button for process management
        self.process_submit_button = tk.Button(self.process_frame, text="Save Processes", command=self.submit_processes)
        self.process_submit_button.pack(pady=5)

    def fetch_settings(self):
        async def get_settings():
            def callback(received_settings, error=None):
                if error:
                    print(f"Failed to fetch settings: {error}")
                else:
                    self.settings = received_settings
                    self.populate_fields()
                    self.populate_processes()

            await self.client.get_settings(callback)

        asyncio.run(get_settings())

    def populate_fields(self):
        if self.settings is not None:
            # Populate the form with the fetched settings
            self.intensity_scale.set(self.settings["interaction_intensity"])
            self.notif_freq_entry.insert(0, str(self.settings["notification_frequency_min"]))
            self.quotes_var.set(self.settings["quotes"])
            self.goals_var.set(self.settings["goals"])
            self.warning_time_entry.insert(0, str(self.settings["default_warning_time"]))
            self.reset_time_entry.insert(0, str(self.settings["reset_times"]["hour"]))
            self.reset_day_entry.insert(0, str(self.settings["reset_times"]["day"]))

    def populate_processes(self):
        self.process_list.delete(0, tk.END)  # Clear the current list
        self.process_settings = self.settings.get("processSettings", {})
        for key, process in self.process_settings.items():
            self.process_list.insert(tk.END, f"{process.label} - {process.executable_name}")

    def submit_settings(self):
        # Update the settings object with the values from the form
        self.settings["interaction_intensity"] = self.intensity_scale.get()
        self.settings["notification_frequency_min"] = int(self.notif_freq_entry.get())
        self.settings["quotes"] = self.quotes_var.get()
        self.settings["goals"] = self.goals_var.get()
        self.settings["default_warning_time"] = int(self.warning_time_entry.get())
        self.settings["reset_times"]["hour"] = int(self.reset_time_entry.get())
        self.settings["reset_times"]["day"] = int(self.reset_day_entry.get())

        async def update_settings():
            def callback(success, error=None):
                if success:
                    print("Settings updated successfully!")
                else:
                    print(f"Failed to update settings: {error}")

            await self.client.set_settings(self.settings, callback)

        asyncio.run(update_settings())

    def add_process(self):
        exe_file = filedialog.askopenfilename(title="Select Executable", filetypes=[("Executable Files", "*.exe")])
        if not exe_file:
            return  # User cancelled the file dialog
        
        # Get only the executable name and extension
        exe_file = os.path.basename(exe_file)

        label = simpledialog.askstring("Input", "Enter a label for the process:")
        if label is None:
            return  # User cancelled the input dialog

        process = ProcessSettings(label, exe_file)
        self.process_settings[exe_file] = process

        # Update the settings dictionary
        self.settings["processSettings"] = self.process_settings

        # Refresh the process list
        self.populate_processes()

    def edit_process(self, event):
        selected_index = self.process_list.curselection()
        if not selected_index:
            return  # No selection

        selected_process = self.process_list.get(selected_index).split(" - ")
        exe_file = selected_process[1]
        current_label = selected_process[0]

        new_label = simpledialog.askstring("Edit Process", "Enter a new label:", initialvalue=current_label)
        if new_label is None:
            return  # User cancelled the input dialog

        # Update the process settings
        process = self.process_settings[exe_file]
        process.label = new_label
        self.process_settings[exe_file] = process

        # Update the settings dictionary
        self.settings["processSettings"] = self.process_settings

        # Refresh the process list
        self.populate_processes()

    def delete_process(self):
        selected_index = self.process_list.curselection()
        if not selected_index:
            return  # No selection

        selected_process = self.process_list.get(selected_index).split(" - ")
        exe_file = selected_process[1]

        # Confirm deletion
        if messagebox.askyesno("Delete Process", f"Are you sure you want to delete '{selected_process[0]}'?"):
            del self.process_settings[exe_file]

            # Update the settings dictionary
            self.settings["processSettings"] = self.process_settings

            # Refresh the process list
            self.populate_processes()

    def submit_processes(self):
        # Update the settings dictionary with current process settings
        self.settings["processSettings"] = self.process_settings

        async def update_processes():
            def callback(success, error=None):
                if success:
                    print("Processes updated successfully!")
                else:
                    print(f"Failed to update processes: {error}")

            await self.client.set_settings(self.settings, callback)

        asyncio.run(update_processes())

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsApp(root)
    root.mainloop()