# import tkinter as tk
# from overlay import Window
# from tkhtmlview import HTMLLabel

# def Notification():
#     # Create the window
#     win = Window()

#     # Change the title of the window
#     win.root.title("Custom Notification")

#     # Set the background color of the window (can be any color, it will be transparent later)
#     win.root.configure(bg="lightblue")

#     # Make the window transparent
#     win.root.attributes("-alpha", 0.9)  # 0.9 is the transparency level (90% opacity)

#     # Create the HTMLLabel with your HTML content
#     my_label = HTMLLabel(win.root, html=""" 
#         <h1 style="color: lightblue;">DeepBreath</h1>
#     """)

#     # Pack the HTMLLabel into the window
#     my_label.pack(pady=10, padx=10)

#     # Create the regular label and change its text color and background
#     label = tk.Label(win.root, text="Hey", font=("Arial", 14), bg="lightblue", fg="black")
#     label.pack(pady=20, padx=20)

#     win.root.after(5000, lambda: safe_destroy(win.root))

#     # Launch the window
#     win.root.mainloop()

# def safe_destroy(window):
#     try:
#         window.destroy()
#     except tk.TclError:
#         pass

# def schedule_notification():
#     Notification()

#     tk.Tk().after(1000, schedule_notification)

# schedule_notification()


import tkinter as tk
from overlay import Window  # Ensure your `Window` class is properly defined.
from tkhtmlview import HTMLLabel

def Notification():
    # Create the window
    win = Window()

    # Change the title of the window
    win.root.title("Custom Notification")

    # Set the background color of the window (can be any color, it will be transparent later)
    win.root.configure(bg="lightblue")

    # Make the window transparent
    win.root.attributes("-alpha", 0.9)  # 0.9 is the transparency level (90% opacity)

    # Create the HTMLLabel with your HTML content
    my_label = HTMLLabel(win.root, html=""" 
        <h1 style="color: lightblue;">DeepBreath</h1>
    """)
    my_label.pack(pady=10, padx=10)

    # Regular label
    label = tk.Label(win, text="Hey", font=("Arial", 14), bg="lightblue", fg="black")
    label.pack(pady=20, padx=20)

    win.root.after(5000,win.root.destroy)

    # Launch the window
    win.root.mainloop()

    # win.root.quit()

# Notification()

    

