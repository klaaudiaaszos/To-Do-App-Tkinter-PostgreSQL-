import tkinter as tk
from db import create_table
import gui

create_table ()

gui.root.protocol ("WM_DELETE_WINDOW", gui.on_closing)
gui.root.mainloop ()