from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QTimer

class Notification:
    def __init__(self, message):
        self.alive = True
        self.quote = message

    def is_alive(self):
        return self.alive

    def display_notification(self):
        app = QtWidgets.QApplication([])

        # Create the window
        notification = QtWidgets.QWidget()
        notification.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        notification.setGeometry(10, 10, 300, 100)  # Set position and size
        notification.setWindowOpacity(0.5)

        # Customize background and label
        notification.setStyleSheet("background-color: darkblue; border-radius: 10px;")
        layout = QtWidgets.QVBoxLayout(notification)

        # Add custom label
        label = QtWidgets.QLabel(self.quote)
        label.setFont(QtGui.QFont("Arial", 14))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Set a timer for auto-close (similar to notification duration)
        QTimer.singleShot(5000, notification.close)  # Closes after 5 seconds

        # Show the window
        notification.show()

        app.exec_()

    #TODO - Get_inspiring_quote()

    #TODO - Get_homework_assignment()  
