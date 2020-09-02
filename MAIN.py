import pymongo as pym
import tkinter as tk
import matplotlib.pyplot as plt
from PIL import ImageTk, Image


class WoCal:

    # Initiate WoCal object by signing into DB.
    def __init__(self, master):
        # Create Login Window for DB.
        self.master = master



        # Window Attributes.
        self.master.title('WOCAL - SIGN IN')
        self.master.minsize(400, 400)
        self.master.resizable(False, False)

        self.master.mainloop()


# Execute Program.
def main():
    master = tk.Tk()
    wocal_obj = WoCal(master)
    master.mainloop()


if __name__ == '__main__':
    main()
