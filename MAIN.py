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


class WoCal:

    # Initiate WoCal object by signing into MongoDB.
    def __init__(self, window):

        self.master = window

        self.currentDate = datetime.datetime.now()

        # Login credentials.
        self._username = None
        self.password = None
        self.url = "mongodb+srv://{0}:{1}@wocal.szoqb.mongodb.net/WOCAL?retryWrites=true&w=majority"

        # Sign user into WoCal Collection in MongoDB.
        def signIn():
            try:
                # Setup connection; Authenticate user before advancing to next GUI (Graphical-User-Interface).
                self.username = str(self._usernameEntry.get())
                self.password = str(self._passwordEntry.get())
                if self.username != 'Enter Username' and self.password != 'Enter Password':
                    self.client = MongoClient(self.url.format(self.username, self.password))
                    try:
                        # WoCal = DB, workoutPerDay & calPerDay = Collections within WoCal.
                        self.client.admin.command('ismaster')
                        self.db = self.client['WOCAL']
                        self.workoutPerDay = self.db['workoutPerDay']
                        self.calPerDay = self.db['calPerDay']

                    # Direct user to the one error window for all general errors that may arise.
                    except ConnectionFailure:
                        raise ValueError
                    except OperationFailure:
                        raise ValueError

                    # Transition to next screen.
                    self.master.destroy()
                    self.master.quit()
                    print('[{0} has signed into the DB]'.format(self.username))

                    # Save user login credentials to text file if 'rememberMe' checkbutton is selected by user.
                    if self._rememberMe.get():
                        # Determine user's operating system, to ensure login.txt file is saved to project directory.
                        self.uMachine = system()
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
                            print('[login.txt couldn\'t be saved to the project directory.]]')

                    # Transfer to next screen.
                    self.root = tk.Tk()
                    self.methodsScreen(self.root)
                    self.root.mainloop()

            # Unable to establish connection; Notify user with alert window.
            except OperationFailure and ConnectionFailure and ValueError:
                print('[Authentication Error!]')
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
                self._alert.bind('<Return>', lambda cmd: self._alert.destroy())
                self._alert.mainloop()

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

        # Styling method for checkbutton.
        def remember():
            if self._rememberMe.get():
                self._rememberMeCheckBox.config(text='Remember login!', bg='azure2')
            else:
                self._rememberMeCheckBox.config(text='Stay signed-In?', bg='slategray3')

        # Determine user machine OS, and check if login.text file exists.
        self.uMachine = system()
        self.filename = None
        self.fileExists = None
        if self.uMachine == 'Darwin' or 'Linux':
            self.filename = os.getcwd() + '/login.txt'
            self.fileExists = os.path.exists(self.filename)
        elif self.uMachine == 'Windows':
            self.filename = os.getcwd() + '\\login.txt'
            self.fileExists = os.path.exists(self.filename)

        print('[Awaiting user sign-in for DB] ...')
        # Prompt user for sign-in:
        if not self.fileExists:
            # Top Frame.
            self._topFrame = tk.Frame(self.master, bg='gray25')
            self._font1 = font.Font(self._topFrame, family='HELVETICA', size=30, weight='bold', underline=True)
            self._topLabel1 = tk.Label(self._topFrame, text='Sign Into Database:', font=self._font1, bd=4, bg='lavender', fg='gray25')
            self._topLabel1.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
            self._topFrame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            # Middle Frame.
            self._middleFrame = tk.Frame(self.master, bg='slategray3', relief='raised', bd=4, highlightbackground='gray25')
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
            self._rememberMe = tk.BooleanVar(self.master)
            self._rememberMe.set(False)
            self._rememberMeCheckBox = tk.Checkbutton(self._middleFrame, text='Stay signed-In?', variable=self._rememberMe, command=remember, bg='slategray3')
            self._rememberMeCheckBox.grid(row=2, column=0, pady=(0, 14), sticky='ns', padx=20)
            self._signInButton = tk.Button(self._middleFrame, text='Sign In!', height=3, font='HELVETICA 20 bold', relief='ridge', bd=1, command=lambda: signIn())
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
            self._bottomFrame = tk.Frame(self.master, bg='gray25')
            self._bottomFont = font.Font(self._topFrame, family='TIMES NEW ROMAN', size=10)
            self._bottomLabel = tk.Label(self._bottomFrame, text='Powered through MongoDB\nCreated by Pamal Mangat', font=self._bottomFont, bg='lavender')
            self._bottomLabel.pack(fill=tk.BOTH, padx=18, pady=10, expand=True)
            self._bottomFrame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            # Sign-In Window attributes.
            self.master.title('WOCAL - SIGN IN')
            self.master.minsize(400, 500)
            self.master.config(bg='royalblue2')
            self.master.bind('<Return>', lambda cmd: signIn())
            self.master.mainloop()

        # Sign user into DB using saved credentials in login.txt.
        else:
            self._credentials = [0, 0]
            with open(self.filename, "r") as self.file:
                for line in self.file:
                    self._credentials = line.split(':')
                self._username = self._credentials[0]
                self._password = self._credentials[1]
            print('[Successful login for {0}, into the Database]'.format(self._username))
            self.url = "mongodb+srv://{0}:{1}@wocal.szoqb.mongodb.net/WOCAL?retryWrites=true&w=majority".format(self._username, self._password)
            self.client = MongoClient(self.url)
            self.client.admin.command('ismaster')
            # DB collections.
            self.db = self.client['WOCAL']
            self.workoutPerDay = self.db['workoutPerDay']
            self.calPerDay = self.db['calPerDay']
            self.methodsScreen(self.master)

    # Main-Menu for the program.
    def methodsScreen(self, window):

        self.master = window

        # Direct user to specific method depending on tag (specified by button).
        def terminal(tag):
            self.master.destroy()
            self.master.quit()
            self.root = tk.Tk()
            if tag == 1:
                self.recordCalories(self.root)
            elif tag == 2:
                self.viewCalories(self.root)
            elif tag == 3:
                self.recordWorkout(self.root)
            elif tag == 4:
                self.viewWorkout(self.root)
            self.root.mainloop()

        # Log user out of db, delete login.txt file if it exists.
        def logOff():
            try:
                self.master.destroy()
                self.master.quit()
                os.remove(self.filename)
                sleep(1)
                print("[{0} has been logged out of the database]".format(self.username))
            except FileNotFoundError:
                pass
            finally:
                self.root = tk.Tk()
                self.__init__(self.root)
                self.root.mainloop()

        # Top Frame.
        self._topFrame = tk.Frame(self.master, bg='gray25', relief='raised', bd=4, highlightbackground='gray30')
        self._topFrame.grid_rowconfigure(0, weight=1)
        self._topFrame.grid_columnconfigure(0, weight=1)
        self._topFrame.grid_columnconfigure(1, weight=1)
        self._topFrame.grid_rowconfigure(0, weight=1)
        self._topFrame.grid_columnconfigure(0, weight=1)
        self._topFrame.grid_columnconfigure(1, weight=1)
        self._topFont = font.Font(self._topFrame, family='Times NEW ROMAN', size=20, weight='bold', underline=False)
        self._welcomeLabel = tk.Label(self._topFrame, text='Welcome,\n{0}'.format(self._username), font=self._topFont, anchor='w', bg='gray25', fg='ivory')
        self._welcomeLabel.grid(row=0, column=0, sticky='ew', padx=18, pady=2)
        self._logOffButton = tk.Button(self._topFrame, text='LogOff', font='HELVETICA 18 bold', relief='raised', bd=2)
        self._logOffButton.config(command=lambda: logOff(), highlightbackground='indianred')
        self._logOffButton.grid(row=0, column=1, sticky='nsew', padx=18, pady=8)
        self._topFrame.pack(fill=tk.BOTH, expand=False, padx=18, pady=(14, 0))

        # Bottom Frame.
        self._bottomFrame = tk.Frame(self.master, bg='snow3', relief='raised', bd=4, highlightbackground='gray30')
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

        # Window attributes.
        self.master.title('WOCAL_DB')
        self.master.focus_set()
        self.master.config(bg='royalblue2')
        self.master.minsize(600, 400)
        self.master.mainloop()

    # Record calorie(s) for specific date.
    def recordCalories(self, window):

        self._amount = None
        self._desc = None
        self._date = None

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

        # Binded method updates label underneath calendar whenever date is selected.
        def updateDate():
            self._getSelectedDate = self._cal.selection_get()
            self._topLabel2.config(text=self._getSelectedDate)
            self._dayTotal = updateDayTotal()
            self._dayTotalLabel.config(text='Day Total: {0}'.format(self._dayTotal))
            self.master.after(1, self.master.update())

        # Method binded to backButton.
        def back():
            self.master.destroy()
            self.master.quit()
            self.root = tk.Tk()
            self.methodsScreen(self.root)
            self.root.mainloop()

        # Method returns the summed value of calories for the selected day.
        def updateDayTotal():
            self._dayTotal = 0.0
            for self.records in self.calPerDay.find({'date': str(self._cal.selection_get())}):
                self._dayTotal += self.records['amount']
            return float(self._dayTotal)

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
                    self.master.destroy()
                    self.master.quit()
                    self.root = tk.Tk()
                    self.methodsScreen(self.root)
                    self.root.mainloop()

            except ValueError:
                self._alert = tk.Tk()
                self._alert.title('INSERT ERROR')

                self._topLabel = tk.Label(self._alert, text='Error Encountered whilst inserting document.', fg='bisque', bg='gray25')
                self._topLabel.pack(fill=tk.X, padx=18, pady=10)

                self._alert.minsize(300, 150)
                self._alert.resizable(False, False)
                self._alert.mainloop()

        self.master = window

        # Top Frame.
        # Initial update for first time user logs into window. Label must be updated prior to entry.
        self.dayTotal = 0.0
        for records in self.calPerDay.find({'date': '{0}-{1}-{2}'.format(self.currentDate.year, self.currentDate.month, self.currentDate.day)}):
            self.dayTotal += float(records['amount'])
        # Calendar for user to pick date of record for calories.
        self._topFrame = tk.Frame(self.master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
        self._topFont = font.Font(self._topFrame, family='TIMES', size=22, weight='bold', underline=True)
        self._topLabel = tk.Label(self._topFrame, text='SELECT DATE', bg='gray25', fg='ivory', font=self._topFont)
        self._topLabel.pack(padx=18, pady=(14, 0), fill=tk.BOTH)
        self._cal = Calendar(self._topFrame, selectmode='day', year=self.currentDate.year, month=self.currentDate.month, day=self.currentDate.day)
        self._cal.config(firstweekday='sunday', showweeknumbers=False, foreground='firebrick4', background='ivory', selectforeground='orange', showothermonthdays=False)
        self._cal.pack(padx=30, fill=tk.BOTH, expand=True)
        self._dayTotalLabel = tk.Label(self._topFrame, text='Day Total: {0}'.format(updateDayTotal()), font='TIMES 14 bold', bg='lavender')
        self._dayTotalLabel.pack(fill=tk.Y, padx=25, pady=(14, 0))
        self._font2 = font.Font(self._topFrame, family='TIMES', size=22, weight='bold', underline=True)
        self._topLabel2 = tk.Label(self._topFrame, text=self._cal.selection_get(), bg='lightcyan', fg='gray25', font=self._font2)
        self._topLabel2.pack(padx=18, pady=14, fill=tk.Y)
        self._topFrame.pack(fill=tk.BOTH, padx=18, pady=(8, 4), expand=True)

        # Middle Frame
        self._middleFrame = tk.Frame(self.master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
        self._amountEntry = tk.Entry(self._middleFrame, justify='center', font='HELVETICA 16 bold', bg='bisque', fg='gray25')
        self._amountEntry.pack(padx=20, fill=tk.X, expand=True, pady=(14, 0))
        self._amountEntry.insert(0, 'Enter Calorie Amount')
        self._middleFont = font.Font(self._middleFrame, family='TIMES NEW ROMAN', size=16, weight='normal')
        self._descEntry = tk.Entry(self._middleFrame, justify='center', font=self._middleFont, bg='bisque', fg='gray25')
        self._descEntry.pack(padx=18, pady=14, fill=tk.BOTH)
        self._descEntry.insert(0, 'Enter Desc. (optional)')
        self._middleFrame.pack(fill=tk.BOTH, padx=18, expand=True, pady=10)

        # Bottom Frame
        self._bottomFrame = tk.Frame(self.master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
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

        # Window Attributes.
        self.master.config(bg='firebrick4')
        self.master.title('RECORD CALORIES')
        self.master.bind('<<CalendarSelected>>', lambda cmd: updateDate())
        self._amountEntry.bind('<FocusIn>', amountEntry_Focus)
        self._amountEntry.bind('<FocusOut>', amountEntry_Focus)
        self._descEntry.bind('<FocusIn>', descBox_Focus)
        self._descEntry.bind('<FocusOut>', descBox_Focus)
        self.master.minsize(500, 550)
        self.master.mainloop()

    # Record workout for specific date.
    def recordWorkout(self, window):

        self.bodyGroup = None
        self.workout = None
        # Each index in sets, corresponds to that same index in reps.
        # Index of set# in self.sets is related to same index in self.reps.
        # So index 3 in self.reps will state the # of reps for the set # @ index 3 in self.sets
        self.sets = []
        self.reps = []
        self._weights = []

        # Method inserts the workout details into DB.
        def insertDocument():
            self._bodyGroup = str(self._selectedMuscleGroup.get())
            self._workout = str(self._workout.get())
            self._reps = self.reps
            self._sets = self.sets
            self._weights = self._weights
            self._date = str(self._cal.selection_get().year) + "-" + str(self._cal.selection_get().month) + "-" + str(self._cal.selection_get().day)

            # Write contents to database.
            self._query = {'date': self._date, 'muscleGroup': self._bodyGroup, 'workout': self._workout, 'sets': self._sets, 'reps': self._reps, 'weight': self._weights}
            self._insert = self.workoutPerDay.insert_one(self._query)

            # Transition back to main-menu.
            self.master.destroy()
            self.master.quit()
            self.root = tk.Tk()
            self.methodsScreen(self.root)
            self.root.mainloop()

        # Method binded to backButton.
        def back():
            self.master.destroy()
            self.master.quit()
            self.root = tk.Tk()
            self.methodsScreen(self.root)
            self.root.mainloop()

        # Binded method updates label underneath calendar whenever date is selected.
        def updateDate():
            self._getSelectedDate = self._cal.selection_get()
            self._topLabel2.config(text=self._getSelectedDate)
            self.master.after(1, self.master.update())

        def updateWorkoutList():
            self._bodyGroup = str(self._selectedMuscleGroup.get())
            self._array = []
            if self._bodyGroup == 'CHEST' or 'BACK' or 'SHOULDERS' or 'ARMS' or 'ABS' or 'LEGS':
                self._label2['state'] = 'normal'
                self._workoutSelector['state'] = 'normal'
                self._workoutSelector['menu'].delete(0, tk.END)
                if self._bodyGroup == 'CHEST':
                    self._workout.set(self._chestWorkouts[0])
                    for item in self._chestWorkouts:
                        self._array.append(item)
                elif self._bodyGroup == 'BACK':
                    self._workout.set(self._backWorkouts[0])
                    for item in self._backWorkouts:
                        self._array.append(item)
                elif self._bodyGroup == 'SHOULDERS':
                    self._workout.set(self._shoulderWorkouts[0])
                    for item in self._shoulderWorkouts:
                        self._array.append(item)
                elif self._bodyGroup == 'ARMS':
                    self._workout.set(self._armWorkouts[0])
                    for item in self._armWorkouts:
                        self._array.append(item)
                elif self._bodyGroup == 'ABS':
                    self._workout.set(self._coreWorkouts[0])
                    for item in self._coreWorkouts:
                        self._array.append(item)
                elif self._bodyGroup == 'LEGS':
                    self._workout.set(self._legsWorkouts[0])
                    for item in self._legsWorkouts:
                        self._array.append(item)

                self._workoutSelector.pack_forget()
                self._workout = tk.StringVar()
                self._workoutSelector = tk.OptionMenu(self._middleFrame, self._workout, *self._array, command=lambda cmd: updateSetRepBox())
                self._workoutSelector['menu'].config(font=('calibri', 20), relief='raised', bd=4)
                self._workout.set('-')
                self._workoutSelector.grid(row=3, column=0, sticky='ew', padx=6, pady=(0, 12))

        def updateSetRepBox():
            self._setRepBox['state'] = 'normal'
            self._label3['state'] = 'normal'
            self._setRepBox['bg'] = 'snow'
            self._addRow['state'] = 'normal'
            self._weightEntry['state'] = 'normal'
            self._repEntry['state'] = 'normal'

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

        def addRows():
            try:
                if str(self._weightEntry.get()) != 'Weight (lbs)':
                    try:
                        self._setNum += 1
                        self.sets.append(int(self._setNum))
                        self.reps.append(int(self._repEntry.get()))
                        self._weights.append(float(self._weightEntry.get()))
                        self._setRepBox.insert(tk.END, 'Set {0}: {1} Reps - {2} lbs.'.format(self._setNum, self._repEntry.get(), self._weightEntry.get()))
                    except ValueError:
                        raise ValueError
                else:
                    try:
                        self._setNum += 1
                        self.sets.append(int(self._setNum))
                        self.reps.append(int(self._repEntry.get()))
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
                self.master.update()

            except ValueError:
                def closeWindow():
                    self._alertWindow.destroy()
                    self._alertWindow.quit()
                self._alertWindow = tk.Tk()
                self._setNum -= 1

                self._label1 = tk.Label(self._alertWindow, text='Please ensure you have entered a \nvalid rep amount and weight amount. ', fg='ivory', bg='indianred3')
                self._label1.config(font='HELVETICA 16 bold')
                self._label2 = tk.Label(self._alertWindow, text='If no weight for the workout, than leave entry as is!')
                self._label2.config(bg='indianred3', fg='bisque', font='HELVETICA 12 bold')
                self._label1.pack(pady=(10, 6), padx=20, fill=tk.X)
                self._label2.pack(padx=20, fill=tk.X)
                self._closeButton = tk.Button(self._alertWindow, text='CLOSE MESSAGE', font='HELVETICA 16 bold', highlightbackgroun='gray25', fg='ivory')
                self._closeButton.config(command=lambda: closeWindow())
                self._closeButton.pack(fill=tk.X, padx=20, pady=10)

                self._alertWindow.config(bg='indianred3')
                self._alertWindow.title('ALERT')
                self._alertWindow.minsize(350, 150)
                self._alertWindow.resizable(False, False)
                self._alertWindow.bind('<Return>', lambda cmd: closeWindow())
                self._alertWindow.mainloop()

        def delRows():
            self._setNum -= 1
            if self._setNum > 0:
                self._delRow['state'] = 'normal'
                self._addButton['state'] = 'normal'
            else:
                self._delRow['state'] = 'disabled'
                self._addButton['state'] = 'disabled'
            self.master.update()

            self._setRepBox.delete(tk.END)
            self.sets.pop()
            self.reps.pop()
            self._weights.pop()

        self.master = window
        self._setNum = 0

        # Top Frame.
        # Calendar for user to pick workout date.
        self._topFrame = tk.Frame(self.master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
        self._font1 = font.Font(self._topFrame, family='TIMES', size=22, weight='bold', underline=True)
        self._topLabel = tk.Label(self._topFrame, text='SELECT DATE', bg='gray25', fg='ivory', font=self._font1)
        self._topLabel.pack(padx=18, pady=(14, 0), fill=tk.BOTH)
        self._cal = Calendar(self._topFrame, selectmode='day', year=self.currentDate.year, month=self.currentDate.month, day=self.currentDate.day)
        self._cal.config(firstweekday='sunday', showweeknumbers=False, foreground='firebrick4', background='ivory', selectforeground='orange', showothermonthdays=False)
        self._cal.pack(padx=30, fill=tk.BOTH, expand=True)
        self._font2 = font.Font(self._topFrame, family='TIMES', size=22, weight='bold', underline=True)
        self._topLabel2 = tk.Label(self._topFrame, text=self._cal.selection_get(), bg='lightcyan', fg='gray25', font=self._font2)
        self._topLabel2.pack(padx=18, pady=14, fill=tk.Y)
        self._topFrame.pack(fill=tk.BOTH, padx=18, pady=8, expand=True)

        # Middle Frame.
        self._middleFrame = tk.Frame(self.master, relief='raised', bd=4, highlightbackground='gray30', bg='bisque')
        self._middleFrame.grid_columnconfigure(0, weight=1)
        self._middleFrame.grid_columnconfigure(1, weight=1)
        self._middleFrame.grid_columnconfigure(2, weight=1)
        self._middleFrame.grid_rowconfigure(0, weight=1)
        self._middleFrame.grid_rowconfigure(1, weight=1)
        self._middleFrame.grid_rowconfigure(2, weight=1)
        self._middleFrame.grid_rowconfigure(3, weight=1)

        self._muscleGroups = ['CHEST', 'BACK', 'SHOULDERS', 'ARMS', 'ABS', 'LEGS']
        self._label1 = tk.Label(self._middleFrame, text='1. SELECT BODY GROUP:', font='TIMESNEWROMAN 16 bold', bg='gray25', fg='ivory')
        self._label1.grid(row=0, column=0, sticky='nsew', padx=8, pady=(12, 0))
        self._selectedMuscleGroup = tk.StringVar()
        self._muscleGroupSelector = tk.OptionMenu(self._middleFrame, self._selectedMuscleGroup, *self._muscleGroups, command=lambda cmd: updateWorkoutList())
        self._muscleGroupSelector['menu'].config(font=('calibri', 20), relief='raised', bd=4)
        self._selectedMuscleGroup.set('-')
        self._muscleGroupSelector.grid(row=1, column=0, sticky='ew', padx=8)

        self._chestWorkouts = ['Push-ups', 'DB Bench Press', 'DB One-Arm Hammer Press', 'DB Fly']
        self._backWorkouts = ['Barbell Bent-Over Row', 'DB One-Arm Row', 'Barbell Reverse Grip Bent-Over Row']
        self._shoulderWorkouts = ['DB Shoulder Press', 'DB Shrugs', 'DB Alt. Deltoid Raises']
        self._armWorkouts = ['DB Concentration Curls', 'DB Hammer Curls', 'DB Seated Bent-over Tricep Exts.', 'Barbell Trciep Extensions']
        self._coreWorkouts = ['Sit-ups', 'V-ups', 'Scissor Kicks']
        self._legsWorkouts = ['Glute Kickbacks', 'DB Lunges', 'DB Seated Calf Raises']
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
        self._repEntry.bind('<FocusIn>', repEntry_Focus)
        self._repEntry.bind('<FocusOut>', repEntry_Focus)
        self._weightEntry_tkvar = tk.StringVar()
        self._weightEntry = tk.Entry(self._middleFrame, justify='center', font='HELVETICA 20 bold', text=self._weightEntry_tkvar, state='disabled')
        self._weightEntry_tkvar.set('Weight (lbs)')
        self._weightEntry.bind('<FocusIn>', weightEntry_Focus)
        self._weightEntry.bind('<FocusOut>', weightEntry_Focus)
        self._weightEntry.grid(row=2, column=2, sticky='nsew', padx=8, pady=12)
        self._addRow = tk.Button(self._middleFrame, text='(+) Set', font='HELVETICA 14 bold', highlightbackground='green', state='disabled', command=lambda: addRows())
        self._addRow.grid(row=3, column=2, sticky='nsew', padx=8, pady=8)
        self._delRow = tk.Button(self._middleFrame, text='(-) Set', font='HELVETICA 14 bold', highlightbackground='indianred3', state='disabled', command=lambda: delRows())
        self._delRow.grid(row=3, column=1, sticky='nsew', padx=8, pady=8)
        self._middleFrame.pack(fill=tk.BOTH, padx=18, pady=8, expand=True)

        # Bottom Frame.
        self._bottomFrame = tk.Frame(self.master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
        self._bottomFrame.grid_rowconfigure(0, weigh=1)
        self._bottomFrame.grid_rowconfigure(1, weight=1)
        self._bottomFrame.grid_columnconfigure(0, weight=1)
        self._addButton = tk.Button(self._bottomFrame, text='INSERT', font='HELVETICA 16 bold', highlightbackground='mediumaquamarine', fg='snow', relief='raised')
        self._addButton.config(command=lambda: insertDocument(), state='disabled')
        self._addButton.grid(row=0, column=0, sticky='nsew', padx=18, pady=4)
        self._backButton = tk.Button(self._bottomFrame, text='BACK', font='HELVETICA 16 bold', command=lambda: back(), highlightbackground='indianred', fg='snow', relief='raised')
        self._backButton.grid(row=1, column=0, sticky='nsew', padx=18, pady=4)
        self._bottomFrame.pack(fill=tk.BOTH, padx=18, pady=8, expand=True)

        self.master.title('RECORD WORKOUT')
        self.master.config(bg='mediumpurple2')
        self.master.bind('<<CalendarSelected>>', lambda cmd: updateDate())
        self.master.minsize(750, 750)
        self.master.mainloop()

    # User can view calories for today, 1-week or 30 days span, or a specific date.
    def viewCalories(self, window):

        self._amount = None
        self._desc = None
        self._date = None

        # Method returns the average calories for the user for all calorie recordings.
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
            self.master.destroy()
            self.master.quit()
            self.root = tk.Tk()
            self.methodsScreen(self.root)
            self.root.mainloop()

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
                self._formatMonthNumber = {1: '01',
                                           2: '02',
                                           3: '03',
                                           4: '04',
                                           5: '05',
                                           6: '06',
                                           7: '07',
                                           8: '08',
                                           9: '09',
                                           10: '10',
                                           11: '11',
                                           12: '12'}

                self._grab = str(self._specDayEntry.get()).split('/')
                self._m = int(self._grab[0])
                if self._m in self._formatMonthNumber.keys():
                    self._m = self._formatMonthNumber.get(self._m)
                else:
                    self._m = int(self._grab[0])

                self._d = int(self._grab[1])
                if self._d in self._formatMonthNumber.keys():
                    self._d = self._formatMonthNumber.get(self._d)
                else:
                    self._d = int(self._grab[1])

                self._y = int(self._grab[2])

                if int(self._m) >= 13 or int(self._m) <= 0:
                    raise ValueError

                viewToday(1, self._m, self._d, self._y)
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

        # View today views the calories and and desc. for today's date. It will also be able to search for specific dates (both imps. in one method).
        def viewToday(tag, *args):

            def back():
                self._alpha.destroy()
                self._alpha.quit()
                self._root = tk.Tk()
                self.viewCalories(self._root)
                self._root.mainloop()

            self._month = None
            self._day = None
            self._year = None

            # Dict. for converting numerical months to letters.
            self._months = {1: 'January',
                            2: 'February',
                            3: 'March',
                            4: 'April',
                            5: 'May',
                            6: 'June',
                            7: 'July',
                            8: 'August',
                            9: 'September',
                            10: 'October',
                            11: 'November',
                            12: 'December'}

            self._formatMonthNumber = {1: '01',
                                       2: '02',
                                       3: '03',
                                       4: '04',
                                       5: '05',
                                       6: '06',
                                       7: '07',
                                       8: '08',
                                       9: '09',
                                       10: '10',
                                       11: '11',
                                       12: '12'}

            # View today.
            if tag == 0:
                self._month_Num = int(self.currentDate.month)
                if self._month_Num in self._formatMonthNumber.keys():
                    self._month_Num = self._formatMonthNumber.get(self._month_Num)
                else:
                    self._month_Num = self.currentDate.month
                self._month = self._months.get(int(self.currentDate.month))
                self._day = self.currentDate.day
                self._year = self.currentDate.year

            # View specific date from supplied *arguments.
            elif tag == 1:
                self._args = []
                for self._item in args:
                    self._args.append(self._item)
                self._month_Num = self._args[0]
                if self._month_Num in self._formatMonthNumber.keys():
                    self._month_Num = self._formatMonthNumber.get(self._month_Num)
                else:
                    self._month_Num = self._args[0]
                self._month = self._months.get(int(self._args[0]))
                self._day = self._args[1]
                self._year = self._args[2]

            self.master.destroy()
            self.master.quit()
            self._todayDateFormat = '{0} {1}, {2}'.format(self._month, self._day, self._year)

            self._alpha = tk.Tk()

            self._calories = []
            self._descriptions = []

            # Fill empty arrays. calories[n] corresponds to descriptions[n].
            for self.docs in self.calPerDay.find({'date': '{0}-{1}-{2}'.format(self._year, self._month_Num, self._day)}):
                self._calories.append(self.docs['amount'])
                self._descriptions.append(self.docs['desc'])

            self._totalCals = 0.0
            for cals in self._calories:
                self._totalCals += cals

            # Display above information in window.
            self._topFrame = tk.Frame(self._alpha, bg='gray25', bd=4, relief='ridge')
            self._listBoxFont = font.Font(family='TIMES NEW ROMAN', size=18, weight='bold')
            self._listBox = tk.Listbox(self._topFrame, bg='antiquewhite', font=self._listBoxFont, justify='center')
            for self._index in range(0, len(self._calories)):
                self._listBox.insert(tk.END, self._descriptions[self._index])
                self._listBox.insert(tk.END, self._calories[self._index])
            self._listBox.pack(padx=20, pady=(20, 5), fill=tk.BOTH)
            for item in range (0, self._listBox.size()):
                if item % 2 == 0:
                    self._listBox.itemconfig(item, bg='lightpink3')
            if self._listBox.size() == 0:
                self._listBox.insert(0, 'NO DATA')
                self._listBox.itemconfig(0, bg='indianred3', fg='ivory')

            self._font1 = font.Font(family='TIMES NEW ROMAN', size=18, weight='bold')
            self._topLabel = tk.Label(self._topFrame, text='Total Calories:', font=self._font1, bg='steelblue1', relief='ridge')
            self._topLabel.pack(padx=20, pady=(5, 5), fill=tk.BOTH)
            self._totalCalLabel = tk.Label(self._topFrame, text=self._totalCals,  font=self._font1, relief='raised')
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
            self._alpha.title(self._todayDateFormat)
            self._alpha.mainloop()

        def sevenDayForecast():
            self._formatMonthNumber = {1: '01', 2: '02', 3: '03',
                                       4: '04', 5: '05', 6: '06',
                                       7: '07', 8: '08', 9: '09',
                                       10: '10', 11: '11', 12: '12'}

            self._year = self.currentDate.year
            self._month = self.currentDate.month
            if self._month in self._formatMonthNumber.keys():
                self._month = self._formatMonthNumber.get(self._month)
            else:
                self._month = self.currentDate.month
            self._day = self.currentDate.day
            if self._day in self._formatMonthNumber.keys():
                self._day = self._formatMonthNumber.get(self._day)
            else:
                self._day = self.currentDate.day

            self._sevenDays = []
            self._date = datetime.date(int(self._year), int(self._month), int(self._day))
            for x in range(1, 8):
                self._sevenDays.append(self._date.strftime('%Y-%m-%d'))
                self._date += datetime.timedelta(days=-1)

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
            self._formatMonthNumber = {1: '01', 2: '02', 3: '03',
                                       4: '04', 5: '05', 6: '06',
                                       7: '07', 8: '08', 9: '09',
                                       10: '10', 11: '11', 12: '12'}

            self._year = self.currentDate.year
            self._month = self.currentDate.month
            if self._month in self._formatMonthNumber.keys():
                self._month = self._formatMonthNumber.get(self._month)
            else:
                self._month = self.currentDate.month
            self._day = self.currentDate.day
            if self._day in self._formatMonthNumber.keys():
                self._day = self._formatMonthNumber.get(self._day)
            else:
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

        self.master = window

        self._tFborder = tk.Frame(self.master, bg='thistle1')
        self._topFrame = tk.Frame(self._tFborder, bg='gray25')
        self._topFrame.grid_rowconfigure(0, weight=1)
        self._topFrame.grid_rowconfigure(1, weight=1)
        self._topFrame.grid_rowconfigure(2, weight=1)
        self._topFrame.grid_rowconfigure(3, weight=1)
        self._topFrame.grid_rowconfigure(4, weight=1)
        self._topFrame.grid_columnconfigure(0, weight=1)
        self._todayStatButton = tk.Button(self._topFrame, text='TODAY\'S CALORIES', font='HELVETICA 22 bold', highlightbackground='lightslateblue', fg='snow')
        self._todayStatButton.config(command=lambda: viewToday(0))
        self._todayStatButton.config(relief='raised', highlightthickness=4)
        self._todayStatButton.grid(row=0, column=0, sticky='nsew', pady=(20, 5), padx=25)
        self._last7DaysButton = tk.Button(self._topFrame, text='LAST 7 DAYS', font='HELVETICA 22 bold', highlightbackground='lightslateblue', fg='snow')
        self._last7DaysButton.config(relief='raised', highlightthickness=4, command=lambda: sevenDayForecast())
        self._last7DaysButton.grid(row=1, column=0, sticky='nsew', pady=5, padx=25)
        self._last30DaysButton = tk.Button(self._topFrame, text='LAST 30 DAYS', font='HELVETICA 22 bold', highlightbackground='lightslateblue', fg='snow')
        self._last30DaysButton.config(relief='raised', highlightthickness=4, command=lambda: thirtyDayForecast())
        self._last30DaysButton.config(relief='raised', highlightthickness=4)
        self._last30DaysButton.grid(row=2, column=0, sticky='nsew', pady=5, padx=25)
        self._font1 = font.Font(family='TIMES NEW ROMAN', size=16, weight='bold')
        self._bottomLabel = tk.Label(self._topFrame, text='Average calories (per day):', fg='snow', bg='mediumpurple4', font=self._font1)
        self._bottomLabel.config(relief='ridge', bd=6)
        self._bottomLabel.grid(row=3, column=0, sticky='nsew', pady=5, padx=25)
        self._font2 = font.Font(family='TIMES NEW ROMAN', size=20, weight='bold')
        self._bottomLabel2 = tk.Label(self._topFrame, text=averageCalories(), fg='gray25', bg='lightskyblue2', font=self._font2)
        self._bottomLabel2.config(relief='ridge', bd=4)
        self._bottomLabel2.grid(row=4, column=0, sticky='ns', pady=(5, 20), padx=5)
        self._topFrame.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)
        self._tFborder.pack(padx=20, pady=(20, 10), fill=tk.BOTH, expand=True)

        self._bottomFrame = tk.Frame(self.master, bg='gray25')
        self._font3 = font.Font(family='TIMES NEW ROMAN', size=16, weight='bold')
        self._bottomLabel = tk.Label(self._bottomFrame, text='Search specific date:', font=self._font3, bg='gray25', fg='ivory')
        self._bottomLabel.pack(padx=25, fill=tk.BOTH, pady=(10, 2), expand=True)
        self._specDayEntry = tk.Entry(self._bottomFrame, justify='center', bg='lightblue3', fg='gray25', font=self._font3)
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

        self.master.config(bg='seagreen3')
        self.master.title('Calories History')
        self.master.minsize(600, 500)
        self._specDayEntry.bind('<FocusIn>', specDayEntry_Focus)
        self._specDayEntry.bind('<FocusOut>', specDayEntry_Focus)
        self.master.bind('<Return>', lambda cmd: specDayEntryBind())
        self.master.mainloop()

    # User can view/track workout progress 1-week or 30 days span, or a specific date.
    def viewWorkout(self, window):

        self.master = window

        # Back to main-menu.
        def back():
            self.master.destroy()
            self.master.quit()
            self.root = tk.Tk()
            self.methodsScreen(self.root)
            self.root.mainloop()

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
                self._formatMonthNumber = {1: '01',
                                           2: '02',
                                           3: '03',
                                           4: '04',
                                           5: '05',
                                           6: '06',
                                           7: '07',
                                           8: '08',
                                           9: '09',
                                           10: '10',
                                           11: '11',
                                           12: '12'}

                self._grab = str(self._specDayEntry.get()).split('/')
                self._m = int(self._grab[0])
                if self._m in self._formatMonthNumber.keys():
                    self._m = self._formatMonthNumber.get(self._m)
                else:
                    self._m = int(self._grab[0])

                self._d = int(self._grab[1])
                if self._d in self._formatMonthNumber.keys():
                    self._d = self._formatMonthNumber.get(self._d)
                else:
                    self._d = int(self._grab[1])

                self._y = int(self._grab[2])

                if int(self._m) >= 13 or int(self._m) <= 0:
                    raise ValueError
                viewDay(self._y, self._m, self._d)
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

        def viewDay(year, month, day):

            def back():
                self._alpha.destroy()
                self._alpha.quit()

            self._workouts = []
            self._reps = []
            self._sets = []
            self._muscleGroups = []
            self._weights = []

            for self._docs in self.workoutPerDay.find({'date': '{0}-{1}-{2}'.format(int(year), int(month), int(day))}):
                self._workouts.append(self._docs['workout'])
                self._sets.append(self._docs['sets'])
                self._reps.append(self._docs['reps'])
                self._weights.append(self._docs['weight'])
                self._muscleGroups.append(self._docs['muscleGroup'])

            self._alpha = tk.Tk()

            self._topFrame = tk.Frame(self._alpha, bg='gray25', bd=4, relief='ridge')
            # Textbox to hold workout history.
            self._textBox = tk.Listbox(self._topFrame, justify='center', font='HELVECTICA 20 bold', bg='gray25', relief='groove', bd=4)

            try:
                for item in range(0, len(self._workouts)):
                    self._textBox.insert(tk.END, str(self._workouts[item]).upper())
                    self._textBox.itemconfig(tk.END, bg='mediumorchid2')
                    self._textBox.insert(tk.END, str(self._muscleGroups[item]).upper())
                    self._textBox.itemconfig(tk.END, bg='lightgoldenrod')
                    self._textBox.insert(tk.END, str(self._sets[item][-1]) + ' Set(s)')
                    self._textBox.itemconfig(tk.END, bg='ivory', fg='gray25')
                    self._textBox.insert(tk.END, str(self._reps[item]) + ' Rep(s)')
                    self._textBox.itemconfig(tk.END, bg='ivory', fg='gray25')
                    self._total = 0.0
                    self._weightMsg = ''
                    for self._weight in self._weights[item]:
                        self._total += self._weight
                    if self._total == 0:
                        self._weightMsg = 'No Weight'
                    if self._weightMsg == '':
                        self._textBox.insert(tk.END, str(self._weights[item]) + ' lbs.')
                    else:
                        self._textBox.insert(tk.END, self._weightMsg)
                    self._textBox.itemconfig(tk.END, bg='ivory', fg='gray25')
                    self._textBox.insert(tk.END, '\n')
                    self._textBox.itemconfig(tk.END, bg='gray25')
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

            self._alpha.title('{0}-{1}-{2}\'s Workout(s):'.format(year, month, day))
            self._alpha.config(bg='thistle1')
            self._alpha.minsize(500, 300)
            self._alpha.mainloop()

        def viewToday():

            def back():
                self._alpha.destroy()
                self._alpha.quit()

            self._workouts = []
            self._reps = []
            self._sets = []
            self._muscleGroups = []
            self._weights = []

            self._year = self.currentDate.year
            self._month = self.currentDate.month
            self._day = self.currentDate.day

            for self._docs in self.workoutPerDay.find({'date': '{0}-{1}-{2}'.format(self._year, self._month, self._day)}):
                self._workouts.append(self._docs['workout'])
                self._sets.append(self._docs['sets'])
                self._reps.append(self._docs['reps'])
                self._weights.append(self._docs['weight'])
                self._muscleGroups.append(self._docs['muscleGroup'])

            self._alpha = tk.Tk()

            self._topFrame = tk.Frame(self._alpha, bg='gray25', bd=4, relief='ridge')
            # Textbox to hold workout history.
            self._textBox = tk.Listbox(self._topFrame, justify='center', font='HELVECTICA 20 bold', bg='gray25', relief='groove', bd=4)

            try:
                for item in range(0, len(self._workouts)):
                    self._textBox.insert(tk.END, str(self._workouts[item]).upper())
                    self._textBox.itemconfig(tk.END, bg='mediumorchid2')
                    self._textBox.insert(tk.END, str(self._muscleGroups[item]).upper())
                    self._textBox.itemconfig(tk.END, bg='lightgoldenrod')
                    self._textBox.insert(tk.END, str(self._sets[item][-1]) + ' Set(s)')
                    self._textBox.itemconfig(tk.END, bg='ivory', fg='gray25')
                    self._textBox.insert(tk.END, str(self._reps[item]) + ' Rep(s)')
                    self._textBox.itemconfig(tk.END, bg='ivory', fg='gray25')
                    self._total = 0.0
                    self._weightMsg = ''
                    for self._weight in self._weights[item]:
                        self._total += self._weight
                    if self._total == 0:
                        self._weightMsg = 'No Weight'
                    if self._weightMsg == '':
                        self._textBox.insert(tk.END, str(self._weights[item]) + ' lbs.')
                    else:
                        self._textBox.insert(tk.END, self._weightMsg)
                    self._textBox.itemconfig(tk.END, bg='ivory', fg='gray25')
                    self._textBox.insert(tk.END, '\n')
                    self._textBox.itemconfig(tk.END, bg='gray25')
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

            self._alpha.title('Today\'s Workout(s):')
            self._alpha.config(bg='thistle1')
            self._alpha.minsize(500, 300)
            self._alpha.mainloop()

        def sevenDayForcast():
            self._formatMonthNumber = {1: '01', 2: '02', 3: '03',
                                       4: '04', 5: '05', 6: '06',
                                       7: '07', 8: '08', 9: '09',
                                       10: '10', 11: '11', 12: '12'}

            self._year = self.currentDate.year
            self._month = self.currentDate.month
            self._day = self.currentDate.day

            self._sevenDays = []
            self._date = datetime.date(int(self._year), int(self._month), int(self._day))
            for x in range(1, 8):
                self._sevenDays.append(self._date.strftime('%Y-%m-%d'))
                self._date += datetime.timedelta(days=-1)

            # For the last 7 days. Each index in each array corresponds to the other index. (eg. self._reps[2] relates to self._workouts[2], etc).
            self._reps = []
            self._sets = []
            self._weights = []
            self._workouts = []
            self._muscleGroups = []

            # Fill calories list for last 7 days.
            for self._x in self._sevenDays:
                for self._workout in self.workoutPerDay.find({'date': self._x}):
                    self._reps.append(self._workout['reps'])
            print(self._reps)

        self._tFborder = tk.Frame(self.master, bg='thistle1')
        self._topFrame = tk.Frame(self._tFborder, bg='gray25')
        self._topFrame.grid_rowconfigure(0, weight=1)
        self._topFrame.grid_rowconfigure(1, weight=1)
        self._topFrame.grid_rowconfigure(2, weight=1)
        self._topFrame.grid_rowconfigure(3, weight=1)
        self._topFrame.grid_rowconfigure(4, weight=1)
        self._topFrame.grid_columnconfigure(0, weight=1)
        self._todayStatButton = tk.Button(self._topFrame, text='TODAY\'S WORKOUT', font='HELVETICA 22 bold', highlightbackground='lightslateblue', fg='snow')
        self._todayStatButton.config(command=lambda: viewToday())
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

        self._bottomFrame = tk.Frame(self.master, bg='gray25')
        self._font3 = font.Font(family='TIMES NEW ROMAN', size=16, weight='bold')
        self._bottomLabel = tk.Label(self._bottomFrame, text='Search specific date:', font=self._font3, bg='gray25', fg='ivory')
        self._bottomLabel.pack(padx=25, fill=tk.BOTH, pady=(10, 2), expand=True)
        self._specDayEntry = tk.Entry(self._bottomFrame, justify='center', bg='lightblue3', fg='gray25', font=self._font3)
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

        self.master.config(bg='mediumpurple3')
        self.master.title('Workout History')
        self.master.minsize(600, 500)
        self._specDayEntry.bind('<FocusIn>', specDayEntry_Focus)
        self._specDayEntry.bind('<FocusOut>', specDayEntry_Focus)
        self.master.bind('<Return>', lambda cmd: specDayEntryBind())
        self.master.mainloop()


# Execute Program.
if __name__ == '__main__':
    master = tk.Tk()
    woCal = WoCal(master)
    master.mainloop()
