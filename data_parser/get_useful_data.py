import pandas as pd

def crime_type_formatter(tp):
    """
    Cleans up the crime type given by the UIPD.
    i.e. UIPD crime type data is given as '[UIPD] UNLAWFUL USE OF WEAPONS'
    This method truncates it such that it becomes 'Unlawful use of weapons'

    :param tp: crime type string to format
    :return: truncated, well-formatted description
    """

    if "[UIPD]" in tp:
        tp = tp[7:]

    return tp.capitalize()

def crime_description_formatter(descr):
    """
    Cleans up the description given by UIPD

    :param descr: description to format
    :return: formatted description
    """

    descr = descr.replace("<BR/>","")
    return descr.capitalize()

def danger_level(freq):
    """
    Assigns a danger level to the area based on the amount of crime, on a scale of 0 - 10.

    :param freq: frequency of crime at a location
    :return: danger level of the location as calculated from the frequency
    """

    return freq // 10 if freq // 10 <= 10 else 10

def get_useful_data(filename, danger_zones):
    """
    Retrieves the information that the front-end needs to map and display the crime zones. Saves data as CSV.

    :param filename: file to get recent crimes from
    :param danger_zones: dictionary of dangerous areas mapped to frequency of crimes in that area
    :return recent_severe_crimes: pandas dataframe of key data from recent crimes for the frontend
    :return dangers: pandas dataframe of key data from the most dangerous areas for the frontend
    """

    recent_severe_crimes = pd.read_csv(filename)

    #important data for recent crimes:
    # - crime location (coordinates for map use only)
    # - crime time
    # - crime type
    # - crime description
    # - address (for human use only)
    important_recent = ("latitude","longitude","incident_datetime","incident_type_primary","incident_description",
                        "address_1","city","state","zip")

    for label in list(recent_severe_crimes.columns.values):
        if label not in important_recent:
            recent_severe_crimes = recent_severe_crimes.drop(columns=label)

    recent_severe_crimes = recent_severe_crimes.rename(columns={"incident_type_primary":"type",
                                                                "incident_description":"description",
                                                                "address_1":"street address",
                                                                "incident_datetime":"date and time"})

    #important data for danger zones
    # - central location
    # - frequency (emphasize the time period)
    dangers = pd.DataFrame({"latitude":[k[0] for k in danger_zones.keys()],
                           "longitutde":[k[1] for k in danger_zones.keys()],
                           "frequency":list(danger_zones.values()),
                            "danger level":[danger_level(v) for v in danger_zones.values()]})

    return recent_severe_crimes, dangers

def combine_data(recent_severe_crimes, danger_zones):
    """
    Combines all data into a single dataframe to pass to the front end

    :param recent_severe_crimes: dataframe with recent crime information
    :param danger_zones: dataframe with danger zone information
    :return: dataframe with information from both
    """

    pass
