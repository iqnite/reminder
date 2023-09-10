'''
Startup Reminder - Autorun checker script
Philipp D.
Jul. 2023
'''

from module import *
from datetime import datetime
from tkinter.messagebox import showinfo, showerror


def days_remaining(day, month):
    d1 = datetime.strptime(
        f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}", "%Y-%m-%d")
    d2 = datetime.strptime(
        f"{datetime.now().year}-{int(month)}-{int(day)}", "%Y-%m-%d")
    return (d2 - d1).days


'''
def time_remaining(day: int, month: int) -> int:
    cd = datetime.now().day
    if month - (cm := datetime.now().month) == 1:
        return month_len(cm, datetime.now().year) - cd + day
    elif month - cm > 1:
        return (month - cm) * 30
    elif month - cm < 0:
        return None
    elif month - cm == 0:
        return day - cd
'''


def main():
    try:
        import profile_1 as conf
        for i in conf.REMINDERS:
            if (d := days_remaining(i["day"], i["month"])) <= conf.INTERVAL and d >= 0:
                showinfo(title="Reminder!",
                        message=f"{i['name']} occurs in {d} days!")
    except FileNotFoundError: pass
    except:
        showerror(title="An error occurred", message="Reminders could not be checked. Try opening the Reminder app and saving the profile again.")

main()
