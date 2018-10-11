#updates the json file with current crime data when called
import requests
import datetime
import pandas as pd

def update_csv():
    url = "https://moto.data.socrata.com/api/views/3h5f-6xbh/rows.csv?accessType=DOWNLOAD"
    request = requests.get(url)

    with open("u_of_i_crime_data.csv","wb") as file:
        file.write(request.content)

    #playing around with UofI police data
    import csv

    with open("u_of_i_crime_data.csv") as file:
        reader = csv.reader(file)
        crime_data = list(reader)

def address_formatter(street, city, state, zipcode):
    if (zipcode): 
        return street.title() + " " + city.capitalize() + ", " + state + " " + zipcode
    else: 
        return street.title() + " " + city.capitalize() + ", " + state

def print_report():
    for crime in crime_data[1:]:
        print("CRIME REPORT:")
        print("Date: " + crime[18] + " "+ crime[2][:crime[2].index(" ")])
        print("Time: " + crime[2][crime[2].index(" ") + 1:])
        print("Category: " + crime[19])
        print("Type: " + crime[3][crime[3].index(" ") + 1:].title())
        print("Address: " + address_formatter(crime[6], crime[8], crime[9], crime[10]))
        print("Coordinates: <" + crime[12] + ", " + crime[13] + ">\n")

def categorize_crimes():
    #analyzing crime types and rates
    dataframe = pd.read_csv("u_of_i_crime_data.csv")

    all_crime_categories = dataframe["parent_incident_type"]
    crime_cats = set(all_crime_categories)

    all_crime_types = dataframe["incident_type_primary"]
    crime_types = set(all_crime_types)

    crime_classification = {k : [] for k in crime_cats}

    for x in range(len(all_crime_categories)):
        if all_crime_types[x] not in crime_classification[all_crime_categories[x]]:
            crime_classification[all_crime_categories[x]].append(all_crime_types[x])

    severe_crimes = ("battery", "carrying out of premise", "robbery", "robbery-armed", "warrant-in state",
                     "mental case-transportation", "robbery-aggravated", "bomb threat", "battery-aggravated",
                     "poss alcohol pub prop / parking lot", "unlawful poss firearm & ammunition",
                     "unlawful use of weapons", "arson-aggravated", "public urination", "search warrant service")

def deadline_time(threshhold):
    # removes data that is older than threshhold number of months
    # csv format: "mm/dd/yy hh:mm:ss AMPM"
    # datetime format: "yyyy-mm-dd hh:mm:ss.ms"
    # reformats datetime to compare to csv
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
    #flips dates so that year goes first
    [date,time,suffix] = datestring.split(" ")
    [month,day,year] = date.split("/")

    return year + "/" + month + "/" + day + " " + time + " " + suffix


def filter_old_data():
    dataframe =  pd.read_csv("u_of_i_crime_data.csv")
    for dt in dataframe.incident_datetime:
        if flip_dates(dt) < deadline_time(6):
            dataframe = dataframe[dataframe.incident_datetime != dt]
    return dataframe