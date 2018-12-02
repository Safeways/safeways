import pandas as pd

def categorize_crimes():
    """ Determines:
    - Types of crimes present in the CU area
    - Broad categories that these crimes fall under
    - This data is then used to determine which crimes are 'severe'
    """

    dataframe = pd.read_csv("u_of_i_crime_data.csv")

    all_crime_categories = dataframe["parent_incident_type"]
    crime_cats = set(all_crime_categories)

    all_crime_types = dataframe["incident_type_primary"]
    crime_types = set(all_crime_types)

    crime_classification = {k : [] for k in crime_cats}

    for x in range(len(all_crime_categories)):
        if all_crime_types[x] not in crime_classification[all_crime_categories[x]]:
            crime_classification[all_crime_categories[x]].append(all_crime_types[x])

    #manually determined after discussions with team
    SEVERE_CRIMES = ("battery", "carrying out of premise", "robbery", "robbery-armed", "warrant-in state",
                     "mental case-transportation", "robbery-aggravated", "bomb threat", "battery-aggravated",
                     "poss alcohol pub prop / parking lot", "unlawful poss firearm & ammunition",
                     "unlawful use of weapons", "arson-aggravated", "public urination", "search warrant service")