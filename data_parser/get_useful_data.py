import pandas as pd

def danger_level(freq):
    """
    Assigns a danger level to the area based on the amount of crime, on a scale of 0 - 10.

    :param freq: frequency of crime at a location
    :return: danger level of the location as calculated from the frequency
    """

    return int(freq // 10) if freq // 10 <= 10 else 10

def get_useful_data(danger_zones):
    """
    Retrieves the information that the front-end needs to map and display the crime zones. Saves data as CSV.
    :param danger_zones: dictionary of dangerous areas mapped to frequency of crimes in that area
    """

    #important data for danger zones
    # - central location
    # - frequency (emphasize the time period)
    dangers = pd.DataFrame({"latitude":[k[0] for k in danger_zones.keys()],
                           "longitude":[k[1] for k in danger_zones.keys()],
                           "frequency":[len(v) for v in danger_zones.values()],
                            "danger_level":[danger_level(len(v)) for v in danger_zones.values()]})

    dangers.to_csv("frontend_files\\danger_zones.csv",index=False)
