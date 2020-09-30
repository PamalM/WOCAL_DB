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

    # Method inserts calorie(s) amount & description into db, for given day.
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

        # Run update calories for pre-selected day (today) upon entry into window.
        updateDay()

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

    # Method inserts workout(s) log into db for given day.
    def inputWorkout(self, window):

        # [2] Styling method for weight and rep entries.
        def weightEntry_Focus(event):
            if str(self._weightEntry.get()) == 'Weight (lbs)':
                self._weightEntry_tkvar.set('')
            elif str(self._weightEntry.get()) == '':
                self._weightEntry_tkvar.set('Weight (lbs)')

        def repEntry_Focus(event):
            if str(self._repEntry.get()) == '# Reps':
                self._repEntry_tkvar.set('')
            elif str(self._repEntry.get()) == '':
                self._repEntry_tkvar.set('# Reps')

        # Return back to main-menu.
        def back():
            self._master.destroy()
            self._master.quit()
            self._root = tk.Tk()
            self.methodsScreen(self._root)
            self._root.mainloop()

        def updateWorkoutList():
            self._bodyGroup = str(self._selectedMuscleGroup.get())
            self._array = []
            if self._bodyGroup == 'CHEST' or 'BACK' or 'SHOULDERS' or 'ARMS' or 'ABS' or 'LEGS':
                self._label2['state'] = 'normal'
                self._workoutSelector['state'] = 'normal'
                self._workoutSelector['menu'].delete(0, tk.END)

                # (Assigning tags to each muscle Group) Chest = 1, Back = 2, Shoulders = 3, Arms = 4, Abs = 5, Legs = 6.
                self._muscleG_Tags = {1: self._chestWorkouts, 2: self._backWorkouts, 3: self._shoulderWorkouts, 4: self._armWorkouts, 5: self._coreWorkouts, 6: self._legsWorkouts}
                self._muscleTag = 0

                if self._bodyGroup == 'CHEST':
                    self._workout.set(self._chestWorkouts[0])
                    self._muscleTag = 1
                elif self._bodyGroup == 'BACK':
                    self._workout.set(self._backWorkouts[0])
                    self._muscleTag = 2
                elif self._bodyGroup == 'SHOULDERS':
                    self._workout.set(self._shoulderWorkouts[0])
                    self._muscleTag = 3
                elif self._bodyGroup == 'ARMS':
                    self._workout.set(self._armWorkouts[0])
                    self._muscleTag = 4
                elif self._bodyGroup == 'ABS':
                    self._workout.set(self._coreWorkouts[0])
                    self._muscleTag = 5
                elif self._bodyGroup == 'LEGS':
                    self._workout.set(self._legsWorkouts[0])
                    self._muscleTag = 6

                for item in self._muscleG_Tags.get(self._muscleTag):
                    self._array.append(item)

                self._workoutSelector.pack_forget()
                #self._workout = tk.StringVar()
                self._workoutSelector = tk.OptionMenu(self._middleFrame, self._workout, *self._array, command=lambda cmd: updateSetRepBox())
                self._workoutSelector['menu'].config(font=('calibri', 20), relief='raised', bd=4)
                self._workout.set('-')
                self._workoutSelector.grid(row=3, column=0, sticky='ew', padx=6, pady=(0, 12))

        # Enables (unlocks) all widgets when user fills out form correctly.
        def updateSetRepBox():
            self._setRepBox['state'] = 'normal'
            self._label3['state'] = 'normal'
            self._setRepBox['bg'] = 'snow'
            self._addRow['state'] = 'normal'
            self._weightEntry['state'] = 'normal'
            self._repEntry['state'] = 'normal'

        # Insert (+) set into selected workout.
        def addRows():
            try:
                self._setNum += 1
                if str(self._weightEntry.get()) != 'Weight (lbs)':
                    try:
                        self._sets.append(int(self._setNum))
                        self._reps.append(int(self._repEntry.get()))
                        self._weights.append(float(self._weightEntry.get()))
                        self._setRepBox.insert(tk.END, 'Set {0}: {1} Reps - {2} lbs.'.format(self._setNum, self._repEntry.get(), self._weightEntry.get()))
                    except ValueError:
                        raise ValueError
                else:
                    try:
                        self._sets.append(int(self._setNum))
                        self._reps.append(int(self._repEntry.get()))
                        self._weights.append(0.0)
                        self._setRepBox.insert(tk.END, 'Set {0}: {1} Reps'.format(self._setNum, self._repEntry.get()))
                    except ValueError:
                        raise ValueError
                self._repEntry_tkvar.set('')
                if self._setNum > 0:
                    self._delRow['state'] = 'normal'
                    self._addButton['state'] = 'normal'
                else:
                    self._delRow['state'] = 'disabled'
                    self._addButton['state'] = 'disabled'
                self._master.update()

            except ValueError:
                self._setNum -= 1

                def closeWindow():
                    self._alertWindow.destroy()
                    self._alertWindow.quit()

                self._alertWindow = tk.Tk()

                self._label1 = tk.Label(self._alertWindow, text='Please ensure you have entered a \nvalid rep amount and weight amount. ', fg='ivory', bg='indianred3')
                self._label1.config(font='HELVETICA 16 bold')
                self._label2 = tk.Label(self._alertWindow, text='If no weight for the workout, than leave entry as is!')
                self._label2.config(bg='indianred3', fg='bisque', font='HELVETICA 12 bold')
                self._label1.pack(pady=(10, 6), padx=20, fill=tk.X)
                self._label2.pack(padx=20, fill=tk.X)
                self._closeButton = tk.Button(self._alertWindow, text='CLOSE MESSAGE', font='HELVETICA 16 bold', highlightbackgroun='gray25', fg='ivory')
                self._closeButton.config(command=lambda: closeWindow())
                self._closeButton.pack(fill=tk.X, padx=20, pady=10)

                # Alert window attributes.
                self._alertWindow.config(bg='indianred3')
                self._alertWindow.title('ALERT')
                self._alertWindow.minsize(350, 150)
                self._alertWindow.resizable(False, False)
                self._alertWindow.bind('<Return>', lambda cmd: closeWindow())
                self._alertWindow.mainloop()

        # Delete (-) set from selected workout.
        def delRows():
            self._setNum -= 1
            if self._setNum > 0:
                self._delRow['state'] = 'normal'
                self._addButton['state'] = 'normal'
            else:
                self._delRow['state'] = 'disabled'
                self._addButton['state'] = 'disabled'

            self._master.update()
            self._setRepBox.delete(tk.END)
            self._sets.pop()
            self._reps.pop()
            self._weights.pop()

        # Insert workout statistics into db, for given day.
        def insertDocument():
            self._bodyGroup = str(self._selectedMuscleGroup.get())
            self._workout = str(self._workout.get())
            self._reps = self._reps
            self._sets = self._sets
            self._weights = self._weights
            self._date = datetime.date(int(self._cal.selection_get().year),
                                       int(self._cal.selection_get().month),
                                       int(self._cal.selection_get().day)).strftime('%Y-%m-%d')

            # Prepare and insert query into DB collection.
            self._query = {'date': self._date, 'muscleGroup': self._bodyGroup, 'workout': self._workout,
                           'sets': self._sets, 'reps': self._reps, 'weight': self._weights}
            self._insert = self.workoutPerDay.insert_one(self._query)

            # Transition back to main-menu.
            self._master.destroy()
            self._master.quit()
            self.root = tk.Tk()
            self.methodsScreen(self.root)
            self.root.mainloop()

        # workoutPerDay attributes.
        self._date = None
        self._muscleGroup = None
        self._workout = None
        self._sets = []
        self._reps = []
        self._weights = []

        # Tracker variables that holds the number of sets (entires) in the listbox.
        self._setNum = 0

        # Lists containing the valid (current) workouts and muscleGroups the user can select from.
        self._muscleGroups = ['CHEST', 'BACK', 'SHOULDERS', 'ARMS', 'ABS', 'LEGS']
        self._chestWorkouts = ['Push-ups', 'DB Bench Press', 'DB One-Arm Hammer Press', 'DB Fly']
        self._backWorkouts = ['Barbell Bent-Over Row', 'DB One-Arm Row', 'Barbell Reverse Grip Bent-Over Row']
        self._shoulderWorkouts = ['DB Shoulder Press', 'DB Shrugs', 'DB Alt. Deltoid Raises']
        self._armWorkouts = ['DB Concentration Curls', 'DB Hammer Curls', 'DB Seated Bent-over Tricep Exts.', 'Barbell Trciep Extensions']
        self._coreWorkouts = ['Sit-ups', 'V-ups', 'Scissor Kicks']
        self._legsWorkouts = ['Glute Kickbacks', 'DB Lunges', 'DB Seated Calf Raises']

        # Input workout window.
        self._master = window

        # Top Frame.
        self._topFrame = tk.Frame(self._master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
        self._topFont = font.Font(self._topFrame, family='TIMES', size=22, weight='bold', underline=True)
        self._topLabel1 = tk.Label(self._topFrame, text='SELECT DATE', bg='gray25', fg='ivory', font=self._topFont)
        self._topLabel1.pack(padx=18, pady=(14, 0), fill=tk.BOTH)
        self._cal = Calendar(self._topFrame, selectmode='day', year=self.currentDate.year, month=self.currentDate.month, day=self.currentDate.day)
        self._cal.config(firstweekday='sunday', showweeknumbers=False, foreground='firebrick4', background='ivory', selectforeground='orange', showothermonthdays=False)
        self._cal.pack(padx=30, fill=tk.BOTH, expand=True)
        self._topFont2 = font.Font(self._topFrame, family='TIMES', size=22, weight='bold', underline=True)
        self._topLabel2 = tk.Label(self._topFrame, text=self._cal.selection_get(), bg='lightcyan', fg='gray25', font=self._topFont2)
        self._topLabel2.pack(padx=18, pady=14, fill=tk.Y)
        self._topFrame.pack(fill=tk.BOTH, padx=18, pady=8, expand=True)

        # Middle Frame.
        self._middleFrame = tk.Frame(self._master, relief='raised', bd=4, highlightbackground='gray30', bg='bisque')
        self._middleFrame.grid_columnconfigure(0, weight=1)
        self._middleFrame.grid_columnconfigure(1, weight=1)
        self._middleFrame.grid_columnconfigure(2, weight=1)
        self._middleFrame.grid_rowconfigure(0, weight=1)
        self._middleFrame.grid_rowconfigure(1, weight=1)
        self._middleFrame.grid_rowconfigure(2, weight=1)
        self._middleFrame.grid_rowconfigure(3, weight=1)
        self._label1 = tk.Label(self._middleFrame, text='1. SELECT BODY GROUP:', font='TIMESNEWROMAN 16 bold', bg='gray25', fg='ivory')
        self._label1.grid(row=0, column=0, sticky='nsew', padx=8, pady=(12, 0))
        self._selectedMuscleGroup = tk.StringVar()
        self._muscleGroupSelector = tk.OptionMenu(self._middleFrame, self._selectedMuscleGroup, *self._muscleGroups, command=lambda cmd: updateWorkoutList())
        self._muscleGroupSelector['menu'].config(font=('calibri', 20), relief='raised', bd=4)
        self._selectedMuscleGroup.set('-')
        self._muscleGroupSelector.grid(row=1, column=0, sticky='ew', padx=8)
        self._label2 = tk.Label(self._middleFrame, text='2. SELECT WORKOUT:', font='TIMESNEWROMAN 16 bold', bg='gray25', fg='ivory', state='disabled')
        self._label2.grid(row=2, column=0, sticky='ew', padx=8)
        self._workout = tk.StringVar()
        self._workoutSelector = tk.OptionMenu(self._middleFrame, self._workout, [], command=lambda cmd: updateSetRepBox())
        self._workoutSelector['menu'].config(font=('calibri', 20), relief='raised', bd=4)
        self._workoutSelector['state'] = 'disabled'
        self._workout.set('-')
        self._workoutSelector.grid(row=3, column=0, sticky='ew', padx=8, pady=(0, 12))
        self._label3 = tk.Label(self._middleFrame, text='3. ENTER SETS/REPS:', font='TIMESNEWROMAN 16 bold', bg='gray25', fg='ivory', state='disabled')
        self._label3.grid(row=0, column=1, sticky='nsew', padx=8, pady=(12, 0), columnspan=2)
        self._setRepBox = tk.Listbox(self._middleFrame, state='disabled', bg='ivory')
        self._setRepBox.grid(row=1, column=1, sticky='nsew', padx=8, pady=12, rowspan=1, columnspan=2)
        self._repEntry_tkvar = tk.StringVar()
        self._repEntry = tk.Entry(self._middleFrame, justify='center', font='HELVETICA 20 bold', text=self._repEntry_tkvar, state='disabled')
        self._repEntry_tkvar.set('# Reps')
        self._repEntry.grid(row=2, column=1, sticky='nsew', padx=8, pady=12, columnspan=1)
        self._weightEntry_tkvar = tk.StringVar()
        self._weightEntry = tk.Entry(self._middleFrame, justify='center', font='HELVETICA 20 bold', text=self._weightEntry_tkvar, state='disabled')
        self._weightEntry_tkvar.set('Weight (lbs)')
        self._weightEntry.grid(row=2, column=2, sticky='nsew', padx=8, pady=12)
        self._addRow = tk.Button(self._middleFrame, text='(+) Set', font='HELVETICA 14 bold', highlightbackground='green')
        self._addRow.config(state='disabled', command=lambda: addRows())
        self._addRow.grid(row=3, column=2, sticky='nsew', padx=8, pady=8)
        self._delRow = tk.Button(self._middleFrame, text='(-) Set', font='HELVETICA 14 bold', highlightbackground='indianred3')
        self._delRow.config(state='disabled', command=lambda: delRows())
        self._delRow.grid(row=3, column=1, sticky='nsew', padx=8, pady=8)
        self._middleFrame.pack(fill=tk.BOTH, padx=18, pady=8, expand=True)

        # Bottom Frame.
        self._bottomFrame = tk.Frame(self._master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
        self._bottomFrame.grid_rowconfigure(0, weigh=1)
        self._bottomFrame.grid_rowconfigure(1, weight=1)
        self._bottomFrame.grid_columnconfigure(0, weight=1)
        self._addButton = tk.Button(self._bottomFrame, text='INSERT', font='HELVETICA 16 bold')
        self._addButton.config(highlightbackground='mediumaquamarine', fg='snow', relief='raised')
        self._addButton.config(command=lambda: insertDocument(), state='disabled')
        self._addButton.grid(row=0, column=0, sticky='nsew', padx=18, pady=4)
        self._backButton = tk.Button(self._bottomFrame, text='BACK', font='HELVETICA 16 bold', command=lambda: back())
        self._backButton.config(highlightbackground='indianred', fg='snow', relief='raised')
        self._backButton.grid(row=1, column=0, sticky='nsew', padx=18, pady=4)
        self._bottomFrame.pack(fill=tk.BOTH, padx=18, pady=8, expand=True)

        # Input Workout window attributes.
        self._master.title('RECORD WORKOUT')
        self._master.config(bg='mediumpurple2')
        self._master.bind('<<CalendarSelected>>', lambda cmd: self._master.after(1, self._topLabel2.config(text=self._cal.selection_get())))
        self._repEntry.bind('<FocusIn>', repEntry_Focus)
        self._repEntry.bind('<FocusOut>', repEntry_Focus)
        self._weightEntry.bind('<FocusIn>', weightEntry_Focus)
        self._weightEntry.bind('<FocusOut>', weightEntry_Focus)
        self._master.minsize(750, 750)
        self._master.mainloop()

    # Method allows user to view calories/desc trend for specific day, today, previous 7-days, or month.
    def viewCalories(self, window):

        # Styling method for entry.
        def specDayEntry_Focus(event):
            if self._specDayEntry.get() == 'MM/DD/YYYY':
                self._specDayEntry.delete(0, tk.END)
                self._specDayEntry.insert(0, '')
                self._specDayEntry.config(bg='powderblue', fg='gray25')
            elif self._specDayEntry.get() == '':
                self._specDayEntry.insert(0, 'MM/DD/YYYY')
                self._specDayEntry.config(bg='lightblue3', fg='gray25')

        # Function returns user's average calories intake for all entries within the db.
        def averageCalories():
            try:
                self._dayTotal = 0.0
                self._numEntries = self.calPerDay.estimated_document_count()
                for self._records in self.calPerDay.find():
                    self._dayTotal += self._records['amount']

                self._averageCalories = self._dayTotal / self._numEntries
                return round(self._averageCalories, 2)

                # If no entries in the db.
            except ZeroDivisionError:
                return 0.0

        # Back to main-menu.
        def back():
            self._master.destroy()
            self._master.quit()
            self._root = tk.Tk()
            self.methodsScreen(self._root)
            self._root.mainloop()

        # Method binded to specific Day entry. Extract date from entry and view calories for that specific date.
        def specDayEntryBind():
            try:
                self._grab = str(self._specDayEntry.get()).split('/')
                self._enteredDate = datetime.datetime(int(self._grab[2]), int(self._grab[0]), int(self._grab[1])).strftime('%Y-%m-%d')
                viewDay(1, self._enteredDate)

            except (ValueError, IndexError) as e:

                def close():
                    self._valErrorWin.destroy()
                    self._valErrorWin.quit()

                self._valErrorWin = tk.Tk()

                self._font1 = font.Font(family='TIMES NEW ROMAN', size=22, weight='bold')
                self._label1 = tk.Label(self._valErrorWin, text='Couldn\'t process that date.\nPlease try again!', font=self._font1)
                self._label1.pack(padx=20, fill=tk.BOTH, pady=10)

                self._closeButton = tk.Button(self._valErrorWin, text='CLOSE', font='HELVETICA 18 bold', highlightbackground='gray40', fg='ivory')
                self._closeButton.config(relief='raised', command=lambda: close())
                self._closeButton.pack(fill=tk.X, padx=20, pady=10)

                self._valErrorWin.title('ALERT!')
                self._valErrorWin.minsize(300, 100)
                self._valErrorWin.resizable(False, False)
                self._valErrorWin.config(bg='indianred3')
                self._valErrorWin.mainloop()

        # View calories amount/descriptions for specific day. (If tag=0; View today, else tag=1, provide specific date).
        def viewDay(tag, *args):

            def back():
                self._alpha.destroy()
                self._alpha.quit()
                self._root = tk.Tk()
                self.viewCalories(self._root)
                self._root.mainloop()

            # View today.
            if tag == 0:
                self._date = datetime.datetime(self.currentDate.year, self.currentDate.month, self.currentDate.day).strftime('%Y-%m-%d')

            # View specific date from supplied *arguments.
            elif tag == 1:
                self._args = []
                for self._item in args:
                    self._args.append(self._item)
                self._date = self._args[0]

            # Transition to next GUI.
            self._master.destroy()
            self._master.quit()

            self._alpha = tk.Tk()

            # Empty lists; To be filled with data from query result from db (done below).
            self._calories = []
            self._descriptions = []

            # Fill empty arrays. calories[n] corresponds to descriptions[n].
            for self._docs in self.calPerDay.find({'date': self._date}):
                self._calories.append(self._docs['amount'])
                self._descriptions.append(self._docs['desc'])

            # Find total calories for the specified day.
            self._totalCals = 0.0
            for self._cals in self._calories:
                self._totalCals += self._cals

            # Display above information in window.
            self._topFrame = tk.Frame(self._alpha, bg='gray25', bd=4, relief='ridge')
            self._listBoxFont = font.Font(family='TIMES NEW ROMAN', size=18, weight='bold')
            self._listBox = tk.Listbox(self._topFrame, bg='antiquewhite', font=self._listBoxFont, justify='center')
            # Insert data into listbox.
            self._descNum = 0
            for self._index in range(0, len(self._calories)):
                self._descNum += 1
                if self._descriptions[self._index] != '':
                    self._listBox.insert(tk.END, self._descriptions[self._index])
                else:
                    self._listBox.insert(tk.END, 'Item ' + str(self._descNum) + ":")
                self._listBox.insert(tk.END, self._calories[self._index])
            self._listBox.pack(padx=20, pady=(20, 5), fill=tk.BOTH)
            # Add differing colors for desc. and amounts within the listbox.
            for item in range(0, self._listBox.size()):
                if item % 2 == 0:
                    self._listBox.itemconfig(item, bg='lightpink3')
            if self._listBox.size() == 0:
                self._listBox.insert(0, 'NO DATA')
                self._listBox.itemconfig(0, bg='indianred3', fg='ivory')

            self._topFont = font.Font(family='TIMES NEW ROMAN', size=18, weight='bold')
            self._topLabel = tk.Label(self._topFrame, text='Total Calories:', font=self._topFont, bg='steelblue1', relief='ridge')
            self._topLabel.pack(padx=20, pady=(5, 5), fill=tk.BOTH)
            self._totalCalLabel = tk.Label(self._topFrame, text=self._totalCals, font=self._topFont, relief='raised')
            self._totalCalLabel.pack(padx=20, pady=(5, 20), fill=tk.BOTH)
            self._topFrame.pack(padx=20, pady=(20, 10), fill=tk.BOTH, expand=True)

            self._bottomFrame = tk.Frame(self._alpha, bg='gray25', highlightbackground='ivory')
            self._backButton = tk.Button(self._bottomFrame, text='BACK', font='HELVETICA 20 bold', highlightbackground='indianred3')
            self._backButton.config(command=lambda: back(), fg='ivory')
            self._backButton.config(relief='raised')
            self._backButton.pack(fill=tk.BOTH, padx=20, pady=20)
            self._bottomFrame.pack(padx=20, pady=(10, 20), fill=tk.BOTH)

            self._alpha.minsize(400, 400)
            self._alpha.config(bg='darkslateblue')
            self._alpha.title(self._date)
            self._alpha.mainloop()

        def sevenDayForecast():
            # Set pointer to today's date and work backwords.
            self._year = self.currentDate.year
            self._month = self.currentDate.month
            self._day = self.currentDate.day

            self._sevenDays = []
            # Set initially to todays date, and add the previous 7 days into a list.
            self._date = datetime.date(int(self._year), int(self._month), int(self._day))
            for x in range(1, 8):
                self._sevenDays.append(self._date.strftime('%Y-%m-%d'))
                self._date += datetime.timedelta(days=-1)

            # list to hold calories total calories for previous 7 days. (should have 7 elements @ end of exec.)
            self._sevenDaycalories = []

            # Fill calories list for last 7 days.
            for self._dates in self._sevenDays:
                self._dayTotal = 0.0
                for self._calorie in self.calPerDay.find({'date': self._dates}):
                    self._dayTotal += self._calorie['amount']
                self._sevenDaycalories.append(self._dayTotal)

            # Plot the trend.
            self._ax = plt.axes()
            plt.xlabel('Date:')
            plt.ylabel('Calorie Amount:')
            plt.title('Previous 7-Days:')
            self._ax.xaxis.set_major_locator(plt.MultipleLocator(2))
            self._ax.yaxis.set_major_locator(plt.MultipleLocator(500))
            plt.scatter(self._sevenDays, self._sevenDaycalories, label='x', color='m', marker='o')
            plt.plot(self._sevenDays, self._sevenDaycalories, '-o', color='k')
            plt.gca().invert_xaxis()
            fig = plt.gcf()
            self._ax.set_facecolor('xkcd:sky')
            plt.rcParams['figure.facecolor'] = 'white'
            plt.ylim(0, 3750)
            fig.canvas.set_window_title('7-Day Calories Forecast:')
            plt.show()

        def thirtyDayForecast():
            self._year = self.currentDate.year
            self._month = self.currentDate.month
            self._day = self.currentDate.day

            self._thirtyDays = []
            self._date = datetime.date(int(self._year), int(self._month), int(self._day))
            for x in range(1, 31):
                self._thirtyDays.append(self._date.strftime('%Y-%m-%d'))
                self._date += datetime.timedelta(days=-1)

            self._thirtyDaycalories = []

            # Fill calories list for last 30 days.
            for self._dates in self._thirtyDays:
                self._dayTotal = 0.0
                for self._calorie in self.calPerDay.find({'date': self._dates}):
                    self._dayTotal += self._calorie['amount']
                self._thirtyDaycalories.append(self._dayTotal)

            # Plot the trend.
            self._ax = plt.axes()
            plt.xlabel('Date:')
            plt.ylabel('Calorie Amount:')
            plt.title('Previous 30-Days:')
            self._ax.xaxis.set_major_locator(plt.MultipleLocator(7))
            self._ax.yaxis.set_major_locator(plt.MultipleLocator(500))
            plt.scatter(self._thirtyDays, self._thirtyDaycalories, label='x', color='m', marker='o')
            plt.plot(self._thirtyDays, self._thirtyDaycalories, '-o', color='k')
            plt.gca().invert_xaxis()
            fig = plt.gcf()
            self._ax.set_facecolor('xkcd:sky')
            plt.rcParams['figure.facecolor'] = 'white'
            plt.ylim(0, 3750)
            fig.canvas.set_window_title('30-Day Calories Forecast:')
            plt.show()

        # calPerDay Attributes.
        self._amount = None
        self._desc = None
        self._date = None

        # View Calories Window.
        self._master = window

        # Top Frame.
        self._tFborder = tk.Frame(self._master, bg='thistle1')
        self._topFrame = tk.Frame(self._tFborder, bg='gray25')
        self._topFrame.grid_rowconfigure(0, weight=1)
        self._topFrame.grid_rowconfigure(1, weight=1)
        self._topFrame.grid_rowconfigure(2, weight=1)
        self._topFrame.grid_rowconfigure(3, weight=1)
        self._topFrame.grid_rowconfigure(4, weight=1)
        self._topFrame.grid_columnconfigure(0, weight=1)
        self._todayStatButton = tk.Button(self._topFrame, text='TODAY\'S CALORIES', font='HELVETICA 22 bold', highlightbackground='lightslateblue', fg='snow')
        self._todayStatButton.config(command=lambda: viewDay(0))
        self._todayStatButton.config(relief='raised', highlightthickness=4)
        self._todayStatButton.grid(row=0, column=0, sticky='nsew', pady=(20, 5), padx=25)
        self._last7DaysButton = tk.Button(self._topFrame, text='LAST 7 DAYS', font='HELVETICA 22 bold', highlightbackground='lightslateblue', fg='snow')
        self._last7DaysButton.config(relief='raised', highlightthickness=4, command=lambda: sevenDayForecast())
        self._last7DaysButton.grid(row=1, column=0, sticky='nsew', pady=5, padx=25)
        self._last30DaysButton = tk.Button(self._topFrame, text='LAST 30 DAYS', font='HELVETICA 22 bold', highlightbackground='lightslateblue', fg='snow')
        self._last30DaysButton.config(relief='raised', highlightthickness=4, command=lambda: thirtyDayForecast())
        self._last30DaysButton.config(relief='raised', highlightthickness=4)
        self._last30DaysButton.grid(row=2, column=0, sticky='nsew', pady=5, padx=25)
        self._topFont1 = font.Font(family='TIMES NEW ROMAN', size=16, weight='bold')
        self._bottomLabel = tk.Label(self._topFrame, text='Average calories (per day):', fg='snow', bg='mediumpurple4', font=self._topFont1)
        self._bottomLabel.config(relief='ridge', bd=6)
        self._bottomLabel.grid(row=3, column=0, sticky='nsew', pady=5, padx=25)
        self._topFont2 = font.Font(family='TIMES NEW ROMAN', size=20, weight='bold')
        self._bottomLabel2 = tk.Label(self._topFrame, text=averageCalories(), fg='gray25', bg='lightskyblue2', font=self._topFont2)
        self._bottomLabel2.config(relief='ridge', bd=4)
        self._bottomLabel2.grid(row=4, column=0, sticky='ns', pady=(5, 20), padx=5)
        self._topFrame.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)
        self._tFborder.pack(padx=20, pady=(20, 10), fill=tk.BOTH, expand=True)

        # Bottom Frame.
        self._bottomFrame = tk.Frame(self._master, bg='gray25')
        self._bottomFont = font.Font(family='TIMES NEW ROMAN', size=16, weight='bold')
        self._bottomLabel = tk.Label(self._bottomFrame, text='Search specific date:', font=self._bottomFont, bg='gray25', fg='ivory')
        self._bottomLabel.pack(padx=25, fill=tk.BOTH, pady=(10, 2), expand=True)
        self._specDayEntry = tk.Entry(self._bottomFrame, justify='center', bg='lightblue3', fg='gray25', font=self._bottomFont)
        self._specDayEntry.insert(0, 'MM/DD/YYYY')
        self._specDayEntry.pack(fill=tk.BOTH, expand=True, padx=25, pady=(2, 10))
        self._searchButton = tk.Button(self._bottomFrame, text='SEARCH', font='HELVETICA 14 bold', highlightbackground='palegreen3')
        self._searchButton.config(command=lambda: specDayEntryBind())
        self._searchButton.config(relief='raised')
        self._searchButton.pack(padx=25, pady=10, fill=tk.BOTH, expand=True)
        self._backButton = tk.Button(self._bottomFrame, text='BACK', font='HELVETICA 14 bold', highlightbackground='brown3', fg='snow')
        self._backButton.config(command=lambda: back())
        self._backButton.config(relief='ridge')
        self._backButton.pack(padx=25, pady=10, fill=tk.BOTH, expand=True)
        self._bottomFrame.pack(padx=20, pady=(10, 20), fill=tk.BOTH, expand=True)

        # View Calories Window Attributes.
        self._master.config(bg='seagreen3')
        self._master.title('View Calories')
        self._master.minsize(600, 500)
        self._specDayEntry.bind('<FocusIn>', specDayEntry_Focus)
        self._specDayEntry.bind('<FocusOut>', specDayEntry_Focus)
        self._master.bind('<Return>', lambda cmd: specDayEntryBind())
        self._master.mainloop()

    # Method allows user to view workout trends for specific day, today, previous 7-days, or month.
    def viewWorkout(self, window):

        # Back to main-menu.
        def back():
            self._master.destroy()
            self._master.quit()
            self.root = tk.Tk()
            self.methodsScreen(self.root)
            self.root.mainloop()

        # Styling method for entry.
        def specDayEntry_Focus(event):
            if self._specDayEntry.get() == 'MM/DD/YYYY':
                self._specDayEntry.delete(0, tk.END)
                self._specDayEntry.insert(0, '')
                self._specDayEntry.config(bg='powderblue', fg='gray25')
            elif self._specDayEntry.get() == '':
                self._specDayEntry.insert(0, 'MM/DD/YYYY')
                self._specDayEntry.config(bg='lightblue3', fg='gray25')

        # Method extracts date from entry and proceeds to next GUI.
        def specDayEntryBind():
            try:
                self._grab = str(self._specDayEntry.get()).split('/')
                self._m = int(self._grab[0])
                self._d = int(self._grab[1])
                self._y = int(self._grab[2])
                self._date = datetime.datetime(self._y, self._m, self._d).strftime('%Y-%m-%d')
                self._master.destroy()
                self._master.quit()
                viewDay(self._date)

            except (ValueError, IndexError) as e:

                def close():
                    self._valErrorWin.destroy()
                    self._valErrorWin.quit()

                self._valErrorWin = tk.Tk()

                self._font1 = font.Font(family='TIMES NEW ROMAN', size=22, weight='bold')
                self._label1 = tk.Label(self._valErrorWin, text='Couldn\'t process that date.\nPlease try again!', font=self._font1)
                self._label1.pack(padx=20, fill=tk.BOTH, pady=10)

                self._closeButton = tk.Button(self._valErrorWin, text='CLOSE', font='HELVETICA 18 bold', highlightbackground='gray40', fg='ivory')
                self._closeButton.config(relief='raised', command=lambda: close())
                self._closeButton.pack(fill=tk.X, padx=20, pady=10)

                self._valErrorWin.title('ALERT!')
                self._valErrorWin.minsize(300, 100)
                self._valErrorWin.resizable(False, False)
                self._valErrorWin.config(bg='indianred3')
                self._valErrorWin.mainloop()

        # View workout log for specified day.
        def viewDay(date):
            # Close Window.
            def back():
                self._alpha.destroy()
                self._alpha.quit()
                self._root = tk.Tk()
                self.viewWorkout(self._root)
                self._root.mainloop()

            # Get workout results for that date.
            for self._docs in self.workoutPerDay.find({'date': date}):
                self._workout = {'date': date, 'muscleGroup': self._docs['muscleGroup'], 'workout': self._docs['workout'],
                              'sets': self._docs['sets'], 'reps': self._docs['reps'], 'weight': self._docs['weight']}
                self._workouts.append(self._workout)

            self._alpha = tk.Tk()

            self._topFrame = tk.Frame(self._alpha, bg='gray25', bd=4, relief='ridge')
            # Textbox to hold workout history.
            self._textBox = tk.Listbox(self._topFrame, justify='center', font='HELVECTICA 20 bold', bg='gray25', relief='groove', bd=4)

            try:
                for item in range(0, len(self._workouts)):
                    self._textBox.insert(tk.END, self._workouts[item]['workout'].upper())
                    self._textBox.itemconfig(tk.END, bg='mediumorchid2')
                    self._textBox.insert(tk.END, self._workouts[item]['muscleGroup'])
                    self._textBox.itemconfig(tk.END, bg='lightgoldenrod')
                    self._textBox.insert(tk.END, '{0} sets'.format(len(self._workouts[item]['sets'])))
                    self._textBox.itemconfig(tk.END, bg='ivory', fg='gray25')
                    self._textBox.insert(tk.END, '{0} reps'.format(self._workouts[item]['reps']))
                    self._textBox.itemconfig(tk.END, bg='ivory', fg='gray25')
                    self._textBox.insert(tk.END, '{0} lbs'.format(self._workouts[item]['weight']))
                    self._textBox.itemconfig(tk.END, bg='ivory', fg='gray25')
                    self._textBox.insert(tk.END, '')
                    self._textBox.itemconfig(tk.END, bg='indianred3')

            except IndexError:
                if self._textBox.size() == 0:
                    self._textBox.insert(0, 'NO DATA')
                    self._textBox.itemconfig(0, bg='indianred3', fg='ivory')
            finally:
                if self._textBox.size() == 0:
                    self._textBox.insert(0, 'NO DATA')
                    self._textBox.itemconfig(0, bg='indianred3', fg='ivory')

            self._textBox.pack(padx=25, pady=25, fill=tk.BOTH, expand=True)
            self._topFrame.pack(padx=20, pady=(20, 10), fill=tk.BOTH, expand=True)

            self._bottomFrame = tk.Frame(self._alpha, bg='gray25', highlightbackground='ivory')
            self._backButton = tk.Button(self._bottomFrame, text='BACK', font='HELVETICA 20 bold', highlightbackground='indianred3', fg='ivory', command=lambda: back())
            self._backButton.config(relief='raised')
            self._backButton.pack(fill=tk.BOTH, padx=20, pady=20, expand=True)
            self._bottomFrame.pack(padx=20, pady=(10, 20), fill=tk.BOTH, expand=True)

            self._alpha.title(date)
            self._alpha.config(bg='thistle1')
            self._alpha.minsize(500, 300)
            self._alpha.mainloop()

        # View workout trend for previous 7-days.
        def sevenDayForcast():

            # Back to View workout window.
            def closeWindow():
                self._alpha.destroy()
                self._alpha.quit()

            # User can view graph trend for specific workout for previous 7 days.
            # I choose to display each workout individually rather than scattering everything into one graph so its easier to read.
            def viewTrend():
                # Get selected workout.
                self._selectedWorkout = self._listbox.get(self._listbox.curselection())

                # Each date will have a list of reps/weights that correspond for that workout.
                self._dateLog = {'dates': [], 'reps': [], 'sets': []}

                self._reps = []
                self._weights = []
                self._dates = []

                # Filter results specifically for this workout only.
                for self._stat in self._workouts:
                    if self._stat['workout'].upper() == self._selectedWorkout:
                        for self._rep in self._stat['reps']:
                            self._reps.append(self._rep)
                            self._dateMsg = ''
                            for self._date in self._stat['date']:
                                self._dateMsg += self._date
                            self._dates.append(self._dateMsg)
                        for self._weight in self._stat['weight']:
                            self._weights.append(self._weight)
                        self._dateLog = {'date': self._dates, 'reps': self._reps, 'weights': self._weights}

                print(self._dateLog.get('date'))
                print(self._dateLog.get('reps'))

                self._alpha.after(1, self._alpha.update())

                # Plot the information collected above.
                plt.scatter(self._dateLog.get('date'), self._dateLog.get('reps'))
                plt.show()


            # Set pointer to today's date and work backwards.
            self._year = self.currentDate.year
            self._month = self.currentDate.month
            self._day = self.currentDate.day

            # Populate workouts list with previous 7 days of workouts.
            self._sevenDays = []
            self._date = datetime.date(int(self._year), int(self._month), int(self._day))
            for x in range(1, 8):
                self._sevenDays.append(self._date.strftime('%Y-%m-%d'))
                self._date += datetime.timedelta(days=-1)
            for self._day in self._sevenDays:
                for self._doc in self.workoutPerDay.find({'date': self._day}):
                    self._workout = {'date': self._day, 'muscleGroup': self._doc['muscleGroup'], 'workout': self._doc['workout'],
                                     'sets': self._doc['sets'], 'reps': self._doc['reps'], 'weight': self._doc['weight']}
                    self._workouts.append(self._workout)

            # 7 day forecast window.
            self._alpha = tk.Tk()

            self._topFrame = tk.Frame(self._alpha, bg='gray25')
            self._topLabel = tk.Label(self._topFrame, text='Select specific workout to view trend for:', font='HELVETICA 20 bold', bg='gray25', fg='mediumseagreen')
            self._topLabel.pack(fill=tk.X, padx=30, pady=(10, 4), expand=True)
            self._listbox = tk.Listbox(self._topFrame, font='TIMES 20 bold', justify='center', selectmode=tk.SINGLE)
            self._listbox.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
            # Fill listbox with data above. (Make sure to only show unique workouts, no duplicates)
            self._uniqueWorkouts = []
            for self._workout in self._workouts:
                self._uniqueWorkouts.append(self._workout['workout'])
            self._uniqueWorkouts = list(set(self._uniqueWorkouts))
            for self._workout in self._uniqueWorkouts:
                self._listbox.insert(tk.END, self._workout.upper())

            self._closeButton = tk.Button(self._topFrame, text='Close', highlightbackground='indianred', fg='ivory', font='HELVETICA 20 bold')
            self._closeButton.config(command=lambda: closeWindow(), relief='raised')
            self._closeButton.pack(fill=tk.BOTH, padx=20, pady=20, expand=True)
            self._topFrame.pack(fill=tk.BOTH, padx=20, pady=20, expand=True)

            # 7 day forecase window attributes.
            self._alpha.config(bg='lightskyblue1')
            self._listbox.bind("<<ListboxSelect>>", lambda cmd: viewTrend())
            self._alpha.title('Last 7 Days:')
            self._alpha.minsize(400, 400)
            self._alpha.mainloop()

        # workoutPerDay attributes.
        self._workout = {'date': '', 'muscleGroup': '', 'workout': '', 'sets': [], 'reps': [], 'weight': []}
        # Empty list will hold all the workouts that are returned in the query.
        self._workouts = []

        # View Workout Window.
        self._master = window

        self._tFborder = tk.Frame(self._master, bg='thistle1')
        self._topFrame = tk.Frame(self._tFborder, bg='gray25')
        self._topFrame.grid_rowconfigure(0, weight=1)
        self._topFrame.grid_rowconfigure(1, weight=1)
        self._topFrame.grid_rowconfigure(2, weight=1)
        self._topFrame.grid_rowconfigure(3, weight=1)
        self._topFrame.grid_rowconfigure(4, weight=1)
        self._topFrame.grid_columnconfigure(0, weight=1)
        self._todayStatButton = tk.Button(self._topFrame, text='TODAY\'S WORKOUT', font='HELVETICA 22 bold', highlightbackground='lightslateblue', fg='snow')
        self._todayStatButton.config(command=lambda: viewDay(datetime.datetime(self.currentDate.year, self.currentDate.month, self.currentDate.day).strftime('%Y-%m-%d')))
        self._todayStatButton.config(relief='raised', highlightthickness=4)
        self._todayStatButton.grid(row=0, column=0, sticky='nsew', pady=(20, 5), padx=25)
        self._last7DaysButton = tk.Button(self._topFrame, text='LAST 7 DAYS', font='HELVETICA 22 bold', highlightbackground='lightslateblue', fg='snow')
        self._last7DaysButton.config(relief='raised', highlightthickness=4, command=lambda: sevenDayForcast())
        self._last7DaysButton.grid(row=1, column=0, sticky='nsew', pady=5, padx=25)
        self._last30DaysButton = tk.Button(self._topFrame, text='LAST 30 DAYS', font='HELVETICA 22 bold', highlightbackground='lightslateblue', fg='snow')
        self._last30DaysButton.config(relief='raised', highlightthickness=4, command=lambda: print(''))
        self._last30DaysButton.config(relief='raised', highlightthickness=4)
        self._last30DaysButton.grid(row=2, column=0, sticky='nsew', pady=5, padx=25)
        self._topFrame.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)
        self._tFborder.pack(padx=20, pady=(20, 10), fill=tk.BOTH, expand=True)

        self._bottomFrame = tk.Frame(self._master, bg='gray25')
        self._bottomFont = font.Font(family='TIMES NEW ROMAN', size=16, weight='bold')
        self._bottomLabel = tk.Label(self._bottomFrame, text='Search specific date:', font=self._bottomFont, bg='gray25', fg='ivory')
        self._bottomLabel.pack(padx=25, fill=tk.BOTH, pady=(10, 2), expand=True)
        self._specDayEntry = tk.Entry(self._bottomFrame, justify='center', bg='lightblue3', fg='gray25', font=self._bottomFont)
        self._specDayEntry.insert(0, 'MM/DD/YYYY')
        self._specDayEntry.pack(fill=tk.BOTH, expand=True, padx=25, pady=(2, 10))
        self._searchButton = tk.Button(self._bottomFrame, text='SEARCH', font='HELVETICA 14 bold', highlightbackground='palegreen3')
        self._searchButton.config(command=lambda: specDayEntryBind())
        self._searchButton.config(relief='raised')
        self._searchButton.pack(padx=25, pady=10, fill=tk.BOTH, expand=True)
        self._backButton = tk.Button(self._bottomFrame, text='BACK', font='HELVETICA 14 bold', highlightbackground='brown3', fg='snow')
        self._backButton.config(command=lambda: back())
        self._backButton.config(relief='ridge')
        self._backButton.pack(padx=25, pady=10, fill=tk.BOTH, expand=True)
        self._bottomFrame.pack(padx=20, pady=(10, 20), fill=tk.BOTH, expand=True)

        # View Workout Window attributes.
        self._master.config(bg='mediumpurple3')
        self._master.title('View Workout')
        self._master.minsize(600, 500)
        self._specDayEntry.bind('<FocusIn>', specDayEntry_Focus)
        self._specDayEntry.bind('<FocusOut>', specDayEntry_Focus)
        self._master.bind('<Return>', lambda cmd: specDayEntryBind())
        self._master.mainloop()

# Execute Program.
if __name__ == '__main__':
    master = tk.Tk()
    woCal = WoCal(master)
    master.mainloop()
