import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter GUI")

#Top Width label
menuWidthLabel = tk.Label(root, text="-----------------------------------------------------------------")
menuWidthLabel.pack(pady=10)

# Time label and entry box
timeLabel = tk.Label(root, text="Enter time for rule (in minutes):")
timeLabel.pack(pady=10)
timeEntry = tk.Entry(root, width=30)
timeEntry.pack(pady=5)

# TimeScale label and radio
timeScaleLabel = tk.Label(root, text="Select how time is measured:")
timeScaleLabel.pack(pady=10)
timeScaleTypes = ["session", "day", "week"]
def sel():
   selection = "You selected " + str(timeScaleTypes[var.get()])
   label.config(text = selection)
var = tk.IntVar()
R1 = tk.Radiobutton(root, text="count in the session ", variable=var, value=0, command=sel)
R1.pack( anchor = tk.W )
R2 = tk.Radiobutton(root, text="count for the day", variable=var, value=1, command=sel)
R2.pack( anchor = tk.W )
R3 = tk.Radiobutton(root, text="count for the week", variable=var, value=2, command=sel)
R3.pack( anchor = tk.W)
label = tk.Label(root)
label.pack()

# color label and dropdown
colorLabel = tk.Label(root, text="Color")
colorLabel.pack(pady=10)
#currently textbox is the input, do we want only the dropdown? Data retrieval needed, see comment below
colorEntry = tk.Entry(root, width=30)
colorEntry.pack(pady=5)
#dropdown?----------------------------
# datatype of menu text 
clicked = tk.StringVar()
colorOptions = ["red", "gray", "white", "black"]
colorDropdown = tk.OptionMenu(root , clicked , *colorOptions ) 
colorDropdown.pack()
#info here: https://www.geeksforgeeks.org/dropdown-menus-tkinter/

# Shutdown label and dropdown
shutdownLabel = tk.Label(root, text="Shutdown the program? (True/False)")
shutdownLabel.pack(pady=10)
# Create an entry widget for user input
shutdownEntry = tk.Entry(root, width=30)
shutdownEntry.pack(pady=5)
#Dropdown, change StringVar to boolean?
clicked = tk.StringVar()
boolOptions = [True, False]
colorDropdown = tk.OptionMenu(root , clicked , *boolOptions ) 
colorDropdown.pack()

# message type label and textbox. Dropdown needed
messageTypeLabel = tk.Label(root, text="Select your message type:")
messageTypeLabel.pack(pady=10)
messageTypeEntry = tk.Entry(root, width=30)
messageTypeEntry.pack(pady=5)

def submit_click():
    summary_text = "after "+timeEntry.get()+" minutes in a "+timeScaleTypes[var.get()]+" I'll send you a "+colorEntry.get()+" "+messageTypeEntry.get()+" message and "+("shutdown" if shutdownEntry.get().lower()=="true" else "not shutdown")
    summaryLabel.config(text=f"So, {summary_text}. Sound good?")  # Update the label with the input text
    #session, day, week

# summary label and submit button
summaryLabel = tk.Label(root, text="Select Settings above")
summaryLabel.pack(pady=10)
submitButton = tk.Button(root, text="Submit Settings", command=submit_click)
submitButton.pack(pady=10)

#confirm label and button
confirmAndSendLabel = tk.Label(root, text="")
confirmAndSendLabel.pack(pady=10)
def confirm_click():
    confirmAndSendLabel.config(text=f"I hope that went through")

confirmAndSendButton = tk.Button(root, text="Confirm", command=confirm_click)
confirmAndSendButton.pack(pady=10)

# Run the application
root.mainloop()
