import pandas as pd
import decimal
from services.filter_by_time import flip_dates, deadline_time

def drange(start, end, increment):
    """
    Returns a discreet range from start to end using the increment

    :param start: start of the range, inclusive
    :param end: end of the range, non-inclusive
    :param increment: number to increment by
    :return: discreet range from start to end
    """
    start = decimal.Decimal(start)
    end = decimal.Decimal(end)
    while start < end:
        yield float(start)
        start += decimal.Decimal(increment)

def truncate_4(num):
    """
    Returns a number truncated to four decimal places

    :param num: decimal number to truncate
    :return: truncated number
    """
    return float("%.4f" % num)

def truncate_2(num):
    """
    Returns a number truncated to two decimal places

    :param num: decimal number to truncate
    :return: truncated number
    """
    return float("%.2f" % num)

def frequency_counter(filename):
    """
    Creates a dictionary that correlates a location with crimes that happen at that place.
    'Same place' in this context means it is within the same section
    Sections are defined as areas within .01 of each other
    i.e. (i.e. (40.255,-88) and (40.264,-88) are considered to be the same area)
    :param filename: filename to take crimes from
    :return: dictionary with coordinates (of blocks) mapped to the dates/times that crimes
            have happened at that location
    """
    dataframe = pd.read_csv(filename)
    [lat, long] = [list(dataframe.latitude), list(dataframe.longitude)]

    count = {(truncate_2(lat[i]), truncate_2(long[i])): [] for i in range(len(lat))}
    for i in range(len(dataframe.latitude)):
        lat = truncate_2(dataframe.latitude[i])
        long = truncate_2(dataframe.longitude[i])
        count[lat, long].append(dataframe.loc[i, "date_and_time"])

    return count


def dangerous(counts):
    """
    Using the counts dictionary returned by the previous function, chooses only the locations where crimes have
         occured more than 6 times in the past year.

    :param counts: dictionary of locations mapped to times that crimes have happened there
    :return: dictionary of same format but only with locations where crimes have happened recently
    """
    recent_only = {}
    for k, v in counts.items():
        count = 0
        for dt in v:
            if flip_dates(dt) > deadline_time(12):
                count += 1

        if count >= 6:
            recent_only[k] = v

    return recent_only