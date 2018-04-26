import tkinter
from Window import Window


def close():
    app.write_stats()
    root.destroy()


root = tkinter.Tk()
app = Window(root)
root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
