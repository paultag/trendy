#!/usr/bin/env python

from flask import Flask, render_template, request
app = Flask(__name__)

import os
import charlie
import json

# End setup

@app.route("/")
def list_folder():
    return render_template(
        'index.html'
    )

def load_location_data():
    hs = [ "x", "y", "name" ]
    inf = open("tlocs", 'r').readlines()
    inf = [ s.strip().split(",") for s in inf ]
    stop_trans = {}
    for line in inf:
        l = {}
        for x in range(0,len(hs)):
            try:
                line[x] = int(line[x])
            except Exception:
                pass
            l[hs[x]] = line[x]
        stop_trans[l['name']] = l
    return stop_trans

@app.route("/trains.json")
def get_json():
    charlie.refresh()
    ret = []
    locd = load_location_data()

    for train in charlie.train_list:
        train = charlie.train_list[train]
        curStop = train.getNextEvent()
        if not curStop:
            continue
        try:
            preStop = train.getStop( curStop["prev"] )
        except KeyError:
            continue

        if not preStop:
            continue

        time = curStop["TargetTime"] - preStop["TargetTime"]

        curStation = charlie.get_station_by_stop( curStop["PlatformKey"] )
        preStation = charlie.get_station_by_stop( preStop["PlatformKey"] )

        curLoc = locd[curStation.name]
        preLoc = locd[preStation.name]

        payload = {
            "id" : train.name,
            "root" : {
                "id" : curLoc["name"],
                "x"  : curLoc["x"],
                "y"  : curLoc["y"]
            },
            "dest" : {
                "id" : preLoc["name"],
                "x"  : preLoc["x"],
                "y"  : preLoc["y"]
            },
            "time" : time.seconds
        }
        ret.append(payload)

    return render_template(
        "json",
        json=json.dumps(ret)
    )

if __name__ == "__main__":
    app.run(debug=True)
