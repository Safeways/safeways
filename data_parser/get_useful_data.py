import pandas as pd

def crime_type_formatter(tp):
    """
    Cleans up the description given by the UIPD.
    i.e. UIPD description data is given as '[UIPD] UNLAWFUL USE OF WEAPONS'
    This method truncates it such that it becomes 'Unlawful use of weapons'

    :return: truncated, well-formatted description
    """

    if "[UIPD]" in tp:
        tp = tp[7:]

    return tp.capitalize()

def get_useful_data(filename):
    """ Retrieves the information that the front-end needs to map and display the crime zones. Saves data as CSV. """
    recent_severe_crimes = pd.read_csv(filename)

    #important data for recent crimes:
    # - crime location (coordinates for map use only)
    # - crime time
    # - crime type
    # - crime description
    # - address (for human use only)

    important_recent = ("latitude","longitude","incident_datetime","incident_type_primary","incident_description",
                        "address_1","address_2","city","state","zip")

    for label in list(recent_severe_crimes.columns.values):
        if label not in important_recent:
            recent_severe_crimes = recent_severe_crimes.drop(columns=label)

    #important data for danger zones
    # - crime location
    # - frequency (emphasize the time period)

    important_frequent = ("latitude","longitude")


def main():
    get_useful_data("filtered_crime_data.csv")


if __name__== "__main__":
    main()
