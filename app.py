from flask import Flask, render_template, request

app = Flask(__name__)

# Index / Frontsite
@app.get("/")
def index_view():
    return render_template("index.html")

@app.get("/drone")
def drone_view():
    return render_template("drone.html")

@app.get("/data")
def data_view():
    ftype = request.args.get("ftype", "")
    fstr = request.args.get("fstr", "")

    listview = {
            "ssid 1": ["189377823925", "827390733912"],
            "ssid 2": ["189372983053", "084724652590", "739472952784"]
    }

    return render_template("data.html", ftype=ftype, fstr=fstr, listview=listview)

@app.get("/data/bssid/<string:bssid>")
def bssid_data_view(bssid: str):
    return render_template("bssid_data.html", bssid=bssid)

@app.get("/data/ssid/<string:ssid>")
def ssid_data_view(ssid: str):
    return render_template("ssid_data.html", ssid=ssid)

if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
