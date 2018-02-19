from Window import Window
from tkinter import *


def close():
    app.write_stats()
    root.destroy()


root = Tk()
app = Window(root)
root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
