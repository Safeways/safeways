import datetime
import pandas as pd

def deadline_time(threshhold):
    """
    Returns a date threshhold number of months before today's date

    :param threshhold: number of months to keep
    :return: threshhold date
    """

    [date, time] = str(datetime.datetime.now()).split(" ")
    [yr, month, day] = date.split("-")
    [hr, min, sec] = time.split(":")

    if (int(hr) > 12):
        hr = str(int(hr) - 12)
        suffix = "PM"
    else:
        suffix = "AM"

    deadline_month = (int(month) - threshhold) if int(month) >= (threshhold + 1) else (int(month) - threshhold) + 12
    deadline_year = str(yr) if int(month) >= (threshhold + 1) else str((int(yr) - threshhold//12))

    return deadline_year + "/" + str(deadline_month).zfill(2) + "/" + day.zfill(2) + " " \
            + hr.zfill(2) + ":" + min.zfill(2) + ":" + sec[:2].zfill(2) + " " + suffix

def flip_dates(datestring):
    """
    Flips the ordering of the components of the dates/times.
    CSV files gives dates and times in the format mm/dd/yy hh:mm:ss AMorPM
    Datetime gives it in the format yyyy-mm-dd hh:mm:ss.ms
    This function reformats datetime for accurate comparison to CSV

    :param datestring: date to flip
    :return: flipped date
    """
    [date,time,suffix] = datestring.split(" ")
    [month,day,year] = date.split("/")

    return year + "/" + month + "/" + day + " " + time + " " + suffix


def filter_old_data(filename):
    """
    Removes entries from the csv that occur before the threshhold date

    :param filename: file to remove entries from
    """

    dataframe =  pd.read_csv(filename)
    to_remove = set([dt for dt in dataframe.date_and_time if flip_dates(dt) < deadline_time(6)])

    for dt in to_remove: dataframe = dataframe[dataframe.date_and_time != dt]

    dataframe.to_csv(path_or_buf="services\\frontend_files\\recent_severe_crimes.csv", sep=",", index=False)