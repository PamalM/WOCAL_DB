import datetime
import os
from platform import system
from time import sleep
import tkinter as tk
from tkinter import font
from tkcalendar import Calendar
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
import matplotlib.pyplot as plt


# Class is utilized to provide typography and color to console/terminal messages.
class Console:
    purple = '\033[95m'
    cyan = '\033[96m'
    darkCyan = '\033[36m'
    blue = '\033[94m'
    yellow = '\033[93m'
    red = '\033[91m'
    magenta = '\u001b[35m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'


# WoCal DB client.
class WoCal:

    # Initiate WoCal object by signing into MongoDB.
    def __init__(self, window):

        # Login credentials.
        self.username = None
        self.password = None
        self.url = "mongodb+srv://{0}:{1}@wocal.szoqb.mongodb.net/WOCAL?retryWrites=true&w=majority"

        # DB Attributes.
        self.client = None
        self.db = None
        self.workoutPerDay = None
        self.calPerDay = None

        # Method saves (login.txt) with user login credentials to project directory.
        def saveLogin():
            self._uMachine = system()
            # Proceed to save .txt file, only printing error if one arises.
            if self._uMachine == 'Darwin' or 'Linux':
                self._filename = os.getcwd() + '/login.txt'
            elif self._uMachine == 'Windows':
                self._filename = os.getcwd() + '\login.txt'
            else:
                self._filename = 'NOF'
            if self._filename != 'NOF':
                with open(self._filename, 'w') as self.file:
                    self.file.write(self.username + ":" + self.password)
                self.file.close()
            else:
                print(Console.red + Console.underline + Console.bold + '[Error occured whilst storing login credentials.]]' + Console.end)

        # [2] Styling methods for both entries.
        def usernameEntry_Focus(event):
            if self._usernameEntry.get() == 'Enter Username':
                self._usernameEntry.delete(0, tk.END)
                self._usernameEntry.insert(0, '')
                self._usernameEntry.config(bg='mistyrose', fg='gray25')
            elif self._usernameEntry.get() == '':
                self._usernameEntry.insert(0, 'Enter Username')
                self._usernameEntry.config(bg='gray25', fg='ivory')

        def passwordEntry_Focus(event):
            if self._passwordEntry.get() == 'Enter Password':
                self._passwordEntry.delete(0, tk.END)
                self._passwordEntry.insert(0, '')
                self._passwordEntry.config(bg='mistyrose', fg='gray25')
            elif self._passwordEntry.get() == '':
                self._passwordEntry.insert(0, 'Enter Password')
                self._passwordEntry.config(bg='gray25', fg='ivory')

        # Styling method for checkbox.
        def checkBox_Select():
            if self._rememberMe.get():
                self._rememberMeCheckBox.config(text='Remember login!', bg='azure2')
            else:
                self._rememberMeCheckBox.config(text='Stay signed-In?', bg='slategray3')

        # [2] Styling methods for Sign-In button.
        def signInButton_FocusIn(event):
            self._signInButton['highlightbackground'] = 'lightsalmon'
            self._signInButton['fg'] = 'gray25'
            self._signInButton['font'] = 'HELVETICA 20 underline'
            self._signInButton['relief'] = 'groove'

        def signInButton_FocusOut(event):
            self._signInButton['highlightbackground'] = 'lavender'
            self._signInButton['font'] = 'HELVETICA 20 bold'
            self._signInButton['fg'] = 'black'

        # Sign user into WoCal Collection in MongoDB.
        def signIn(*args):
            # Setup connection; Authenticate user before advancing to next GUI (Graphical-User-Interface).
            try:
                self._args = []
                for self._arguments in args:
                    self._args.append(self._arguments)
                if 'r' or 'remember' not in self._arguments:
                    self.username = str(self._usernameEntry.get())
                    self.password = str(self._passwordEntry.get())

                if self.username != 'Enter Username' and self.password != 'Enter Password':
                    self.client = MongoClient(self.url.format(self.username, self.password))
                    try:
                        # WoCal = DB, workoutPerDay & calPerDay = Collections within WoCal. (Initialize DB attributes)
                        self.client.admin.command('ismaster')
                        self.db = self.client['WOCAL']
                        self.workoutPerDay = self.db['workoutPerDay']
                        self.calPerDay = self.db['calPerDay']

                    # Direct user to the one error window for all general errors that may arise.
                    except ConnectionFailure:
                        raise ValueError
                    except OperationFailure:
                        raise ValueError

                    if 'r' or 'remember' not in self._arguments:
                        # Transition to next screen.
                        self._master.destroy()
                        self._master.quit()

                        # Save user login credentials to text file if 'rememberMe' checkbutton is selected by user.
                        if self._rememberMe.get():
                            saveLogin()

                    print(Console.blue + Console.bold + '[{0} has signed into the DB]'.format(self.username) + Console.end)

                    # Transfer to next screen.
                    self.root = tk.Tk()
                    self.methodsScreen(self.root)
                    self.root.mainloop()

            # Unable to establish connection; Notify user with alert window.
            except OperationFailure and ConnectionFailure and ValueError:
                def close():
                    self._alert.destroy()
                    self._alert.quit()

                print(Console.red + Console.bold + Console.underline + '[Authentication Error!]' + Console.end)
                self._alert = tk.Tk()
                self._alert.grid_rowconfigure(0, weight=1)
                self._alert.grid_columnconfigure(0, weight=1)
                self._alert.grid_rowconfigure(1, weight=1)
                self._label = tk.Label(self._alert, text='[Authentication Error]')
                self._label.grid(row=0, column=0, sticky='ew', padx=18, pady=(10, 0))
                self._font2 = font.Font(self._topFrame, family='TIMES NEW ROMAN', size=20, weight='bold')
                self._alertMsg = '''The application couldn't establish a successful\nconnection with the login credentials you've provided!'''
                self._label2 = tk.Label(self._alert, text=self._alertMsg, font=self._font2, bg='coral4', fg='ivory')
                self._label2.grid(row=1, column=0, sticky='ew', padx=18)
                self._closeButton = tk.Button(self._alert, text='Close Message', font='TIMES 18 bold', command=lambda: self._alert.destroy())
                self._closeButton.grid(row=2, column=0, sticky='ew', padx=18, pady=(0, 10))

                self._alert.title('Authentication Error')
                self._alert.minsize(300, 150)
                self._alert.resizable(False, False)
                self._alert.config(bg='coral4')
                self._alert.bind('<Return>', lambda cmd: close())
                self._alert.mainloop()

        # Method determines if user login is necessary again (RememberMe?)
        def determine_Login():
            # Determine user machine OS, and check if login.text file exists.
            self._uMachine = system()
            self._filename = None
            self._fileExists = None
            if self._uMachine == 'Darwin' or 'Linux':
                self._filename = os.getcwd() + '/login.txt'
                self._fileExists = os.path.exists(self._filename)
            elif self._uMachine == 'Windows':
                self._filename = os.getcwd() + '\\login.txt'
                self._fileExists = os.path.exists(self._filename)

            if self._fileExists:
                with open(self._filename, "r") as self._file:
                    for line in self._file:
                        self._credentials = line.split(':')
                    self.username = self._credentials[0]
                    self.password = self._credentials[1]
                self._file.close()

                # Bypass login screen and proceed with automatic sign-in.
                signIn('r')

        # Run method before initiating sign-ign window.
        determine_Login()
        print(Console.yellow + Console.bold + '[Waiting for user to login to DB...]' + Console.end)

        # Sign In Window.
        self._master = window

        # Top Frame.
        self._topFrame = tk.Frame(self._master, bg='gray25')
        self._topFont = font.Font(self._topFrame, family='HELVETICA', size=30, weight='bold', underline=True)
        self._topLabel1 = tk.Label(self._topFrame, text='Sign Into Database:', font=self._topFont, bd=4, bg='lavender', fg='gray25')
        self._topLabel1.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        self._topFrame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Middle Frame.
        self._middleFrame = tk.Frame(self._master, bg='slategray3', relief='raised', bd=4, highlightbackground='gray25')
        self._middleFrame.grid_columnconfigure(0, weight=1)
        self._middleFrame.grid_rowconfigure(0, weight=1)
        self._middleFrame.grid_rowconfigure(1, weight=1)
        self._middleFrame.grid_rowconfigure(2, weight=1)
        self._middleFrame.grid_rowconfigure(3, weight=1)
        self._usernameEntry = tk.Entry(self._middleFrame, justify='center', font='HELVETICA 14 bold', bg='gray25', fg='ivory')
        self._usernameEntry.grid(row=0, column=0, sticky='nsew', pady=(14, 0), padx=18)
        self._usernameEntry.insert(0, 'Enter Username')
        self._passwordEntry = tk.Entry(self._middleFrame, justify='center', font='HELVETICA 14 bold', bg='gray25', fg='ivory')
        self._passwordEntry.grid(row=1, column=0, sticky='nsew', padx=18, pady=10)
        self._passwordEntry.insert(0, 'Enter Password')
        self._rememberMe = tk.BooleanVar(self._master)
        self._rememberMe.set(False)
        self._rememberMeCheckBox = tk.Checkbutton(self._middleFrame, text='Stay signed-In?', variable=self._rememberMe)
        self._rememberMeCheckBox.config(command=checkBox_Select(), bg='slategray3')
        self._rememberMeCheckBox.grid(row=2, column=0, pady=(0, 14), sticky='ns', padx=20)
        self._signInButton = tk.Button(self._middleFrame, text='Sign In!', height=3, font='HELVETICA 20 bold', relief='ridge', bd=1)
        self._signInButton.config(command=lambda: signIn())
        self._signInButton.config(highlightbackground='lavender')
        self._signInButton.grid(row=3, column=0, sticky='nsew', pady=10, padx=18)
        self._signInButton.focus_set()
        self._usernameEntry.bind('<FocusIn>', usernameEntry_Focus)
        self._usernameEntry.bind('<FocusOut>', usernameEntry_Focus)
        self._passwordEntry.bind('<FocusIn>', passwordEntry_Focus)
        self._passwordEntry.bind('<FocusOut>', passwordEntry_Focus)
        self._signInButton.bind('<Enter>', signInButton_FocusIn)
        self._signInButton.bind('<Leave>', signInButton_FocusOut)
        self._middleFrame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Bottom Frame.
        self._bottomFrame = tk.Frame(self._master, bg='gray25')
        self._bottomFont = font.Font(self._topFrame, family='TIMES NEW ROMAN', size=10)
        self._bottomLabel = tk.Label(self._bottomFrame, text='Powered through MongoDB\nCreated by Pamal Mangat')
        self._bottomLabel.config(font=self._bottomFont, bg='lavender')
        self._bottomLabel.pack(fill=tk.BOTH, padx=18, pady=10, expand=True)
        self._bottomFrame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Sign-In Window attributes.
        self._master.title('WOCAL - SIGN IN')
        self._master.minsize(400, 500)
        self._master.config(bg='royalblue2')
        self._master.bind('<Return>', lambda cmd: signIn())
        self._master.mainloop()

    # Main-Menu for the program.
    def methodsScreen(self, window):
        self._master = window
        self._master.mainloop()


# Execute Program.
if __name__ == '__main__':
    master = tk.Tk()
    woCal = WoCal(master)
    master.mainloop()
