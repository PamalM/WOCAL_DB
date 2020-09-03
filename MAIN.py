import pymongo as pym
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
import tkinter as tk
from tkinter import font
import getpass
import platform
import os
import matplotlib.pyplot as plt


class WoCal:

    # Constructor method initiates WoCal object by signing into DB.
    def __init__(self, master):

        # Login credentials.
        self._username = None
        self._password = None
        self._url = None

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

        uMachine = platform.system()
        filename = None
        fileExists = None
        if uMachine == 'Darwin' or 'Linux':
            filename = os.getcwd() + '/login.txt'
            fileExists = os.path.exists(filename)
        elif uMachine == 'Windows':
            filename = os.getcwd() + '\\login.txt'
            fileExists = os.path.exists(filename)
        else:
            fileExists = None
            filename = None

        self.master = master

        # If login.txt file exists, than bypass login.
        if fileExists:
            with open(filename, "r") as file:
                for line in file:
                    credentials = line.split(':')
            self._username = credentials[0]
            self._password = credentials[1]
            print('[Successful login for user: {0}, into the Database]'.format(self._username))
            self._url = "mongodb+srv://{0}:{1}@wocal.szoqb.mongodb.net/WOCAL?retryWrites=true&w=majority".format(self._username, self._password)
            self.client = pym.MongoClient(self._url)
            self.client.admin.command('ismaster')
            self.db = self.client['WOCAL']
            self.methodsScreen(self.master)
        else:
            print('[Awaiting user sign-in for DB] ...')
            # Login Window for MongoDB cluster.

            '''Top Frame'''
            self._topFrame = tk.Frame(self.master, bg='gray25')
            self._topFrame.grid_columnconfigure(0, weight=1)
            self._topFrame.grid_rowconfigure(0, weight=1)
            self._topFrame.grid_rowconfigure(1, weight=1)
            self._font1 = font.Font(self._topFrame, family='HELVETICA', size=30, weight='bold', underline=True)
            self._topLabel1 = tk.Label(self._topFrame, text='Sign Into Database:', font=self._font1, bd=4, bg='lavender', fg='gray25')
            self._topLabel1.grid(row=0, column=0, sticky='nsew', padx=18, pady=(14, 0))
            self._font2 = font.Font(self._topFrame, family='TIMES NEW ROMAN', size=16, weight='normal')
            self._topLabel2 = tk.Label(self._topFrame, text='Register for an account by emailing:\nmangatpamal@gmail.com', font=self._font2, bd=4, bg='lavender', fg='gray25')
            self._topLabel2.grid(row=1, column=0, sticky='nsew', padx=18, pady=(0, 14))
            self._topFrame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            '''Middle Frame'''
            self._middleFrame = tk.Frame(self.master, bg='slategray3', relief='raised')
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
            self._bottomFrame.grid_columnconfigure(0, weight=1)
            self._bottomFrame.grid_rowconfigure(0, weight=1)
            self._bottomFrame.grid_rowconfigure(1, weight=1)
            self._font3 = font.Font(self._topFrame, family='TIMES NEW ROMAN', size=10)
            self._bottomLabel = tk.Label(self._bottomFrame, text='Powered through MongoDB\nFurther resources provided by wger\'s REST API.', font=self._font3, bg='lavender')
            self._bottomLabel.grid(row=0, column=0, padx=18, pady=(14, 0), sticky='nsew')
            self._bottomLabel2 = tk.Label(self._bottomFrame, text='Created by Pamal Mangat', font=self._font3, bg='lavender')
            self._bottomLabel2.grid(row=1, column=0, padx=18, pady=(0, 14), sticky='nsew')
            self._bottomFrame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            # Window Attributes.
            self.master.title('WOCAL - SIGN IN')
            self.master.minsize(400, 500)
            self.master.config(bg='royalblue2')
            self.master.bind('<Return>', lambda cmd: signIn())
            self.master.mainloop()

    def methodsScreen(self, master):
        self.master = master
        self.master.title('WOCAL_DB')
        self.master.mainloop()

# Execute Program.
if __name__ == '__main__':
    master = tk.Tk()
    woCal = WoCal(master)
    master.mainloop()
