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
    Returns a decimal truncated to four decimal places

    :param num: decimal number to truncate
    :return: truncated number
    """
    return float("%.4f" % num)

def truncate_2(num):
    """
    Retruns a number truncated to two decimal places

    :param num: decimal number to truncate
    :return: truncated number
    """
    return float("%.2f" % num)

def frequency_counter(filename):
    """
    Counts how many times a crime occurs at the same place.
    'Same place' in this context means it is within the same section
    Sections are defined as areas within FINENESS of each other
    i.e. (i.e. (40.255,-88) and (40.255 + FINENESS,-88) are considered to be the same location)

    :param filename: filename to take crimes from
    :return: dictionary with coordinates (of blocks) mapped to frequency of crimes in that area
    """

    FINENESS = .02
    THRESHHOLD = 5 # if the number of crimes in an area exceed threshhold, it is marked as a dangerous zone

    dataframe = pd.read_csv(filename)
    [lat,long] = [list(dataframe.latitude), list(dataframe.longitude)]
    coordinates = [(truncate_4(lat[i]), truncate_4(long[i])) for i in range(len(lat))]

    min_lat = min(lat)
    max_lat = max(lat)
    min_long = min(long)
    max_long = max(long)

    count = {}

    for c in coordinates:
        lt = truncate_2(truncate_2(c[0]) if int(str(truncate_2(c[0]))[-1]) % 2 == 0 else truncate_2(c[0]) - FINENESS / 2)
        lg = truncate_2(truncate_2(c[1]) if int(str(truncate_2(c[1]))[-1]) % 2 == 0 else truncate_2(c[1]) - FINENESS / 2)

        if (lt, lg) not in count: count[(lt,lg)] = 1
        else: count[(lt,lg)] += 1

    return {k:v for k,v in count.items() if v > 5}



def main():
    dt = frequency_counter("C:\\Users\\MYChe\\PycharmProjects\\safeways\\data_parser\\u_of_i_crime_data.csv")
    print(dt)

if __name__== "__main__":
    main()
