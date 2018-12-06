from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler

from services.driver import main as update_data

#Main server
app = Flask(__name__)


scheduler = BackgroundScheduler()
job = scheduler.add_job(update_data, 'interval', days=1)
scheduler.start()

@app.route("/")


@app.route("/index.html", methods = ['GET'])
def index():
    return render_template("index.html")

@app.route("/about.html", methods = ['GET'])
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)