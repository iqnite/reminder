'''
Startup Reminder
Philipp D.
Jun. 2023
'''


import tkinter as tk
from tkinter.messagebox import showinfo, showerror, showwarning


class Config(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def __enter__(self):
        self.file = open(self.file_name, 'w')
        return self.file

    def __exit__(self, *args):
        self.file.close()


class ReminderApp (tk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.def_gui()
        self.build_gui()
        self.load()

    def def_gui(self):
        self.remindersFrame = tk.LabelFrame(self, text="Active reminders")
        self.remindersBox = tk.Listbox(
            self.remindersFrame, selectmode="single")

        self.optionsFrame = tk.Frame(self)
        self.addFrame = tk.LabelFrame(self.optionsFrame, text="Add reminder")
        self.addDayLabel = tk.LabelFrame(self.addFrame, text="Day")
        self.addDayInput = tk.Entry(self.addDayLabel)
        self.addMonthLabel = tk.LabelFrame(self.addFrame, text="Month")
        self.addMonthInput = tk.Entry(self.addMonthLabel)
        self.addNameLabel = tk.LabelFrame(self.addFrame, text="Name")
        self.addNameInput = tk.Entry(self.addNameLabel)
        self.addButton = tk.Button(
            self.addFrame, text="Add", command=self.add_to_list)

        self.removeFrame = tk.LabelFrame(
            self.optionsFrame, text="Remove selected reminder")
        self.removeButton = tk.Button(
            self.removeFrame, text="Remove", command=self.remove_from_list)

        self.intervalFrame = tk.LabelFrame(
            self.optionsFrame, text="Notification")
        self.intervalInfo = tk.Label(
            self.intervalFrame, text="Set how many days before the given date the app should remind you.\nReminders will only appear at startup.", wraplength=window.winfo_width()/3)
        self.intervalDays = tk.StringVar(self.intervalFrame)
        self.intervalInput = tk.Entry(
            self.intervalFrame, textvariable=self.intervalDays)
        self.intervalButton = tk.Button(
            self.intervalFrame, text="Save & check", command=self.verify)

    def build_gui(self):
        self.remindersFrame.pack(side="left", fill="both", expand=True)
        self.optionsFrame.pack(side="right", fill="both", expand=True)

        self.addFrame.pack(fill="both", expand=True)
        self.removeFrame.pack(fill="both", expand=True)
        self.intervalFrame.pack(fill="both", expand=True)

        self.remindersBox.pack(fill="both", expand=True)
        self.addNameLabel.pack(side="top", fill="x", expand=True)
        self.addDayLabel.pack(side="top", fill="x", expand=True)
        self.addMonthLabel.pack(side="top", fill="x", expand=True)
        self.addButton.pack(side="bottom", fill="none", expand=True)
        self.removeButton.pack(fill="none", expand=True)
        self.intervalInfo.pack(fill="both", expand=True)
        self.intervalInput.pack(fill="x", expand=True)
        self.intervalButton.pack(fill="none", expand=True)

        self.addDayInput.pack(fill="both", expand=True)
        self.addMonthInput.pack(fill="both", expand=True)
        self.addNameInput.pack(fill="both", expand=True)

    def add_to_list(self):
        name = self.addNameInput.get()
        if ("@" in name) or ('"' in name):
            showerror(title="Could not add reminder",
                      message="Name cannot contain the following characters: @ \".")
            return
        try:
            day = int(self.addDayInput.get())
            month = int(self.addMonthInput.get())
        except:
            showerror(title="Could not add reminder", message="Invalid date.")
            return
        if (not month in range(1, 13, 1)
                or not day in range(1, 32, 1)
                or ((month == 4 or month == 6 or month == 9 or month == 11) and day > 30)
                or (month == 2 and day > 29)
                ):
            showerror(title="Could not add reminder", message="Invalid date.")
            return
        self.remindersBox.insert(1, f"{name} @ {day}. {month}")
        self.save()

    def remove_from_list(self):
        self.remindersBox.delete(self.remindersBox.curselection()[0])
        self.save()

    def save(self):
        with Config("profile_1.py") as xprofile:
            xprofile.write(self.compile())
            try:
                int(self.intervalInput.get())
            except:
                showerror("Could not set interval",
                          message="Invalid interval number.")
                return
            xprofile.write(
                f"\nINTERVAL = {abs(int(self.intervalInput.get()))}")

    def verify(self):
        self.save()
        try:
            import remind_startup as run
        except ModuleNotFoundError:
            showerror(title="An error occurerd", message="Your settings were saved, but could not check for reminders because the module 'remind_startup.py' was not found in the current directory. Try downloading the program again.")
        else:
            try:
                run.main()
            except NameError:
                showerror(title="An error occurerd",
                          message="Your settings were saved, but could not check for reminders because the autorun module is corrupted. Try downloading the program again.")
            except:
                showwarning(title="An error occurerd",
                            message="An error occured while saving your settings. Please try again.")
            else:
                showinfo(
                    title="Success", message="Settings saved and reminders checked successfully.")

    def compile(self):
        result = []
        for i in self.remindersBox.get(0, "end"):
            reminder_tuple = i.split("@")
            name = reminder_tuple[0]
            date_tuple = reminder_tuple[1].split(".")
            day = date_tuple[0]
            month = date_tuple[1]
            result.append(
                "{" + f'"name": "{name}", "day": "{day}", "month": "{month}"' + '},')
        result_str = "REMINDERS = ["
        for j in result:
            result_str += j
        result_str += "]"
        return result_str

        '''reminders = "REMINDERS = ("
        mode = 0
        for j in self.remindersBox.get(0, -1):
            reminders += "("
            for i in j:
                if ((i == "@") and (mode == 0)) or ((i == ".") and (mode == 1)):
                    mode += 1
                if mode == 0:
                    reminders += i
            reminders += ","'''

    def load(self):
        try:
            import profile_1 as conf
            for i in conf.REMINDERS:
                self.remindersBox.insert(
                    1, f"{i['name']} @ {int(i['day'])}. {int(i['month'])}")
            self.intervalDays.set(conf.INTERVAL)
        except:
            self.intervalDays.set(1)


window = tk.Tk()
window.title("Startup Reminder - Settings")
window.geometry("500x600")
window.state("zoomed")
Main = ReminderApp(window)
Main.mainloop()
