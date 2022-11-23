from flask import Flask, render_template, request
import requests
import argparse

# Optional docker flag
parser = argparse.ArgumentParser()
parser.add_argument('--docker', action="store_true", default=False, dest="docker")
args = parser.parse_args()

data_analysis_host = "localhost"

if args.docker:
    data_analysis_host = "data_analysis_engine"

app = Flask(__name__)

# Index / Frontsite
@app.get("/")
def index_view():
    return render_template("index.html")

# Drone Controller
@app.get("/drone")
def drone_view():
    return render_template("drone.html")

# Data Analysis
@app.get("/data")
def data_view():
    ftype = request.args.get("ftype", 2)
    fstr = request.args.get("fstr", "")

    arg1 = ftype if len(fstr) != 0 else 2
    arg2 = fstr if len(fstr) != 0 else '0'

    r = requests.get(f"http://{data_analysis_host}:8090/api/ssidoverview/{arg1}/{arg2}") 
    listview = r.json()

    return render_template("data.html", ftype=ftype, fstr=fstr, listview=listview)

# Data Analysis - BSSID
@app.get("/data/bssid/<string:bssid>")
def bssid_data_view(bssid: str):
    r = requests.get(f"http://{data_analysis_host}:8090/api/bssiddatapoints/<string:bssid>")
    datapoints = r.json()

    return render_template("bssid_data.html", bssid=bssid, datapoints=datapoints)

# Data Analysis - SSID
@app.get("/data/ssid/<string:ssid>")
def ssid_data_view(ssid: str):
    return render_template("ssid_data.html", ssid=ssid)

if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
