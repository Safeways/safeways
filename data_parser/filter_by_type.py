import pandas as pd

#severe crimes, as determined by group memembers:
SEVERE_CRIMES = ("[UIPD] BATTERY", "[UIPD] CARRYING OUT OF PREMISE", "[UIPD] ROBBERY", "[UIPD] ROBBERY-ARMED",
                 "[UIPD] WARRANT-IN-STATE", "[UIPD] MENTAL CASE-TRANSPORTATION", "[UIPD] ROBBERY-AGGRAVATED",
                 "[UIPD] BOMB THREAT", "[UIPD] BATTERY-AGGRAVATED", "[UIPD] POSS ALCOHOL PUB PROP / PARKING LOT",
                 "[UIPD] UNLAWFUL POSS FIREARM & AMMUNITION", "[UIPD] UNLAWFUL USE OF WEAPONS",
                 "[UIPD] ARSON-AGGRAVATED", "[UIPD] PUBLIC URINATION", "[UIPD] SEARCH WARRANT SERVICE")

def filter_types(filename):
    """
    Removes entries from the CSV if it is not considered a 'severe crime'

    :param filename: file to remove crimes from
    """

    dataframe = pd.read_csv(filename)

    to_remove = [tp for tp in set(dataframe.incident_type_primary) if tp not in SEVERE_CRIMES]

    for tp in to_remove: dataframe = dataframe[dataframe.incident_type_primary != tp]

    dataframe.to_csv(path_or_buf="data_parser\\filtered_crime_data.csv", sep=",")
