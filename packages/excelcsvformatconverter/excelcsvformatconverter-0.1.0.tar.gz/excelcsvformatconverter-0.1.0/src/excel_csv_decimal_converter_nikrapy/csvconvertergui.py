import tkinter
from pathlib import Path
from tkinter import filedialog
from tkinter.constants import TOP

from excel_csv_decimal_converter_nikrapy import csvdecimalconverter


class MyApp:

    def __init__(self, parent):
        self.src_folder: Path = Path()
        self.dst_folder: Path = Path()

        self.frm = tkinter.Frame(parent, padx=10, pady=10)
        self.frm.grid()
        self.message = tkinter.Label(self.frm, text="Select Source and Destination Folder")

        self.button1 = tkinter.Button(self.frm, text="Source Folder")
        self.button1.pack(side=TOP)
        self.button1.bind("<Button>", self.src_select_button_click)

        src_folder = tkinter.Label(self.frm, text="")
        src_folder.pack()

        self.button2 = tkinter.Button(self.frm, text="Destination Folder")
        self.button2.pack()
        self.button2.bind("<Button>", self.dst_select_button_click)
        src_folder = tkinter.Label(self.frm, text="")
        src_folder.pack()

        self.button3 = tkinter.Button(self.frm, text="Convert!")
        self.button3.pack()
        self.button3.bind("<Button>", self.convert_button_click)
        src_folder = tkinter.Label(self.frm, text="")
        src_folder.pack()

    def src_select_button_click(self, event):
        self.src_folder = Path(filedialog.askdirectory(initialdir=self.src_folder.resolve()))

    def dst_select_button_click(self, event):
        self.dst_folder = Path(filedialog.askdirectory(initialdir=self.dst_folder.resolve()))

    def convert_button_click(self, event):
        csvdecimalconverter.convert_files_in_dir(self.src_folder, self.dst_folder)


def gui_main():
    tk = tkinter.Tk()
    myapp = MyApp(tk)
    tk.mainloop()


if __name__ == "__main__":
    gui_main()
