import tkinter as tk
from tkinter import ttk
from setting_management.SettingClient import SettingClient

class SettingsApp:
    def __init__(self, root):
        self.client = SettingClient()

        root.title("Settings Manager")

        # Interaction Intensity
        self.interaction_intensity_label = tk.Label(root, text="Interaction Intensity:")
        self.interaction_intensity_label.grid(row=0, column=0, padx=10, pady=5)
        self.interaction_intensity_entry = tk.Entry(root)
        self.interaction_intensity_entry.grid(row=0, column=1, padx=10, pady=5)

        # Color
        self.color_label = tk.Label(root, text="Color:")
        self.color_label.grid(row=1, column=0, padx=10, pady=5)
        self.color_var = tk.StringVar(value="red")
        self.color_dropdown = ttk.Combobox(root, textvariable=self.color_var, values=["red", "gray", "white", "black"])
        self.color_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Notification Frequency
        self.notification_label = tk.Label(root, text="Notification Frequency (min):")
        self.notification_label.grid(row=2, column=0, padx=10, pady=5)
        self.notification_entry = tk.Entry(root)
        self.notification_entry.grid(row=2, column=1, padx=10, pady=5)

        # Quotes (Boolean)
        self.quotes_var = tk.BooleanVar(value=True)
        self.quotes_checkbox = tk.Checkbutton(root, text="Quotes", variable=self.quotes_var)
        self.quotes_checkbox.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Goals (Boolean)
        self.goals_var = tk.BooleanVar(value=False)
        self.goals_checkbox = tk.Checkbutton(root, text="Goals", variable=self.goals_var)
        self.goals_checkbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Default Warning Time
        self.warning_time_label = tk.Label(root, text="Default Warning Time (min):")
        self.warning_time_label.grid(row=5, column=0, padx=10, pady=5)
        self.warning_time_entry = tk.Entry(root)
        self.warning_time_entry.grid(row=5, column=1, padx=10, pady=5)

        # Reset Times (hour/day)
        self.reset_hour_label = tk.Label(root, text="Reset Hour:")
        self.reset_hour_label.grid(row=6, column=0, padx=10, pady=5)
        self.reset_hour_entry = tk.Entry(root)
        self.reset_hour_entry.grid(row=6, column=1, padx=10, pady=5)

        self.reset_day_label = tk.Label(root, text="Reset Day:")
        self.reset_day_label.grid(row=7, column=0, padx=10, pady=5)
        self.reset_day_entry = tk.Entry(root)
        self.reset_day_entry.grid(row=7, column=1, padx=10, pady=5)

        # Submit Button
        self.submit_button = tk.Button(root, text="Submit", command=self.submit_settings)
        self.submit_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Status Label
        self.status_label = tk.Label(root, text="")
        self.status_label.grid(row=9, column=0, columnspan=2, pady=10)

        # Fetch initial settings
        root.after(100, self.load_settings)

    def load_settings(self):
        # Use SettingClient to fetch initial settings
        async def fetch_settings():
            def update_ui(settings, error=None):
                if error:
                    self.status_label.config(text="Error fetching settings.")
                else:
                    # Update UI with current settings
                    self.interaction_intensity_entry.insert(0, settings['interaction_intensity'])
                    self.color_var.set(settings['color'])
                    self.notification_entry.insert(0, settings['notification_frequency_min'])
                    self.quotes_var.set(settings['quotes'])
                    self.goals_var.set(settings['goals'])
                    self.warning_time_entry.insert(0, settings['default_warning_time'])
                    self.reset_hour_entry.insert(0, settings['reset_times']['hour'])
                    self.reset_day_entry.insert(0, settings['reset_times']['day'])

            await self.client.get_settings(update_ui)

        asyncio.run(fetch_settings())

    def submit_settings(self):
        # Collect settings from the UI
        new_settings = {
            "interaction_intensity": int(self.interaction_intensity_entry.get()),
            "color": self.color_var.get(),
            "notification_frequency_min": int(self.notification_entry.get()),
            "quotes": self.quotes_var.get(),
            "goals": self.goals_var.get(),
            "default_warning_time": int(self.warning_time_entry.get()),
            "reset_times": {
                "hour": int(self.reset_hour_entry.get()),
                "day": int(self.reset_day_entry.get())
            }
        }

        # Use SettingClient to update settings
        async def update_settings():
            def set_callback(status, error=None):
                if status:
                    self.status_label.config(text="Settings updated successfully.")
                else:
                    self.status_label.config(text=f"Failed to update settings: {error}")

            await self.client.set_settings(new_settings, set_callback)

        asyncio.run(update_settings())

# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsApp(root)
    root.mainloop()


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
        while True:
            root = tk.Tk()
            app = SettingsApp(root)
            root.mainloop()
    except KeyboardInterrupt:
        print("Stopping server...")
        ws_server.stop()
        print("Server stopped gracefully.")




DEFAULT_SETTINGS = {
    "processSettings": {

    },
    "interaction_intensity": 1,
    "color": 'red',
    "notification_frequency_min": 5,
    "quotes": True,
    "goals": False,
    "default_warning_time": 5,
    "reset_times": {
        "hour": 3,
        "day": 0
    }
}