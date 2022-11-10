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

if __name__ == "__main__":
    app.run("localhost", 8080)
