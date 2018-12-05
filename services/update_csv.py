import requests

def update_csv():
    """ Makes a request to the crime data api and saves the new data to the same CSV file. """

    url = "https://moto.data.socrata.com/api/views/3h5f-6xbh/rows.csv?accessType=DOWNLOAD"
    request = requests.get(url)

    with open("../services/u_of_i_crime_data.csv","wb") as file:
        file.write(request.content)