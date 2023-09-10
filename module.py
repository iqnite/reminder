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