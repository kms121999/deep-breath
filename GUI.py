import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
from setting_management.SettingClient import SettingClient
import asyncio

class SettingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Settings GUI")
        self.client = SettingClient()

        # Initialize settings dictionary (will be fetched from SettingClient)
        self.settings = None

        # Create a Notebook to hold different pages
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Create main settings page
        self.create_settings_page()
        
        # Create process management page
        self.create_process_management_page()

        # Fetch settings from the server asynchronously
        self.root.after(0, self.fetch_settings)

    def create_settings_page(self):
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="General Settings")

        # Interaction intensity
        self.intensity_label = tk.Label(self.settings_frame, text="Interaction Intensity:")
        self.intensity_label.pack(pady=5)
        self.intensity_scale = tk.Scale(self.settings_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.intensity_scale.pack(pady=5)

        # Notification frequency (minutes)
        self.notif_freq_label = tk.Label(self.settings_frame, text="Notification Frequency (minutes):")
        self.notif_freq_label.pack(pady=5)
        self.notif_freq_entry = tk.Entry(self.settings_frame)
        self.notif_freq_entry.pack(pady=5)

        # Quotes (True/False)
        self.quotes_label = tk.Label(self.settings_frame, text="Enable Quotes:")
        self.quotes_label.pack(pady=5)
        self.quotes_var = tk.BooleanVar()
        self.quotes_check = tk.Checkbutton(self.settings_frame, text="Quotes", variable=self.quotes_var)
        self.quotes_check.pack(pady=5)

        # Goals (True/False)
        self.goals_label = tk.Label(self.settings_frame, text="Enable Goals:")
        self.goals_label.pack(pady=5)
        self.goals_var = tk.BooleanVar()
        self.goals_check = tk.Checkbutton(self.settings_frame, text="Goals", variable=self.goals_var)
        self.goals_check.pack(pady=5)

        # Default warning time (minutes)
        self.warning_time_label = tk.Label(self.settings_frame, text="Default Warning Time (minutes):")
        self.warning_time_label.pack(pady=5)
        self.warning_time_entry = tk.Entry(self.settings_frame)
        self.warning_time_entry.pack(pady=5)

        # Reset times (hour and day)
        self.reset_time_label = tk.Label(self.settings_frame, text="Reset Time (Hour of day):")
        self.reset_time_label.pack(pady=5)
        self.reset_time_entry = tk.Entry(self.settings_frame)
        self.reset_time_entry.pack(pady=5)

        self.reset_day_label = tk.Label(self.settings_frame, text="Reset Day (0=Sunday, 6=Saturday):")
        self.reset_day_label.pack(pady=5)
        self.reset_day_entry = tk.Entry(self.settings_frame)
        self.reset_day_entry.pack(pady=5)

        # Submit button
        self.submit_button = tk.Button(self.settings_frame, text="Submit Settings", command=self.submit_settings)
        self.submit_button.pack(pady=10)

    def create_process_management_page(self):
        self.process_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.process_frame, text="Process Management")

        self.process_listbox = tk.Listbox(self.process_frame)
        self.process_listbox.pack(expand=True, fill='both', padx=10, pady=10)

        self.add_process_button = tk.Button(self.process_frame, text="Add Process", command=self.add_process)
        self.add_process_button.pack(pady=5)

        self.edit_process_button = tk.Button(self.process_frame, text="Edit Process", command=self.edit_process)
        self.edit_process_button.pack(pady=5)

    def fetch_settings(self):
        async def get_settings():
            def callback(received_settings, error=None):
                if error:
                    print(f"Failed to fetch settings: {error}")
                else:
                    self.settings = received_settings
                    self.populate_fields()

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
        # Open file dialog to select an executable
        exe_file = filedialog.askopenfilename(title="Select Executable", filetypes=[("Executable Files", "*.exe")])
        if exe_file:
            # Prompt for a custom label
            title = simpledialog.askstring("Process Title", "Enter a title for the process:")
            if title:
                # Add the process to the listbox
                self.process_listbox.insert(tk.END, f"{title} - {exe_file}")
                # Here, you might also want to save the process to your data structure or database

    def edit_process(self):
        selected_index = self.process_listbox.curselection()
        if selected_index:
            selected_process = self.process_listbox.get(selected_index)
            parts = selected_process.split(" - ")
            if len(parts) == 2:
                title, exe_file = parts
                # Prompt for a new title
                new_title = simpledialog.askstring("Edit Process Title", "Edit the title for the process:", initialvalue=title)
                if new_title:
                    # Update the listbox with the new title
                    self.process_listbox.delete(selected_index)
                    self.process_listbox.insert(selected_index, f"{new_title} - {exe_file}")
                    # Here, you might also want to save the updated process to your data structure or database
        else:
            messagebox.showwarning("Selection Error", "Please select a process to edit.")

# Run the application
if __name__ == "__main__":
    from setting_management.SettingServer import SettingServer
    from setting_management.SettingManager import SettingManager

    # Create the SettingServer instance
    setting_manager = SettingManager()
    ws_server = SettingServer(setting_manager, host="localhost", port=8765)

    # Start the WebSocket server in a separate thread
    ws_server.start()
    print("Server started in a background thread.")

    try:
        # Main thread can do other things here (e.g., running a GUI)
        root = tk.Tk()
        app = SettingsApp(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("Stopping server...")
        ws_server.stop()
        print("Server stopped gracefully.")
