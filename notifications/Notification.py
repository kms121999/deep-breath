from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QTimer
import tkinter as tk
import json
import random
import os
import requests
from dotenv import load_dotenv

class Notification:
    def __init__(self):
        self.alive = True
        # self.quote = self.get_random_quote() or message
        self.x1 = 10
        self.y1 = 10
        self.x2 = 300
        self.y2 = 100
        self.color = 'red'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.quotes_dir =  os.path.join(base_dir, 'quotes.json')

    def is_alive(self):
        return self.alive
    
    def get_random_quote(self):
        '''
        :fun: This will pull a quote from 
        '''
        print("Current working directory:", os.getcwd())
        with open(self.quotes_dir, 'r') as file:
            data = json.load(file)
            quotes = data['inspirational_quotes_and_goals']
            length_quotes = len(quotes) - 1
            random_index = random.randint(0, length_quotes)
            selected_quote = quotes[random_index]

        return selected_quote['quote']

    def slide_in(self, root, start_y, target_y, step=5, delay=10):
        """ Slide the window in from start_y to target_y """
        if start_y < target_y:
            root.geometry(f"+0+{start_y}")
            # Schedule the next update (increase by step)
            root.after(delay, self.slide_in, root, start_y + step, target_y)
        else:
            root.geometry(f"+0+{target_y}")  # Set to final position

    def get_quote_api(self, category):

        # Get API key from the environment
        with open("notifications/quoteninja.env", 'r') as F:
            api_key = F.read().strip()

        api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
        response = requests.get(api_url, headers={'X-Api-Key': api_key})
        
        # Check if the response is successful
        if response.status_code == requests.codes.ok:
            data = response.json()
            quote = data[0]['quote']
        else:
            quote = "Error in getting quote..."

        # Create a tkinter root window
        root = tk.Tk()
        root.title("Quote of the Day")
        root.overrideredirect(True)
        root.geometry(f"+0+20")  # Position the window

        root.attributes('-alpha', 0.8)

        # Create a label with line wrapping
        label = tk.Label(
            root, 
            text=quote, 
            font=("Arial", 12), 
            bg="black", 
            fg="white", 
            padx=10, 
            pady=5, 
            wraplength=600  # Set the wraplength in pixels (adjust as needed)
        )
        
        label.pack()

        # Start the sliding animation (move from -100 to 20 pixels down)
        self.slide_in(root, start_y=-100, target_y=20, step=5, delay=10)

        # Destroy the notification after 5 seconds
        root.after(10000, root.destroy)
        root.mainloop()



    def display_notification(self):
        '''
        :fun: This doesn't return anything, simply displays the notification.
        '''
        quote = self.get_random_quote()
        root = tk.Tk()
        root.title("Quote of the Day")
        root.overrideredirect(True)
        root.geometry(f"+0+0")
        # root.wm_attributes("-fullscreen", 1)  # Always on top
        label = tk.Label(root, text=quote, font=("Arial", 12), bg="black", fg="white", padx=10, pady=5)
        label.pack()
        root.after(5000, root.destroy)
        root.mainloop()
        #!!!!!!!!!!!!!!!
        # app = QtWidgets.QApplication([])

        # # Create the window
        # notification = QtWidgets.QWidget()
        # notification.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # notification.setGeometry(self.x1, self.y1, self.x2, self.y2)  # Set position and size
        # notification.setWindowOpacity(0.5)

        # # Customize background and label
        # notification.setStyleSheet(f"background-color: {self.color}; border-radius: 10px;")
        # layout = QtWidgets.QVBoxLayout(notification)

        # # Add custom label
        # quote = self.get_random_quote()
        # label = QtWidgets.QLabel(quote)
        # label.setFont(QtGui.QFont("Arial", 14))
        # label.setAlignment(Qt.AlignCenter)
        # layout.addWidget(label)

        # # Set a timer for auto-close (similar to notification duration)
        # QTimer.singleShot(5000, notification.close)  # Closes after 5 seconds

        # # Show the window
        # notification.show()

        # app.exec_()
