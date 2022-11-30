from flask import Flask, render_template, request, Response
from PIL import Image, ImageDraw
from io import BytesIO
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
    length = request.args.get("length", 100)
    height = request.args.get("height", 100)
    rounds = request.args.get("rounds", 3)
    if request.args.get("start", 0) == 1:
        r = requests.get(f"http://host.docker.internal:8100/api/fly/{length}/{height}/{rounds}")

    return render_template("drone.html", length=length, height=height, rounds=rounds)

# Api route to make 
@app.get("/api/dronepath/<int:length>.<int:height>.png")
def dronepath_api(length: int, height: int):
    im = Image.new("RGB", (250, 250), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw.rectangle(
        [
            (
                (im.width-length)/2,
                (im.height-height)/2
            ),
            (
                (im.width+length)/2,
                (im.height+height)/2
            )
        ],
        outline=(0, 0, 0),
        width=2
    )

    output = BytesIO()
    im.save(output, format="png")

    return Response(output.getvalue(), mimetype="image/png")

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
    r = requests.get(f"http://{data_analysis_host}:8090/api/bssiddatapoints/{bssid}")
    datapoints = r.json()

    return render_template("bssid_data.html", bssid=bssid, datapoints=datapoints)

# Start server when run directly
if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
