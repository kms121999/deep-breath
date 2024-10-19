from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QTimer
import json
import random
import os

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


    def display_notification(self):
        '''
        :fun: This doesn't return anything, simply displays the notification.
        '''
        app = QtWidgets.QApplication([])

        # Create the window
        notification = QtWidgets.QWidget()
        notification.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        notification.setGeometry(self.x1, self.y1, self.x2, self.y2)  # Set position and size
        notification.setWindowOpacity(0.5)

        # Customize background and label
        notification.setStyleSheet(f"background-color: {self.color}; border-radius: 10px;")
        layout = QtWidgets.QVBoxLayout(notification)

        # Add custom label
        quote = self.get_random_quote()
        label = QtWidgets.QLabel(quote)
        label.setFont(QtGui.QFont("Arial", 14))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Set a timer for auto-close (similar to notification duration)
        QTimer.singleShot(5000, notification.close)  # Closes after 5 seconds

        # Show the window
        notification.show()

        app.exec_()  
