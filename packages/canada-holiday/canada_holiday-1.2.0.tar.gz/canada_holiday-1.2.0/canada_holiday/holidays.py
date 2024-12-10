from calendar import Calendar
import datetime

from canada_holiday.holiday_info import national, all
from canada_holiday.holiday import CanadaHoliday
from canada_holiday.utils import (
    check_province_name,
    filter_list_of_holidays_by_month,
    sort_list_of_holidays,
    update_list_of_holidays,
)


cal = Calendar()


def get_province_holidays(prov: str, year: int = None) -> list:
    """
    Returns holidays that are specific to the given province.
    """
    province = check_province_name(prov)
    all_holidays_in_province = all.HOLIDAYS_DICT[province]
    print(f"Getting holiday information of {province} province...")

    # Combine with Canadian national holidays
    all_holidays_in_province.extend(national.HOLIDAYS)
    # Add 'year' information to holidays
    if year:
        for holiday in all_holidays_in_province:
            holiday["year"] = year
    return all_holidays_in_province


def get_holidays(province: str, year: int, month: int = None) -> list:
    """
    Get all holidays of the given province in the given year.
    If month is given, filter all_holidays for the given month.
    """
    holidays = get_province_holidays(province, year)
    holiday_objs = [convert_holiday_info_to_obj(h) for h in holidays]
    all_holidays = (
        filter_list_of_holidays_by_month(holiday_objs, month)
        if month and isinstance(month, int)
        else holiday_objs
    )

    # Update holiday objects to have date for the given year
    sorted_all_holidays = sort_list_of_holidays(all_holidays)
    return sorted_all_holidays


def is_holiday(date: datetime.date, prov: str) -> bool:
    """
    Check if the given datetime.date is a holiday for the given Canadian province.
    """
    province_name = check_province_name(prov)
    holidays_for_province = get_holidays(province_name, date.year, date.month)

    for h in holidays_for_province:
        if h.date == date:
            print(
                f"{date} is a holiday, {h.name} in {h.province} province(s) in Canada"
            )
            return True
        print(f"{date} is not a holiday in {province_name} province.")
        return False


def convert_holiday_info_to_obj(holiday_info: dict):
    return CanadaHoliday(
        name=holiday_info.get("name", None),
        month=holiday_info.get("month", None),
        year=holiday_info.get("year", None),
        day=holiday_info.get("day", None),
        day_of_the_week=holiday_info.get("day_of_the_week", None),
        date=holiday_info.get("date", None),
        nearest_day=holiday_info.get("nearest_day", None),
        nth_day=holiday_info.get("nth_day", None),
        preceding_date=holiday_info.get("preceding_date", None),
        province=holiday_info.get("province", None),
        succeeding_date=holiday_info.get("succeeding_date", None),
    )
