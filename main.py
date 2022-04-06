import tkinter as tk
import tkinter.filedialog
from functools import partial
import os
import re
import datetime
import batch_cleaner

def file_select():
    filepath = tk.filedialog.askdirectory(
        mustexist = True
    )
    entry_entry.insert(0, filepath)

window = tk.Tk()
window.title('Photo Batch Organizer')
window.geometry('500x200')
entry_label = tk.Label(text = 'Enter absolute path for photos')
entry_instructions = tk.Label(text = '(Should include the folder name in which the photos are stored.)')
entry_entry = tk.Entry(width = 55)
browse_button = tk.Button(
    master = window, 
    text = 'Browse', 
    command = lambda: file_select())
run_button = tk.Button(
    master = window,
    text = 'Organize photos', 
    command = lambda: batch_cleaner.photo_batch_cleaner(entry_entry.get())
    )


entry_label.pack()
entry_entry.pack()
entry_instructions.pack()
browse_button.pack()
run_button.pack()




window.mainloop()
