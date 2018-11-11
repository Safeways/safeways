from update_csv import *
from filter_by_type import *
from filter_by_time import *
from emphasis_frequency import *
from get_useful_data import *

def main():
    update_csv()
    filter_types("u_of_i_crime_data.csv")
    filter_old_data("filtered_by_type_crime_data.csv")
    #danger_zones = frequency_counter("filtered_by_type_crime_data.csv")
    get_useful_data(danger_zones)


if __name__== "__main__":
    main()