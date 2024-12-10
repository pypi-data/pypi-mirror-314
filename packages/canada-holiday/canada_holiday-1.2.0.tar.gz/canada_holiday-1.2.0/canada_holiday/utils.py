import calendar
import datetime
import math
from typing import Union, Tuple


cal = calendar.Calendar()
DAY_TO_INDEX = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tuesday": 1,
    "wed": 2,
    "wednesday": 2,
    "thu": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}
INDEX_TO_DAY = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


def check_province_name(prov: str):
    province = prov.lower()

    if province in ["alberta", "ab"]:
        provincial_name = "Alberta"
    elif province in ["british columbia", "bc"]:
        provincial_name = "British Columbia"
    elif province in ["manitoba", "mb"]:
        provincial_name = "Manitoba"
    elif province in ["new brunswick", "nb"]:
        provincial_name = "New Brunswick"
    elif province in ["newfoundland", "newfoundland and labrador", "nl"]:
        provincial_name = "Newfoundland and Labrador"
    elif province in ["northwest territories", "nt"]:
        provincial_name = "Northwest Territories"
    elif province in ["nova scotia", "ns"]:
        provincial_name = "Nova Scotia"
    elif province in ["nunavut", "nu"]:
        provincial_name = "Nunavut"
    elif province in ["ontario", "on"]:
        provincial_name = "Ontario"
    elif province in ["prince edward island", "pe"]:
        provincial_name = "Prince Edward Island"
    elif province in ["quebec", "qc"]:
        provincial_name = "Quebec"
    elif province in ["saskatchewan", "sk"]:
        provincial_name = "Saskatchewan"
    elif province in ["yukon", "yt"]:
        provincial_name = "Yukon"
    else:
        raise Exception(
            f"Cannot find the given province: {prov}. Please check your input."
        )
    return provincial_name


def find_easter_day(year: int) -> datetime.date:
    """
    # Use algorithm to find the date of Easter day
    # Reference: https://www.geeksforgeeks.org/how-to-calculate-the-easter-date-for-a-given-year-using-gauss-algorithm/
    """
    a = year % 19
    b = year % 4
    c = year % 7
    p = math.floor(year / 100)
    q = math.floor((13 + 8 * p) / 25)
    m = 15 - q + p - (p // 4) % 30
    n = 4 + p - (p // 4) % 7
    d = (19 * a + m) % 30
    e = (n + 2 * b + 4 * c + 6 * d) % 7
    days = 22 + d + e

    # A corner case: when D is 29
    if (d == 29) and (e == 6):
        easter_day = datetime.date(year, 4, 19)
        return easter_day
    # Another corner case: when D is 28
    elif (d == 28) and (e == 6):
        easter_day = datetime.date(year, 4, 18)
        return easter_day
    else:
        # If days > 31, move to April
        if days > 31:
            easter_day = datetime.date(year, 4, days - 31)
            return easter_day
        else:
            # Otherwise, stay on March
            easter_day = datetime.date(year, 3, days)
            return easter_day


def update_list_of_holidays(holiday_objs: list, year: int) -> list:
    """
    Update holidays to have date information on their instance.
    """
    updated_holidays_list = holiday_objs.copy()
    for h in updated_holidays_list:
        h.year = year
        h.date = h.to_date(year)
        h.day = h.date.day
        h.day_of_the_week = INDEX_TO_DAY[h.date.weekday()]
    return updated_holidays_list


def sort_list_of_holidays(holidays: list) -> list:
    """
    Sort the given list of Holidays bt their date.
    """
    return sorted(holidays, key=lambda h: h.date)


def filter_list_of_holidays_by_month(holidays: list, month: int) -> list:
    """
    Filter the given list of Holidays by the given month.
    """
    return [h for h in holidays if h.month == month]


def get_last_day_str_of_month(year: int, month: int, day_str: str) -> datetime.date:
    """
    Find the last day string of the month.
    ex: last Sunday of the given month
    """
    day_idx = DAY_TO_INDEX[day_str]
    weeks = cal.monthdatescalendar(year, month)
    return (
        weeks[-1][day_idx] if weeks[-1][day_idx].month == month else weeks[-2][day_idx]
    )


def parse_preceding_day_str(preceding_day: str):
    preceding_day_str_list = preceding_day.split()
    if len(preceding_day_str_list) < 2:
        raise Exception(
            f"Please check the preceding day, ${preceding_day} of the month"
        )
    return preceding_day_str_list


def get_day_of_the_week_idx(
    day_condition: Tuple[str, Union[int, str]]
) -> Tuple[int, Union[int, str]]:
    day_of_the_week, condition = day_condition
    return DAY_TO_INDEX[day_of_the_week], condition
