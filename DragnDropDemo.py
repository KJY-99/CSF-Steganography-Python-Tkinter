# Hi all this is a demonstration for the drag and drop function. You can run this file separately to take a look at how it functions.

import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
# METHOD 1: GET FILEPATH METHOD (Cannot have spaces in the filename)
# This method requires a listbox to function. User drags their desired file to the listbox and it will get the filepath.
# You can then get the file from the exact filepath, perform your encoding/decoding and display image/video.
def drop_inside_listbox(event):
    listb.insert("end", event.data)
    
# METHOD 2: READ TEXT FILE METHOD (Cannot have spaces in the filename)
# This method requires a texbox to function. User drags their desired file to the listbox and it will read the file to text, printing it in the textbox.
def drop_inside_textbox(event):
    tbox.delete("1.0", "end")
    eventtest = event.data
    eventtest = eventtest.strip("}{")
    print(eventtest)
    if eventtest.endswith(".txt"):
        with open(eventtest, "r") as file:
            for line in file:
                line = line.strip()
                tbox.insert("end", f"{line}\n")

# Open Tkinter window
root = TkinterDnD.Tk()
root.geometry("800x500")

# Add UI Elements - Listbox (Method 1)
listb = tk.Listbox(root, selectmode=tk.SINGLE, background="#ffe0d6")
listb.pack(fill=tk.X)
listb.drop_target_register(DND_FILES)
listb.dnd_bind("<<Drop>>", drop_inside_listbox)

# Add UI Elements - Textbox (Method 2)
tbox = tk.Text(root)
tbox.pack()
tbox.drop_target_register(DND_FILES)
tbox.dnd_bind("<<Drop>>", drop_inside_textbox)

# Run Application
root.mainloop()