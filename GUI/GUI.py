import tkinter as tk

# Function to handle button click
def on_click():
    input_text = entry.get()  # Get text from the entry widget
    label.config(text=f"Hello, {input_text}!")  # Update the label with the input text

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter GUI")

# Create a label
label = tk.Label(root, text="Enter your name:")
label.pack(pady=10)

# Create an entry widget for user input
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Create a button that will trigger the on_click function
button = tk.Button(root, text="Submit", command=on_click)
button.pack(pady=10)

# Run the application
root.mainloop()
