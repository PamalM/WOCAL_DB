import pymongo as pym
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
import tkinter as tk
from tkinter import font
from tkcalendar import Calendar
import platform
import os
import matplotlib.pyplot as plt
import time
import datetime


class WoCal:

    # Constructor method initiates WoCal object by signing into DB.
    def __init__(self, master):

        # Login credentials.
        self._username = None
        self._password = None
        self._url = None

        self.currentDate = datetime.datetime.now()

        # Method signs user into DB with username/password provided within entry fields.
        def signIn():
            try:
                # Setup connection.
                self._username = str(self._usernameEntry.get())
                self._password = str(self._passwordEntry.get())
                if self._username != 'Enter Username' and self._password != 'Enter Password':
                    self._url = "mongodb+srv://{0}:{1}@wocal.szoqb.mongodb.net/WOCAL?retryWrites=true&w=majority".format(self._username, self._password)
                    # Make connection; Check for user authentication.
                    self.client = pym.MongoClient(self._url)
                    try:
                        self.client.admin.command('ismaster')
                        self.db = self.client['WOCAL']
                    except ConnectionFailure:
                        raise ValueError
                    except OperationFailure:
                        raise ValueError

                    # Transition to next screen.
                    print('[Successful sign-in into DB!]')
                    self.master.destroy()
                    self.master.quit()

                    # Save user login credentials to text file depending on checkbox selection.
                    if self._rememberMe.get():
                        # Determine user's operating system.
                        uMachine = platform.system()
                        if uMachine == 'Darwin' or 'Linux':
                            filename = os.getcwd() + '/login.txt'
                        elif uMachine == 'Windows':
                            filename = os.getcwd() + '\login.txt'
                        else:
                            filename = 'NOF'
                        if filename != 'NOF':
                            with open(filename, 'w') as file:
                                # Save login credentials to text file in cwd.
                                file.write(self._username + ":" + self._password)
                            file.close()
                        else:
                            print('Error determining user OS; Error writing to file!')

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

        # [4] Methods below highlight and add style to both entries when clicked on/off.
        def usernameEntry_FocusIn(event):
            if self._usernameEntry.get() == 'Enter Username':
                self._usernameEntry.delete(0, tk.END)
                self._usernameEntry.insert(0, '')
                self._usernameEntry.config(bg='mistyrose', fg='gray25')

        def usernameEntry_FocusOut(event):
            if self._usernameEntry.get() == '':
                self._usernameEntry.insert(0, 'Enter Username')
            self._usernameEntry.config(bg='gray25', fg='ivory')

        def passwordEntry_FocusIn(event):
            if self._passwordEntry.get() == 'Enter Password':
                self._passwordEntry.delete(0, tk.END)
                self._passwordEntry.insert(0, '')
                self._passwordEntry.config(bg='mistyrose', fg='gray25')

        def passwordEntry_FocusOut(event):
            if self._passwordEntry.get() == '':
                self._passwordEntry.insert(0, 'Enter Password')
            self._passwordEntry.config(bg='gray25', fg='ivory')

        # [2] Styling method for button color change to occur on mouse hover-over.
        def signInButton_FocusIn(event):
            self._signInButton['highlightbackground'] = 'lightsalmon'
            self._signInButton['fg'] = 'gray25'
            self._signInButton['font'] = 'HELVETICA 20 underline'
            self._signInButton['relief'] = 'groove'

        def signInButton_FocusOut(event):
            self._signInButton['highlightbackground'] = 'lavender'
            self._signInButton['font'] = 'HELVETICA 20 bold'
            self._signInButton['fg'] = 'black'

        # Method adds styling/text-alterations to checkbox depending on selection.
        def remember():
            self.remember = self._rememberMe.get()
            if self.remember:
                self._rememberMeCheckBox.config(text='Remember login!', bg='azure2')
            else:
                self._rememberMeCheckBox.config(text='Stay signed-In?', bg='slategray3')

        # Determine user machine OS, and check if login.text file exists.
        self.uMachine = platform.system()
        self.filename = None
        self.fileExists = None
        if self.uMachine == 'Darwin' or 'Linux':
            self.filename = os.getcwd() + '/login.txt'
            self.fileExists = os.path.exists(self.filename)
        elif self.uMachine == 'Windows':
            self.filename = os.getcwd() + '\\login.txt'
            self.fileExists = os.path.exists(self.filename)

        self.master = master
        print('[Awaiting user sign-in for DB] ...')
        # If (login.txt) file exists in proj. directory, than bypass login; Else direct user to db login screen.
        if self.fileExists:
            with open(self.filename, "r") as file:
                for line in file:
                    credentials = line.split(':')
            self._username = credentials[0]
            self._password = credentials[1]
            print('[Successful login for {0}, into the Database]'.format(self._username))
            self._url = "mongodb+srv://{0}:{1}@wocal.szoqb.mongodb.net/WOCAL?retryWrites=true&w=majority".format(self._username, self._password)
            self.client = pym.MongoClient(self._url)
            self.client.admin.command('ismaster')
            self.db = self.client['WOCAL']
            self.methodsScreen(self.master)
        else:
            '''Top Frame'''
            self._topFrame = tk.Frame(self.master, bg='gray25')
            self._font1 = font.Font(self._topFrame, family='HELVETICA', size=30, weight='bold', underline=True)
            self._topLabel1 = tk.Label(self._topFrame, text='Sign Into Database:', font=self._font1, bd=4, bg='lavender', fg='gray25')
            self._topLabel1.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
            self._topFrame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            '''Middle Frame'''
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
            self._usernameEntry.bind('<FocusIn>', usernameEntry_FocusIn)
            self._usernameEntry.bind('<FocusOut>', usernameEntry_FocusOut)
            self._passwordEntry.bind('<FocusIn>', passwordEntry_FocusIn)
            self._passwordEntry.bind('<FocusOut>', passwordEntry_FocusOut)
            self._signInButton.bind('<Enter>', signInButton_FocusIn)
            self._signInButton.bind('<Leave>', signInButton_FocusOut)
            self._middleFrame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            '''Bottom Frame'''
            self._bottomFrame = tk.Frame(self.master, bg='gray25')
            self._font3 = font.Font(self._topFrame, family='TIMES NEW ROMAN', size=10)
            self._bottomLabel = tk.Label(self._bottomFrame, text='Powered through MongoDB\nCreated by Pamal Mangat', font=self._font3, bg='lavender')
            self._bottomLabel.pack(fill=tk.BOTH, padx=18, pady=10, expand=True)
            self._bottomFrame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            # Window Attributes.
            self.master.title('WOCAL - SIGN IN')
            self.master.minsize(400, 500)
            self.master.config(bg='royalblue2')
            self.master.bind('<Return>', lambda cmd: signIn())
            self.master.mainloop()

    # Method presents user with all methods and actions that can be performed within the program; (Main-Menu)
    def methodsScreen(self, master):

        def terminal(tag):
            self.master.destroy()
            self.master.quit()
            self.root = tk.Tk()
            if tag == 1:
                self.recordCalories(self.root)
            elif tag == 3:
                self.recordWorkout(self.root)
            else:
                print(tag)
            self.root.mainloop()

        # Method deletes login.text file from cwd if it exits, and directs user back to db log-in window.
        def logOff():
            self.master.destroy()
            self.master.quit()
            if self.fileExists:
                os.remove(self.filename)
            time.sleep(1)
            print("[" + self._username + " has been logged out of the database]")
            self.root = tk.Tk()
            self.__init__(self.root)
            self.root.mainloop()

        self.master = master

        '''Top Frame'''
        self._topFrame = tk.Frame(self.master, bg='gray25', relief='raised', bd=4, highlightbackground='gray30')
        self._topFrame.grid_rowconfigure(0, weight=1)
        self._topFrame.grid_columnconfigure(0, weight=1)
        self._topFrame.grid_columnconfigure(1, weight=1)
        self._topFrame.grid_rowconfigure(0, weight=1)
        self._topFrame.grid_columnconfigure(0, weight=1)
        self._topFrame.grid_columnconfigure(1, weight=1)
        self._font1 = font.Font(self._topFrame, family='Times NEW ROMAN', size=20, weight='bold', underline=False)
        self._welcomeLabel = tk.Label(self._topFrame, text='Welcome,\n{0}'.format(self._username), font=self._font1, anchor='w', bg='gray25', fg='ivory')
        self._welcomeLabel.grid(row=0, column=0, sticky='ew', padx=18, pady=2)
        self._logOffButton = tk.Button(self._topFrame, text='LogOff', font='HELVETICA 18 bold', relief='raised', bd=2, highlightbackground='indianred', command=lambda: logOff())
        self._logOffButton.grid(row=0, column=1, sticky='nsew', padx=18, pady=8)
        self._topFrame.pack(fill=tk.BOTH, expand=False, padx=18, pady=(14, 0))

        '''Methods Frame'''
        self._methodFrame = tk.Frame(self.master, bg='snow3', relief='raised', bd=4, highlightbackground='gray30')
        self._methodFrame.grid_columnconfigure(0, weight=1)
        self._methodFrame.grid_columnconfigure(1, weight=1)
        self._methodFrame.grid_rowconfigure(0, weight=1)
        self._methodFrame.grid_rowconfigure(1, weight=1)
        self._font2 = font.Font(self._topFrame, family='TIMES', size=22, weight='bold')
        self._recordCaloriesButton = tk.Button(self._methodFrame, text='RECORD\nCALORIES', font=self._font2, highlightbackground='firebrick4', relief='flat')
        self._recordCaloriesButton.config(command=lambda: terminal(1))
        self._recordCaloriesButton.grid(row=0, column=0, sticky='nsew', padx=(18, 2), pady=(14, 4))
        self._trackCaloriesButton = tk.Button(self._methodFrame, text='VIEW\nCALORIES\nLOG', font=self._font2, highlightbackground='springgreen4', relief='flat')
        self._trackCaloriesButton.config(command=lambda: terminal(2))
        self._trackCaloriesButton.grid(row=0, column=1, sticky='nsew', padx=(2, 18), pady=(14, 4))
        self._recordWorkoutButton = tk.Button(self._methodFrame, text='RECORD\nWORKOUT', font=self._font2, highlightbackground='mediumpurple2', relief='flat')
        self._recordWorkoutButton.config(command=lambda: terminal(3))
        self._recordWorkoutButton.grid(row=1, column=0, sticky='nsew', padx=(18, 2), pady=(4, 14))
        self._trackWorkoutButton = tk.Button(self._methodFrame, text='VIEW\nWORKOUT\nLOG', font=self._font2, highlightbackground='lightpink2', relief='flat')
        self._trackWorkoutButton.config(command=lambda: terminal(4))
        self._trackWorkoutButton.grid(row=1, column=1, sticky='nsew', padx=(2, 18), pady=(4, 14))
        self._methodFrame.pack(fill=tk.BOTH, expand=True, padx=18, pady=8)

        self.master.title('WOCAL_DB')
        self.master.focus_set()
        self.master.config(bg='royalblue2')
        self.master.minsize(600, 400)
        self.master.mainloop()

    def recordCalories(self, master):

        self._amount = None
        self._desc = None
        self._date = None
        self.calPerDay = self.db['calPerDay']

        # [4] Styling methods binded for 2 entries within frame.
        def amountEntry_FocusIn(event):
            if self._amountEntry.get() == 'Enter Calorie Amount':
                self._amountEntry.delete(0, tk.END)
                self._amountEntry.insert(0, '')
                self._amountEntry.config(bg='mistyrose', fg='gray25')

        def amountEntry_FocusOut(event):
            if self._amountEntry.get() == '':
                self._amountEntry.insert(0, 'Enter Calorie Amount')
            self._amountEntry.config(bg='bisque', fg='gray25')

        def descBox_FocusIn(event):
            if self._descEntry.get() == 'Enter Desc. (optional)':
                self._descEntry.delete(0, tk.END)
                self._descEntry.insert(0, '')
                self._descEntry.config(bg='mistyrose', fg='gray25')

        def descBox_FocusOut(event):
            if self._descEntry.get() == '':
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

        self.master = master

        '''Top Frame'''
        # Initial update for first time user logs into window. Label must be updated prior to entry.
        self.dayTotal = 0.0
        for records in self.calPerDay.find({'date': '{0}-{1}-{2}'.format(self.currentDate.year, self.currentDate.month, self.currentDate.day)}):
            self.dayTotal += float(records['amount'])
        # Calendar for user to pick date of record for calories.
        self._topFrame = tk.Frame(self.master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
        self._font1 = font.Font(self._topFrame, family='TIMES', size=22, weight='bold', underline=True)
        self._topLabel = tk.Label(self._topFrame, text='SELECT DATE', bg='gray25', fg='ivory', font=self._font1)
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

        '''Middle Frame'''
        self._middleFrame = tk.Frame(self.master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
        self._amountEntry = tk.Entry(self._middleFrame, justify='center', font='HELVETICA 16 bold', bg='bisque', fg='gray25')
        self._amountEntry.pack(padx=20, fill=tk.X, expand=True, pady=(14, 0))
        self._amountEntry.insert(0, 'Enter Calorie Amount')
        self._font3 = font.Font(self._middleFrame, family='TIMES NEW ROMAN', size=16, weight='normal')
        self._descEntry = tk.Entry(self._middleFrame, justify='center', font=self._font3, bg='bisque', fg='gray25')
        self._descEntry.pack(padx=18, pady=14, fill=tk.BOTH)
        self._descEntry.insert(0, 'Enter Desc. (optional)')
        self._middleFrame.pack(fill=tk.BOTH, padx=18, expand=True, pady=10)

        '''Bottom Frame'''
        self._bottomFrame = tk.Frame(self.master, relief='raised', bd=4, highlightbackground='gray30', bg='gray25')
        self._bottomFrame.grid_rowconfigure(0, weigh=1)
        self._bottomFrame.grid_rowconfigure(1, weight=1)
        self._bottomFrame.grid_columnconfigure(0, weight=1)
        self._addButton = tk.Button(self._bottomFrame, text='INSERT', font='HELVETICA 16 bold', highlightbackground='mediumaquamarine', fg='snow', relief='raised')
        self._addButton.config(command=lambda: insertDocument())
        self._addButton.grid(row=0, column=0, sticky='nsew', padx=18, pady=4)
        self._backButton = tk.Button(self._bottomFrame, text='BACK', font='HELVETICA 16 bold', command=lambda: back(), highlightbackground='indianred', fg='snow', relief='raised')
        self._backButton.grid(row=1, column=0, sticky='nsew', padx=18, pady=4)
        self._bottomFrame.pack(fill=tk.BOTH, padx=18, pady=(0, 8), expand=True)

        self.master.config(bg='firebrick4')
        self.master.title('RECORD CALORIES')
        self.master.bind('<<CalendarSelected>>', lambda cmd: updateDate())
        self._amountEntry.bind('<FocusIn>', amountEntry_FocusIn)
        self._amountEntry.bind('<FocusOut>', amountEntry_FocusOut)
        self._descEntry.bind('<FocusIn>', descBox_FocusIn)
        self._descEntry.bind('<FocusOut>', descBox_FocusOut)
        self.master.minsize(500, 550)
        self.master.mainloop()

    def recordWorkout(self, master):

        self.bodyGroup = None
        self.workout = None
        # Each index in sets, corresponds to that same index in reps.
        # Index of set# in self.sets is related to same index in self.reps.
        # So index 3 in self.reps will state the # of reps for the set # @ index 3 in self.sets
        self.sets = []
        self.reps = []

        # Method inserts the workout details into DB.
        def insertDocument():
            print('InsertDocument')

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

        def weightEntry_FocusIn(event):
            if str(self._weightEntry.get()) == 'Weight (lbs)':
                self._weightEntry_tkvar.set('')

        def weightEntry_FocusOut(event):
            if str(self._weightEntry.get()) == '':
                self._weightEntry_tkvar.set('Weight (lbs)')

        def repEntry_FocusIn(event):
            if str(self._repEntry.get()) == '# Reps':
                self._repEntry_tkvar.set('')

        def repEntry_FocusOut(event):
            if str(self._repEntry.get()) == '':
                self._repEntry_tkvar.set('# Reps')

        # TODO: Implement try/except statement for ensuring validity/correct format of reps/weight entered by user.
        def addRows():
            self._setNum += 1
            if str(self._weightEntry.get()) != 'Weight (lbs)':
                self._setRepBox.insert(tk.END, 'Set {0}: {1} Reps - {2} lbs.'.format(self._setNum, self._repEntry.get(), self._weightEntry.get()))
            else:
                self._setRepBox.insert(tk.END, 'Set {0}: {1} Reps'.format(self._setNum, self._repEntry.get()))
            self._repEntry_tkvar.set('')
            if self._setNum > 0:
                self._delRow['state'] = 'normal'
                self.master.update()

        def delRows():
            self._setNum -= 1
            if self._setNum >= 1:
                self._delRow['state'] = 'normal'
                self.master.update()
            self._setRepBox.delete(tk.END)


        self.workoutPerDay = self.db['workoutPerDay']

        self.master = master
        self._setNum = 0

        '''Top Frame'''
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

        '''Middle Frame'''
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
        self._repEntry.bind('<FocusIn>', repEntry_FocusIn)
        self._repEntry.bind('<FocusOut>', repEntry_FocusOut)
        self._weightEntry_tkvar = tk.StringVar()
        self._weightEntry = tk.Entry(self._middleFrame, justify='center', font='HELVETICA 20 bold', text=self._weightEntry_tkvar, state='disabled')
        self._weightEntry_tkvar.set('Weight (lbs)')
        self._weightEntry.bind('<FocusIn>', weightEntry_FocusIn)
        self._weightEntry.bind('<FocusOut>', weightEntry_FocusOut)
        self._weightEntry.grid(row=2, column=2, sticky='nsew', padx=8, pady=12)
        self._addRow = tk.Button(self._middleFrame, text='(+) Set', font='HELVETICA 14 bold', highlightbackground='green', state='disabled', command=lambda: addRows())
        self._addRow.grid(row=3, column=2, sticky='nsew', padx=8, pady=8)
        self._delRow = tk.Button(self._middleFrame, text='(-) Set', font='HELVETICA 14 bold', highlightbackground='indianred3', state='disabled', command=lambda: delRows())
        self._delRow.grid(row=3, column=1, sticky='nsew', padx=8, pady=8)
        self._middleFrame.pack(fill=tk.BOTH, padx=18, pady=8, expand=True)

        '''Bottom Frame'''
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

# Execute Program.
if __name__ == '__main__':
    master = tk.Tk()
    woCal = WoCal(master)
    master.mainloop()
