from update_csv import *
from filter_by_type import *
from filter_by_time import *
from emphasis_frequency import *

def main():
    update_csv()
    filter_types("data_parser\\u_of_i_crime_data.csv")
    filter_old_data("data_parser\\filtered_crime_data.csv")
    danger_zones = frequency_counter("data_parser\\u_of_i_crime_data.csv")


if __name__== "__main__":
    main()