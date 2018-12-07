from services.update_csv import *
from services.filter_by_type import *
from services.filter_by_time import *
from services.emphasis_frequency import *
from services.get_useful_data import *
from services.clean_csv_files import *
from services.csv_to_string import *

def main():
    update_csv()
    filter_types("services/u_of_i_crime_data.csv")
    filter_old_data("services/filtered_by_type_crime_data.csv")
    danger_zones = dangerous(frequency_counter("services/filtered_by_type_crime_data.csv"))
    get_useful_data(danger_zones)
    clean_all()
    print("Data updated.")
    return csv_to_string()


if __name__== "__main__":
    main()