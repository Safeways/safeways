import pandas as pd

def clean_type(file):
    """
    Reformats the type column of the recent severe crimes CSV. Removes the [UIPD] label and changes to sentence case.

    :param file: pandas dataframe of the CSV
    :return: reformatted dataframe
    """

    for i in range(len(file.type)):
        file.at[i,"type"] = file.at[i,"type"].replace("[UIPD] ","").capitalize()

    return file

def clean_descr(file):
    """
    Reformats the description column of the CSV.
    Removes repeated information and line breaks, then changes to sentence case and removes extraneous whitespace.

    :param file: pandas dataframe of the CSV
    :return: reformatted dataframe
    """

    for i in range(len(file.description)):
        file.at[i,"description"] = file.at[i,"description"].replace(str(file.at[i,"type"]).upper(),"",1)
        file.at[i, "description"] = file.at[i, "description"].replace(" <BR/><BR/>", "").capitalize().strip()

    return file

def clean_address(file):
    """
    Reformats the address columns of the CSV by changing to sentence case.

    :param file: pandas dataframe of the CSV
    :return: reformatted dataframe
    """

    for i in range(len(file.street_address)):
        file.at[i,"street_address"] = file.at[i,"street_address"].title()
        file.at[i, "city"] = file.at[i, "city"].title()

def clean_all():
    file = pd.read_csv("frontend_files\\recent_severe_crimes.csv")
    clean_address(clean_descr(clean_type(file)))
    file.to_csv(path_or_buf="frontend_files\\recent_severe_crimes.csv", sep=",", index=False)

