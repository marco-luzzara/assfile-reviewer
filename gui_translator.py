import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from configparser import ConfigParser 

from operations.translator import Translator

WINDOW_HEIGHT = 200
WINDOW_WIDTH = 320

class TranslatorWindow(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master

        # read configs
        configParser = ConfigParser() 
        configParser.read('translator_config.ini')
        self._apiKey = configParser.get('translation_service', 'apiKey')
        self._serviceUrl = configParser.get('translation_service', 'serviceUrl')

        self.pack(fill=tk.BOTH, expand=1)

        # menu
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = tk.Menu(menu)
        fileMenu.add_command(label="Exit", command=self._exitProgram)
        menu.add_cascade(label="File", menu=fileMenu)

        # load file button
        self._filePath = None
        self.loadFileButton = tk.Button(self, text="Load .ass", command=self._getFilename)
        self.loadFileButton.pack(expand=True, padx=10, pady=10)

        # file status
        self.fileStatusLabel = tk.Label(self, text="Load .ass file to translate", wraplength=WINDOW_WIDTH - 20)
        self.fileStatusLabel.pack(expand=True)

        # translate button
        self.translateButton = tk.Button(self, text="Translate", command=self._clickTranslateButton)
        self.translateButton.pack(side=tk.BOTTOM, padx=10, pady=10)

    def _getFilename(self):
        fileNameFromDlg = fd.askopenfilename(title='Choose .ass to translate', initialdir='..', filetypes=[(".ass","*.ass")])

        if fileNameFromDlg != "":
            self._filePath = fileNameFromDlg
            self.fileStatusLabel.configure(text=f'Loaded file: {self._filePath}')

    def _exitProgram(self):
        exit()

    def _clickTranslateButton(self):
        if self._filePath == None:
            mb.showerror(title="No filepath selected", message="Please select filepath from the open dialog")
            return

        translationConfirmed = mb.askokcancel(title="Ready to translate", message="Click ok to start the translation, then wait! Another message box will notify you at the end.")
        if translationConfirmed is False:
            return
        self._translator = Translator(self._filePath, self._apiKey, self._serviceUrl)
        self._translator.translate()
        mb.showinfo(title="Translation done!", message='Translation successful. You should see a new .ass file with the suffix "_translated"')
        

root = tk.Tk()
app = TranslatorWindow(root)

# set window title
root.wm_title("Translator")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

# show window
root.mainloop()