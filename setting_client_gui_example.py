import asyncio
import websockets
import pickle
import tkinter as tk
from tkinter import messagebox
from SettingClient import SettingClient

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Settings Manager")
        self.geometry("300x200")

        self.client = SettingClient()
        self.settings = {}  # Store settings retrieved from the server

        # Create UI components
        self.create_widgets()

        # Fetch current settings when the app starts
        asyncio.run(self.async_get_settings())

    def create_widgets(self):
        # Color Label
        tk.Label(self, text="Current Color:").pack(pady=10)

        # Current Color Display
        self.color_display = tk.Label(self, text="N/A")
        self.color_display.pack(pady=5)

        # New Color Label
        tk.Label(self, text="Enter new color:").pack(pady=10)

        # Color Entry
        self.color_entry = tk.Entry(self)
        self.color_entry.pack(pady=5)

        # Set Settings Button
        self.set_button = tk.Button(self, text="Set Settings", command=self.set_settings)
        self.set_button.pack(pady=5)

        # Status Label
        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=10)

    async def async_get_settings(self):
        def callback(settings, error=None):
            if error:
                self.show_error(f"Error fetching settings: {error}")
            else:
                self.settings = settings
                self.color_display.config(text=settings.get("color", "N/A"))  # Display current color

        await self.client.get_settings(callback)

    async def async_set_settings(self, color):
        updated_settings = self.settings.copy()  # Create a copy of the current settings
        updated_settings["color"] = color  # Modify only the color key

        def callback(status, error=None):
            if status:
                self.show_info("Settings updated successfully!")
                self.settings["color"] = color  # Update the local settings
                self.color_display.config(text=color)  # Update displayed color
            else:
                self.show_error(f"Failed to update settings: {error}")

        await self.client.set_settings(updated_settings, callback)

    def set_settings(self):
        color = self.color_entry.get()
        if color:
            asyncio.run(self.async_set_settings(color))
        else:
            self.show_error("Please enter a color.")

    def show_info(self, message):
        messagebox.showinfo("Info", message)

    def show_error(self, message):
        messagebox.showerror("Error", message)

if __name__ == "__main__":
    app = App()
    app.mainloop()
