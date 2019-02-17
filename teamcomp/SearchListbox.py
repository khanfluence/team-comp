import re
import tkinter


class SearchListbox(tkinter.Listbox):
    def __init__(self, root=None, **kwargs):
        super().__init__(root, kwargs)
        self.root = root
        self.timer = 0
        self.term = []
        self.items = []
        self.update_timer()

    def update_timer(self):
        if self.timer > 0:
            self.timer -= 10

        self.root.after(10, self.update_timer)

    def append(self, item):
        super().insert(tkinter.END, item)
        self.items.append(item)

    def append_stat(self, item):
        super().insert(tkinter.END, item)
        self.items.append(re.split(r'[+-]', item)[0].strip())

    def delete(self, first, last=None):
        super().delete(first, last)

        if last == tkinter.END:
            self.items.clear()
        else:
            del self.items[first]  # assuming super handles multiple, handle it here, too?

    def search(self, char):
        if self.timer == 0:
            self.term.clear()
        self.timer = 1000

        self.term.append(char.lower())
        idx = next((self.items.index(h) for h in self.items if h[0:len(self.term)].lower() == ''.join(self.term)), None)
        if idx is None:
            return

        self.see(idx)
        self.activate(idx)
        self.selection_clear(0, tkinter.END)
        self.selection_set(idx)
