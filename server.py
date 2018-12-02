from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler

from services.update_csv import update_csv
from services.filter_by_type import filter_types
from services.filter_by_time import filter_old_data
from services.emphasis_frequency import dangerous, frequency_counter
from services.get_useful_data import get_useful_data
from services.clean_csv_files import clean_all

app = Flask(__name__)


def update_data():
    update_csv()
    filter_types("services\\u_of_i_crime_data.csv")
    filter_old_data("services\\filtered_by_type_crime_data.csv")
    danger_zones = dangerous(frequency_counter("services\\filtered_by_type_crime_data.csv"))
    get_useful_data(danger_zones)
    clean_all()
    print("Done")

scheduler = BackgroundScheduler()
job = scheduler.add_job(update_data, 'interval', days=1)
scheduler.start()

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)