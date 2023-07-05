'''
Startup Reminder - Autorun checker script
Philipp D.
Jul. 2023
'''


from datetime import datetime
from tkinter.messagebox import showinfo


def switch_year(year: int) -> bool:
    if year % 4 == 0:
        if not year % 100 == 0:
            return True
        else:
            if year % 400 == 0:
                return False
            else:
                return False
    else:
        return False


def month_len(month: int, year: int = 1) -> int:
    if not (month in range(1, 13, 1)):
        raise ValueError
    elif (month == 4 or month == 6 or month == 9 or month == 11):
        return 30
    elif (month == 2 and switch_year(year)):
        return 29
    elif month == 2:
        return 28
    else:
        return 30


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
    import profile_1 as conf
    for i in conf.REMINDERS:
        if (d := days_remaining(i["day"], i["month"])) <= conf.INTERVAL and d >= 0:
            showinfo(title="Reminder!",
                     message=f"{i['name']} occurs in {d} days!")


main()
