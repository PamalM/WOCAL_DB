import datetime
import os
from platform import system
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
        self.currentDate = datetime.datetime.now()

        # Attributes for reading/writing (login.txt).
        self.uMachine = system()
        self.fileName = None
        self.file = None

        # Method saves (login.txt) with user login credentials to project directory.
        def saveLogin():
            # Proceed to save .txt file, only printing error if one arises.
            if self.uMachine == 'Darwin' or 'Linux':
                self.filename = os.getcwd() + '/login.txt'
            elif self.uMachine == 'Windows':
                self.filename = os.getcwd() + '\login.txt'
            else:
                self.filename = 'NOF'
            if self.filename != 'NOF':
                with open(self.filename, 'w') as self.file:
                    self.file.write(self.username + ":" + self.password)
                self.file.close()
            else:
                print(Console.red + Console.underline + Console.bold + '[Error occurred whilst storing login credentials.]]' + Console.end)

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
        # SignIn(0) = Normal Sign-In, SignIn(1) = ByPass Sign-In.
        def signIn(tag):
            # Setup connection; Authenticate user before advancing to next GUI (Graphical-User-Interface).
            try:
                if tag == 0:
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

                        print(Console.blue + Console.bold + '[{0} has signed into the DB]'.format(self.username) + Console.end)

                    # Direct user to the one error window for all general errors that may arise.
                    except ConnectionFailure:
                        raise ValueError
                    except OperationFailure:
                        raise ValueError

                    if tag == 0:
                        # Transition to next screen.
                        self._master.destroy()
                        self._master.quit()

                        # Save user login credentials to text file if 'rememberMe' checkbutton is selected by user.
                        if self._rememberMe.get():
                            saveLogin()

                        # Transfer to next screen.
                        self._root = tk.Tk()
                        self.methodsScreen(self._root)
                        self._root.mainloop()
                    else:
                        self.methodsScreen(self._master)


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
            self.filename = None
            self.fileExists = None
            if self.uMachine == 'Darwin' or 'Linux':
                self.filename = os.getcwd() + '/login.txt'
                self.fileExists = os.path.exists(self.filename)
            elif self.uMachine == 'Windows':
                self.filename = os.getcwd() + '\\login.txt'
                self.fileExists = os.path.exists(self.filename)

            if self.fileExists:
                with open(self.filename, "r") as self.file:
                    for line in self.file:
                        self._credentials = line.split(':')
                    self.username = self._credentials[0]
                    self.password = self._credentials[1]
                self.file.close()

                # Bypass login screen and proceed with automatic sign-in.
                signIn(1)

        print(Console.yellow + Console.bold + '[Waiting for user to login to DB...]' + Console.end)

        # Sign In Window.
        self._master = window

        # Run method before drawing in complete master window.
        determine_Login()

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
        self._signInButton.config(command=lambda: signIn(0))
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
        self._master.bind('<Return>', lambda cmd: signIn(0))
        self._master.mainloop()

    # Main-Menu for the program.
    def methodsScreen(self, window):

        # Direct user to specific method depending on tag (specified from/by button).
        def terminal(tag):
            self._master.destroy()
            self._master.quit()
            self._root = tk.Tk()
            if tag == 1:
                self.inputCalories(self._root)
            elif tag == 2:
                self.viewCalories(self._root)
            elif tag == 3:
                self.inputWorkout(self._root)
            elif tag == 4:
                self.viewWorkout(self._root)
            self._root.mainloop()

        # Method deletes (login.txt) file from project directory when user signs out.
        def deleteLogin():
            # Proceed to save .txt file, only printing error if one arises.
            if self.uMachine == 'Darwin' or 'Linux':
                self.filename = os.getcwd() + '/login.txt'
            elif self.uMachine == 'Windows':
                self.filename = os.getcwd() + '\login.txt'
            else:
                self.filename = 'NOF'
            if self.filename != 'NOF':
                os.remove(self.filename)
                self.file.close()
            else:
                print(Console.red + Console.underline + Console.bold + '[Error occured whilst deleting login credentials.]]' + Console.end)

        # Log user out of DB & delete (login.txt) file if it exists.
        def logOff():
            try:
                self._master.destroy()
                self._master.quit()
                deleteLogin()
            except FileNotFoundError:
                pass
            finally:
                print(Console.purple + Console.bold + "[{0} has been logged out of the database]".format(self.username) + Console.end)
                self.root = tk.Tk()
                self.__init__(self.root)
                self.root.mainloop()

        # Main-Menu window.
        self._master = window

        # Top Frame.
        self._topFrame = tk.Frame(self._master, bg='gray25', relief='raised', bd=4, highlightbackground='gray30')
        self._topFrame.grid_rowconfigure(0, weight=1)
        self._topFrame.grid_columnconfigure(0, weight=1)
        self._topFrame.grid_columnconfigure(1, weight=1)
        self._topFrame.grid_rowconfigure(0, weight=1)
        self._topFrame.grid_columnconfigure(0, weight=1)
        self._topFrame.grid_columnconfigure(1, weight=1)
        self._topFont = font.Font(self._topFrame, family='Times NEW ROMAN', size=20, weight='bold', underline=False)
        self._welcomeLabel = tk.Label(self._topFrame, text='Welcome,\n{0}'.format(self.username), font=self._topFont)
        self._welcomeLabel.config(anchor='w', bg='gray25', fg='ivory')
        self._welcomeLabel.grid(row=0, column=0, sticky='ew', padx=18, pady=2)
        self._logOffButton = tk.Button(self._topFrame, text='LogOff', font='HELVETICA 18 bold', relief='raised', bd=2)
        self._logOffButton.config(command=lambda: logOff(), highlightbackground='indianred')
        self._logOffButton.grid(row=0, column=1, sticky='nsew', padx=18, pady=8)
        self._topFrame.pack(fill=tk.BOTH, expand=False, padx=18, pady=(14, 0))

        # Bottom Frame.
        self._bottomFrame = tk.Frame(self._master, bg='snow3', relief='raised', bd=4, highlightbackground='gray30')
        self._bottomFrame.grid_columnconfigure(0, weight=1)
        self._bottomFrame.grid_columnconfigure(1, weight=1)
        self._bottomFrame.grid_rowconfigure(0, weight=1)
        self._bottomFrame.grid_rowconfigure(1, weight=1)
        self._bottomFont = font.Font(self._topFrame, family='TIMES', size=22, weight='bold')
        self._recordCaloriesButton = tk.Button(self._bottomFrame, text='RECORD\nCALORIES', font=self._bottomFont)
        self._recordCaloriesButton.config(command=lambda: terminal(1), highlightbackground='firebrick4', relief='flat')
        self._recordCaloriesButton.grid(row=0, column=0, sticky='nsew', padx=(18, 2), pady=(14, 4))
        self._trackCaloriesButton = tk.Button(self._bottomFrame, text='VIEW\nCALORIES\nLOG', font=self._bottomFont)
        self._trackCaloriesButton.config(command=lambda: terminal(2), highlightbackground='springgreen4', relief='flat')
        self._trackCaloriesButton.grid(row=0, column=1, sticky='nsew', padx=(2, 18), pady=(14, 4))
        self._recordWorkoutButton = tk.Button(self._bottomFrame, text='RECORD\nWORKOUT', font=self._bottomFont)
        self._recordWorkoutButton.config(command=lambda: terminal(3), highlightbackground='mediumpurple2', relief='flat')
        self._recordWorkoutButton.grid(row=1, column=0, sticky='nsew', padx=(18, 2), pady=(4, 14))
        self._trackWorkoutButton = tk.Button(self._bottomFrame, text='VIEW\nWORKOUT\nLOG', font=self._bottomFont)
        self._trackWorkoutButton.config(command=lambda: terminal(4), highlightbackground='lightpink2', relief='flat')
        self._trackWorkoutButton.grid(row=1, column=1, sticky='nsew', padx=(2, 18), pady=(4, 14))
        self._bottomFrame.pack(fill=tk.BOTH, expand=True, padx=18, pady=8)

        # Main-Menu window attributes.
        self._master.title('WOCAL_DB')
        self._master.focus_set()
        self._master.config(bg='royalblue2')
        self._master.minsize(600, 400)
        self._master.mainloop()

    def inputCalories(self, window):

        # calPerDay Attributes.
        self._amount = None
        self._desc = None
        self._date = None
        self._totalCalories = 0.0  # total Calories for selected day.

        # [2] Styling methods binded for the 2 entries within frame.
        def amountEntry_Focus(event):
            if self._amountEntry.get() == 'Enter Calorie Amount':
                self._amountEntry.delete(0, tk.END)
                self._amountEntry.insert(0, '')
                self._amountEntry.config(bg='mistyrose', fg='gray25')
            elif self._amountEntry.get() == '':
                self._amountEntry.insert(0, 'Enter Calorie Amount')
                self._amountEntry.config(bg='bisque', fg='gray25')

        def descBox_Focus(event):
            if self._descEntry.get() == 'Enter Desc. (optional)':
                self._descEntry.delete(0, tk.END)
                self._descEntry.insert(0, '')
                self._descEntry.config(bg='mistyrose', fg='gray25')
            elif self._descEntry.get() == '':
                self._descEntry.insert(0, 'Enter Desc. (optional)')
                self._descEntry.config(bg='bisque', fg='gray25')

        # Update labels to match calender selection.
        def updateDay():
            self._totalCalories = 0.0
            self._topLabel2.config(text=self._cal.selection_get())

            for self._records in self.calPerDay.find({'date': str(self._cal.selection_get())}):
                self._totalCalories += self._records['amount']

            self._dayTotalLabel.config(text='Day Total: {0}'.format(float(self._totalCalories)))
            self._master.after(1, self._master.update())

        # Return back to main-menu.
        def back():
            self._master.destroy()
            self._master.quit()
            self._root = tk.Tk()
            self.methodsScreen(self._root)
            self._root.mainloop()

        # Method inserts window entries into database.
        def insertDocument():
            try:
                # Attempt to insert document.
                if self._amountEntry != 'Enter Calorie Amount:':
                    if str(self._descEntry.get()) == 'Enter Desc. (optional)':
                        self._desc = ''
                    else:
                        self._desc = str(self._descEntry.get())
                    self._query = {'date': str(self._cal.selection_get()), 'amount': float(self._amountEntry.get()), 'desc': self._desc}
                    self._insert = self.calPerDay.insert_one(self._query)

                    # Transition back to main-menu.
                    self._master.destroy()
                    self._master.quit()
                    self.root = tk.Tk()
                    self.methodsScreen(self.root)
                    self.root.mainloop()

            except ValueError:

                def goBack():
                    self._alert.destroy()
                    self._alert.quit()

                # Alert Error Window.
                self._alert = tk.Tk()
                self._alert.title('INSERT ERROR')

                self._topLabel = tk.Label(self._alert, text='Error Encountered whilst inserting document.', fg='bisque', bg='gray25')
                self._topLabel.pack(fill=tk.BOTH, padx=18, pady=10, expand=True)

                self._closeButton = tk.Button(self._alert, text='CLOSE', font='HELVETICA 20 bold', command=lambda: goBack(), relief='raised')
                self._closeButton.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

                # Alert window attributes.
                self._alert.config(bg='indianred')
                self._alert.minsize(300, 150)
                self._alert.resizable(False, False)
                self._alert.mainloop()

        # Input Calories Window.
        self._master = window

        # Top Frame.
        self._topFrame = tk.Frame(self._master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
        self._topFont = font.Font(self._topFrame, family='TIMES', size=22, weight='bold', underline=True)
        self._topLabel = tk.Label(self._topFrame, text='SELECT DATE', bg='gray25', fg='ivory', font=self._topFont)
        self._topLabel.pack(padx=18, pady=(14, 0), fill=tk.BOTH)
        self._cal = Calendar(self._topFrame, selectmode='day', year=self.currentDate.year, month=self.currentDate.month, day=self.currentDate.day)
        self._cal.config(firstweekday='sunday', showweeknumbers=False, foreground='firebrick4', background='ivory', selectforeground='orange', showothermonthdays=False)
        self._cal.pack(padx=30, fill=tk.BOTH, expand=True)
        self._dayTotalLabel = tk.Label(self._topFrame, text='Day Total:' + str(self._totalCalories), font='TIMES 14 bold', bg='lavender')
        self._dayTotalLabel.pack(fill=tk.Y, padx=25, pady=(14, 0))
        self._topFont = font.Font(self._topFrame, family='TIMES', size=22, weight='bold', underline=True)
        self._topLabel2 = tk.Label(self._topFrame, text=self._cal.selection_get(), bg='lightcyan', fg='gray25', font=self._topFont)
        self._topLabel2.pack(padx=18, pady=14, fill=tk.Y)
        self._topFrame.pack(fill=tk.BOTH, padx=18, pady=(8, 4), expand=True)

        # Middle Frame
        self._middleFrame = tk.Frame(self._master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
        self._amountEntry = tk.Entry(self._middleFrame, justify='center', font='HELVETICA 16 bold', bg='bisque', fg='gray25')
        self._amountEntry.pack(padx=20, fill=tk.X, expand=True, pady=(14, 0))
        self._amountEntry.insert(0, 'Enter Calorie Amount')
        self._middleFont = font.Font(self._middleFrame, family='TIMES NEW ROMAN', size=16, weight='normal')
        self._descEntry = tk.Entry(self._middleFrame, justify='center', font=self._middleFont, bg='bisque', fg='gray25')
        self._descEntry.pack(padx=18, pady=14, fill=tk.BOTH)
        self._descEntry.insert(0, 'Enter Desc. (optional)')
        self._middleFrame.pack(fill=tk.BOTH, padx=18, expand=True, pady=10)

        # Bottom Frame
        self._bottomFrame = tk.Frame(self._master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
        self._bottomFrame.grid_rowconfigure(0, weigh=1)
        self._bottomFrame.grid_rowconfigure(1, weight=1)
        self._bottomFrame.grid_columnconfigure(0, weight=1)
        self._addButton = tk.Button(self._bottomFrame, text='INSERT', font='HELVETICA 16 bold', highlightbackground='mediumaquamarine')
        self._addButton.config(fg='snow', relief='raised')
        self._addButton.config(command=lambda: insertDocument())
        self._addButton.grid(row=0, column=0, sticky='nsew', padx=18, pady=4)
        self._backButton = tk.Button(self._bottomFrame, text='BACK', font='HELVETICA 16 bold')
        self._backButton.config(command=lambda: back(), highlightbackground='indianred', fg='snow', relief='raised')
        self._backButton.grid(row=1, column=0, sticky='nsew', padx=18, pady=4)
        self._bottomFrame.pack(fill=tk.BOTH, padx=18, pady=(0, 8), expand=True)

        # Input Calories window attributes.
        self._master.config(bg='royalblue2')
        self._master.title('RECORD CALORIES')
        self._master.bind('<<CalendarSelected>>', lambda cmd: updateDay())
        self._amountEntry.bind('<FocusIn>', amountEntry_Focus)
        self._amountEntry.bind('<FocusOut>', amountEntry_Focus)
        self._descEntry.bind('<FocusIn>', descBox_Focus)
        self._descEntry.bind('<FocusOut>', descBox_Focus)
        self._master.minsize(500, 550)
        self._master.mainloop()

    def inputWorkout(self, window):
        self._master = window
        self._master.mainloop()
    def viewCalories(self, window):
        self._master = window
        self._master.mainloop()
    def viewWorkout(self, window):
        self._master = window
        self._master.mainloop()

# Execute Program.
if __name__ == '__main__':
    master = tk.Tk()
    woCal = WoCal(master)
    master.mainloop()
