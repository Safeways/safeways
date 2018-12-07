from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler

from services.driver import main as update_data
from services.csv_to_string import csv_to_string as convert

#Main server
app = Flask(__name__)

scheduler = BackgroundScheduler()
job = scheduler.add_job(update_data, 'interval', days=1)
scheduler.start()

@app.route("/")

@app.route("/index.html", methods = ['GET'])
def index():
    danger, recent, severity = convert()
    return render_template("index.html", recent=recent)

@app.route("/about.html", methods = ['GET'])
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)