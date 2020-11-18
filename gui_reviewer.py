import tkinter as tk
from tkinter import ttk 
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from configparser import ConfigParser 
import os

from operations.reviewer import Reviewer

WINDOW_HEIGHT = 320
WINDOW_WIDTH = 500

class ReviewerWindow(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master

        # read configs
        configParser = ConfigParser() 
        configParser.read('reviewer_config.ini')

        self.pack(fill=tk.BOTH, expand=1)

        # menu
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = tk.Menu(menu)
        fileMenu.add_command(label="Exit", command=self._exitProgram)
        menu.add_cascade(label="File", menu=fileMenu)

        # maxLineLength label
        self.maxLineLengthLabel = tk.Label(self, text="Maximum line length (before a \\N):")
        self.maxLineLengthLabel.grid(row=0, column=0, pady=10, padx=10, sticky=tk.E)

        # maxLineLength entry
        defaultMaxLineLength = configParser.get('root', 'defaultMaxLineLength')
        self.maxLineLengthEntry = tk.Entry(self)
        self.maxLineLengthEntry.insert(0, defaultMaxLineLength)
        self.maxLineLengthEntry.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)

        ttk.Separator(self, orient='horizontal').grid(row=1, columnspan=2, sticky=tk.EW)

        # namesToCapitalizeFilePath label
        self._namesToCapitalizeFilePath = None
        self.namesToCapitalizeFilePathLabel = tk.Label(self, text="File path containing the list of names to capitalize:")
        self.namesToCapitalizeFilePathLabel.grid(row=2, column=0, pady=10, padx=10, sticky=tk.E)

        # namesToCapitalizeFilePath button
        self.namesToCapitalizeFilePathBtn = tk.Button(self, text="Search", command=self._getCapitalizeNamesFilePath)
        self.namesToCapitalizeFilePathBtn.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # capitalizeNamesFileStatus label
        self.capitalizeNamesFileStatusLabel = tk.Label(self, text=f"No file loaded yet", wraplength=WINDOW_WIDTH - 20)
        self.capitalizeNamesFileStatusLabel.grid(row=3, columnspan=2, pady=10, padx=10, sticky=tk.W)

        ttk.Separator(self, orient='horizontal').grid(row=4, columnspan=2, sticky=tk.EW)

        # filePath label
        self._filePath = None
        self.filePathLabel = tk.Label(self, text="File to review:")
        self.filePathLabel.grid(row=5, column=0, pady=10, padx=10, sticky=tk.E)

        # load file button
        self.loadFileButton = tk.Button(self, text="Load .ass", command=self._getFilePath)
        self.loadFileButton.grid(row=5, column=1, pady=10, padx=10, sticky=tk.W)

        # filePathStatus label
        self.filePathStatusLabel = tk.Label(self, text="No file loaded yet", wraplength=WINDOW_WIDTH - 20)
        self.filePathStatusLabel.grid(row=6, columnspan=2, pady=10, padx=10, sticky=tk.W)

        ttk.Separator(self, orient='horizontal').grid(row=7, columnspan=2, sticky=tk.EW)

        # review button
        self.reviewButton = tk.Button(self, text="Review", command=self._clickReviewButton)
        self.reviewButton.grid(row=8, column=0, columnspan=2, pady=10, padx=10)


    def _getCapitalizeNamesFilePath(self):
        capitalizeNamesFileDlg = fd.askopenfilename(title='Choose file containing names to capitalize', initialdir='..', filetypes=[("all","*.*")])

        if capitalizeNamesFileDlg != "":
            self._namesToCapitalizeFilePath = capitalizeNamesFileDlg
            self.capitalizeNamesFileStatusLabel.configure(text=f'Loaded file: {self._namesToCapitalizeFilePath}')


    def _getFilePath(self):
        filePathFromDlg = fd.askopenfilename(title='Choose .ass to review', initialdir='..', filetypes=[(".ass","*.ass")])

        if filePathFromDlg != "":
            self._filePath = filePathFromDlg
            self.filePathStatusLabel.configure(text=f'Loaded file: {self._filePath}')


    def _exitProgram(self):
        exit()


    def _clickReviewButton(self):
        if self._retrieveMaxLineLength(self.maxLineLengthEntry.get()) is False:
            mb.showerror(title="Invalid maximum line length", message="Maximum line length must be a positive integer greater than 1.")
            return

        if self._filePath == None:
            mb.showerror(title="No filepath selected", message="Please load the .ass file")
            return

        reviewConfirmed = mb.askokcancel(title="Ready to review", message="Click ok to start the review process, then wait! Another message box will notify you at the end.")
        if reviewConfirmed is False:
            return
        self._reviewer = Reviewer(self._filePath, self._maxLineLength, self._namesToCapitalizeFilePath)
        self._reviewer.review()
        mb.showinfo(title="Review done!", message='Review successful. You should see a new .ass file with the suffix "_reviewed"')
    

    def _retrieveMaxLineLength(self, mll: str) -> bool:
        try:
            val = int(mll)
            self._maxLineLength = val
            return val > 1
        except ValueError:
            return False


root = tk.Tk()
app = ReviewerWindow(root)

# set window title
root.wm_title("Reviewer")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

# show window
root.mainloop()