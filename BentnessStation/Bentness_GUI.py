# -*- coding: utf-8 -*-

'''
Bentness GUI

Description: This simply records the bentness of the tube. It automatically
adds a tube to the database without creating a csv file.

To run, first install Tkinter module into your python library. After
that, running is as simple as: python "Bentness GUI.py" or double clicking in 
Windows 10. 

@author: Jason Gombas
'''

import tkinter as tk
from tkinter import StringVar
import os
from datetime import datetime
import sys

DROPBOX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DROPBOX_DIR)
from sMDT import db, tube, mini_tube
from sMDT.data import bent
path=os.path.dirname(os.path.abspath(__file__))



def write(code, length, name):
    datab = db.db()
    tube1 = mini_tube.Mini_tube()
    tube1.set_ID(code)
    if not length:
        length = 0
    tube1.bent.add_record(bent.BentRecord(bentness=float(length),user=name))    
    datab.add_tube(tube1)
        
#######################################
#####      Swage Entry Code    ########
#######################################    
def handle_enter(event):
    entry_name.config({"background": "White"})
    entry_barcode.config({"background": "White"})
    entry_length.config({"background": "White"})

    if button.cget("text") == "Create Entry":
        status = True
        text_entryStatus.delete("1.0", tk.END)
        if not entry_length.get().replace('.', '', 1).replace('-', '', 1).isdigit() and entry_length.get():
            entry_length.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Lengths aren't numbers")
            status = False
        if entry_name.get() == '':
            entry_name.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Fill in name")
            status = False
        if entry_barcode.get() == '':
            entry_barcode.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Fill in barcode")
            status = False
        #if entry_length.get() == '':
            #entry_length.config({"background": "Red"})
            #text_entryStatus.delete("1.0", tk.END)
            #text_entryStatus.insert("1.0", "Fill in gap size")
            #status = False
        if len(entry_barcode.get()) != 8 and len(entry_barcode.get()) != 5:
            entry_barcode.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Incorrect barcode format")
            status = False
        if len(entry_barcode.get()) == 8:
            if not entry_barcode.get()[3:].isdigit():
                entry_barcode.config({"background": "Red"})
                text_entryStatus.delete("1.0", tk.END)
                text_entryStatus.insert("1.0", "Incorrect barcode format")
                status = False
        if len(entry_barcode.get()) == 5:
            if not entry_barcode.get().isdigit():
                entry_barcode.config({"background": "Red"})
                text_entryStatus.delete("1.0", tk.END)
                text_entryStatus.insert("1.0", "Incorrect barcode format")
                status = False
        if status:         
            name = entry_name.get()
            barcode = entry_barcode.get()
            # Add MSU to number only code
            if len(barcode) == 5:
                barcode  = 'MSU' + barcode
            # Force first 3 letters to be capital
            else:
                barcode = 'MSU' + barcode[3:]
            firstLength = entry_length.get()
            write(barcode,firstLength,name)
            entry_barcode.delete(0, tk.END)
            entry_length.delete(0, tk.END)
        entry_barcode.focus()
        
        
window = tk.Tk()
window.title("Bentness GUI")
window.columnconfigure(0, weight=1, minsize=75)
window.rowconfigure(0, weight=1, minsize=50)
window.bind("<Return>", (lambda event: handle_enter(event)))


########### Generate Frames ###############
frame_entry = tk.Frame(
            master=window,
            width = 25,
            relief=tk.RAISED,
            borderwidth=1
        )
frame_entry.pack()


########### Entry Frame ###############
label_name = tk.Label(master=frame_entry, text="Name")
entry_name = tk.Entry(master=frame_entry)

label_barcode = tk.Label(master=frame_entry, text="Barcode")

entry_barcode = tk.Entry(master=frame_entry)

label_length = tk.Label(master=frame_entry, text='Gap Size [mm]')
entry_length = tk.Entry(master=frame_entry)

button = tk.Button(
    master=frame_entry,
    text="Create Entry",
    width=33,
    height=2,
    bg="blue",
    fg="yellow",
)
button.bind("<Button-1>", handle_enter)
text_entryStatus = tk.Text(master=frame_entry, width=30, height=2)
text_info = tk.Text(master=frame_entry, width=30, height=14, wrap=tk.WORD)

# Info
info = "Bentness station: Scan the tube and rotate it until you see the largest gap at the camera. Then read off the value and put it here. Put in the value that you measure. If it is 0.8 mm or below, then the tube passes and you can use it for swaging. If you enter an illegal format bar code, there will be an error message."
text_info.insert("1.0", info)

############  Pack Everything Together  ##########
entry = tk.Entry()
label_name.pack()
entry_name.pack()

label_barcode.pack()
entry_barcode.pack()

label_length.pack()
entry_length.pack()

text_entryStatus.pack()

button.pack()

text_info.pack()



# Execute mainloop
window.mainloop()
