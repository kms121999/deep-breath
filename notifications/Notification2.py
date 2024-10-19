import tkinter as tk
from overlay import Window
from tkhtmlview import HTMLLabel

def Notification():
    # Create the window
    win = Window()

    win.size = (700,800)

    # Change the title of the window
    win.root.title("Custom Notification")

    # Set the background color of the window (can be any color, it will be transparent later)
    win.root.configure(bg="lightblue")

    # Make the window transparent
    win.root.attributes("-alpha", 0.9)  # 0.9 is the transparency level (90% opacity)

    # Create the HTMLLabel with your HTML content
    my_label = HTMLLabel(win.root, html=""" 
        <iframe src="demo_iframe.htm" height="200" width="300" title="Iframe Example"></iframe>
    """)

    # Pack the HTMLLabel into the window
    my_label.pack(pady=10, padx=10)

    # Create the regular label and change its text color and background
    label = tk.Label(win.root, text="Hey", font=("Arial", 14), bg="lightblue", fg="black")
    label.pack(pady=20, padx=20)

    # Launch the window
    win.root.mainloop()

Notification()

    

