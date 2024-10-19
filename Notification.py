from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QTimer

def show_custom_notification():
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
    label = QtWidgets.QLabel("This is a unique notification!")
    label.setFont(QtGui.QFont("Arial", 14))
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label)
    
    # Set a timer for auto-close (similar to notification duration)
    QTimer.singleShot(5000, notification.close)  # Closes after 5 seconds
    
    # Show the window
    notification.show()
    
    app.exec_()

# Trigger the notification
show_custom_notification()