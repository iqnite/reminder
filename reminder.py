"""
Startup Reminder
Philipp D.
Jun. 2023
"""

import tkinter as tk
from tkinter.messagebox import showinfo, showerror, showwarning


class Config(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def __enter__(self):
        self.file = open(self.file_name, "w")
        return self.file

    def __exit__(self, *args):
        self.file.close()


class ReminderApp(tk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.def_gui()
        self.build_gui()
        self.load()

    def def_gui(self):
        self.remindersFrame = tk.LabelFrame(self, text="Active reminders")
        self.remindersBox = tk.Listbox(self.remindersFrame, selectmode="browse")

        self.optionsFrame = tk.Frame(self)
        self.addFrame = tk.LabelFrame(self.optionsFrame, text="Add reminder")
        self.addDayLabel = tk.LabelFrame(self.addFrame, text="Day")
        self.addDay = tk.StringVar(self.addDayLabel)
        self.addDayInput = tk.Entry(self.addDayLabel, textvariable=self.addDay)
        self.addMonthLabel = tk.LabelFrame(self.addFrame, text="Month")
        self.addMonth = tk.StringVar(self.addMonthLabel)
        self.addMonthInput = tk.Entry(self.addMonthLabel, textvariable=self.addMonth)
        self.addNameLabel = tk.LabelFrame(self.addFrame, text="Name")
        self.addName = tk.StringVar(self.addNameLabel)
        self.addNameInput = tk.Entry(self.addNameLabel, textvariable=self.addName)
        self.addButton = tk.Button(self.addFrame, text="Add", command=self.add_to_list)

        self.selectFrame = tk.LabelFrame(self.optionsFrame, text="Selected reminder")
        self.removeButton = tk.Button(
            self.selectFrame, text="Remove", command=self.remove_from_list
        )
        self.copyButton = tk.Button(self.selectFrame, text="Copy", command=self.copy)

        self.intervalFrame = tk.LabelFrame(self.optionsFrame, text="Notification")
        self.intervalInfo = tk.Label(
            self.intervalFrame,
            text="Set how many days before the given date the app should remind you.\nReminders will only appear at startup.",
            wraplength=window.winfo_width() / 3,
        )
        self.intervalDays = tk.StringVar(self.intervalFrame)
        self.intervalInput = tk.Entry(
            self.intervalFrame, textvariable=self.intervalDays
        )
        self.intervalButton = tk.Button(
            self.intervalFrame, text="Save & check", command=self.verify
        )

    def build_gui(self):
        self.remindersFrame.pack(side="left", fill="both", expand=True)
        self.optionsFrame.pack(side="right", fill="both", expand=True)

        self.addFrame.pack(fill="both", expand=True)
        self.selectFrame.pack(fill="both", expand=True)
        self.intervalFrame.pack(fill="both", expand=True)

        self.remindersBox.pack(fill="both", expand=True)
        self.addNameLabel.pack(side="top", fill="x", expand=True)
        self.addDayLabel.pack(side="top", fill="x", expand=True)
        self.addMonthLabel.pack(side="top", fill="x", expand=True)
        self.addButton.pack(side="bottom", fill="none", expand=True)
        self.removeButton.pack(fill="none", expand=True, side="left")
        self.copyButton.pack(fill="none", expand=True, side="right")
        self.intervalInfo.pack(fill="both", expand=True)
        self.intervalInput.pack(fill="x", expand=True)
        self.intervalButton.pack(fill="none", expand=True)

        self.addDayInput.pack(fill="both", expand=True)
        self.addMonthInput.pack(fill="both", expand=True)
        self.addNameInput.pack(fill="both", expand=True)

    def add_to_list(self):
        name = self.addName.get()
        if ("@" in name) or ('"' in name):
            showerror(
                title="Could not add reminder",
                message='Name cannot contain the following characters: @ "',
            )
            return
        try:
            day = int(self.addDay.get())
            month = int(self.addMonth.get())
        except:
            showerror(title="Could not add reminder", message="Invalid date.")
            return
        if (
            not month in range(1, 13, 1)
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

    def copy(self):
        tp = self.get_date(self.remindersBox.get(self.remindersBox.curselection()[0]))
        self.addName.set(tp["name"])
        self.addDay.set(tp["day"])
        self.addMonth.set(tp["month"])

    def save(self):
        with Config("profile_1.py") as xprofile:
            xprofile.write(self.compile())
            try:
                int(self.intervalInput.get())
            except:
                showerror("Could not set interval", message="Invalid interval number.")
                return
            xprofile.write(f"\nINTERVAL = {abs(int(self.intervalInput.get()))}")

    def verify(self):
        self.save()
        try:
            import remind_startup as run
        except ModuleNotFoundError:
            showwarning(
                title="An error occurerd",
                message="Your settings were saved, but could not check for reminders because the module 'remind_startup.py' was not found in the current directory. Try downloading the program again.",
            )
        else:
            try:
                run.main()
            except NameError:
                showwarning(
                    title="An error occurerd",
                    message="Your settings were saved, but could not check for reminders because the autorun module is corrupted. Try downloading the program again.",
                )
            except:
                showwarning(
                    title="An error occurerd",
                    message="An error occured while saving your settings. Please try again.",
                )
            else:
                showinfo(
                    title="Success",
                    message="Settings saved and reminders checked successfully.",
                )

    @staticmethod
    def get_date(item):
        reminder_tuple = item.split("@")
        name = reminder_tuple[0]
        date_tuple = reminder_tuple[1].split(".")
        day = date_tuple[0]
        month = date_tuple[1]
        return {"name": name, "day": day, "month": month}

    def compile(self):
        result = []
        for i in self.remindersBox.get(0, "end"):
            tp = self.get_date(i)
            result.append(
                "{"
                + f'"name": "{tp["name"].strip(" ")}", "day": "{tp["day"]}", "month": "{tp["month"]}"'
                + "},"
            )
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
                    1, f"{i['name']} @ {int(i['day'])}. {int(i['month'])}"
                )
            self.intervalDays.set(str(conf.INTERVAL))
        except:
            self.intervalDays.set(str(1))


window = tk.Tk()
window.title("Startup Reminder - Settings")
window.geometry("500x600")
window.state("zoomed")
main = ReminderApp(window)
main.mainloop()
