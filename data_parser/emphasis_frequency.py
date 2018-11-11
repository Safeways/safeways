import pandas as pd
import decimal

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

    THRESHHOLD = 5 # if the number of crimes in an area exceed threshhold, it is marked as a dangerous zone

    dataframe = pd.read_csv(filename)
    [lat,long] = [list(dataframe.latitude), list(dataframe.longitude)]

    count = {(truncate_2(lat[i]), truncate_2(long[i])):[] for i in range(len(lat))}
    for i in range(len(dataframe.latitude)):
        lat = truncate_2(dataframe.latitude[i])
        long = truncate_2(dataframe.longitude[i])
        count[lat, long].append(dataframe.loc[i,"date_and_time"])

    return count

def dangerous(counts):
    print(counts)
