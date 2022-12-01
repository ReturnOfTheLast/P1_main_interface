"""Main file: Flask http server that serves the frontend view of the project
"""

# Import modules
from flask import Flask, render_template, request, Response
from PIL import Image, ImageDraw
from io import BytesIO
import requests
import argparse

# Docker flag for docker networking
parser = argparse.ArgumentParser()
parser.add_argument('--docker', action="store_true", default=False, dest="docker")
args = parser.parse_args()

# Set the hostname of the data analysis engine
data_analysis_host = "localhost"

# Use internal docker dns resolution for data analysis engine host
# if the docker flag is set
if args.docker: data_analysis_host = "data_analysis_engine"

# Make flask application
app = Flask(__name__)

@app.get("/")
def index_view():
    """Endpoint for the index of the server.
    """

    # Render the index html template
    return render_template("index.html")

@app.get("/drone")
def drone_view():
    """Endpoint for the drone controller view.
    """

    # Get settings from the get request parameters
    length = request.args.get("length", 100)
    height = request.args.get("height", 100)
    rounds = request.args.get("rounds", 3)
    
    # Check if the drone should start
    if request.args.get("start", 0) == 1:
        # Hit the drone controller api endpoint
        r = requests.get(f"http://host.docker.internal:8100/api/fly/{length}/{height}/{rounds}")

    # Render the drone html template
    return render_template("drone.html", length=length, height=height, rounds=rounds)

@app.get("/api/dronepath/<int:length>.<int:height>.png")
def dronepath_api(length: int, height: int):
    """Simple api endpoint to draw the drone path.

    Args:
        length (int): Length of the path
        height (int): Height of the path
    """

    # Make pillow image and drawing tool
    im = Image.new("RGB", (250, 250), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)

    # Draw the path
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

    # Make file buffer and save the image as an png in it
    output = BytesIO()
    im.save(output, format="png")
    
    # Return the png image
    return Response(output.getvalue(), mimetype="image/png")

@app.get("/data")
def data_view():
    """Endpoint for the data analysis view.
    """

    # Get ssid/bssid filter settings from GET request parameters
    ftype = request.args.get("ftype", 2)
    fstr = request.args.get("fstr", "")

    # Make temp args for ssid overview (avoid issues with empty params)
    arg1 = ftype if len(fstr) != 0 else 2
    arg2 = fstr if len(fstr) != 0 else '0'

    # Make internal request for ssid / bssid data
    r = requests.get(f"http://{data_analysis_host}:8090/api/ssidoverview/{arg1}/{arg2}") 
    listview = r.json()

    # Render the data analysis view with the data html template
    return render_template("data.html", ftype=ftype, fstr=fstr, listview=listview)

@app.get("/data/bssid/<string:bssid>")
def bssid_data_view(bssid: str):
    """Data view for a single bssid.

    Args:
        bssid (str): BSSID to view data for
    """

    # Make internal request for datapoints
    r = requests.get(f"http://{data_analysis_host}:8090/api/bssiddatapoints/{bssid}")
    datapoints = r.json()

    # Render the bssid data html template
    return render_template("bssid_data.html", bssid=bssid, datapoints=datapoints)

if __name__ == "__main__":
    # Start the flask server when run
    app.run("0.0.0.0", 8080)
