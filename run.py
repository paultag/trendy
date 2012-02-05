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


@app.route("/trains.json")
def get_json():
    ret = []
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

    for train in charlie.train_list:
        train = charlie.train_list[train]
        platform = train.getLastKnownPlatform()
        station  = charlie.station_list[ \
            charlie.stop_list[platform].getStationName()]
        try:
            ret.append({
                "trip"     : train.getTrip(),
                "station"  : station.name,
                "platform" : stop_trans[station.name],
            })
        except KeyError as e:
            pass
    return render_template(
        "json",
        json=json.dumps(ret)
    )

if __name__ == "__main__":
    app.run(debug=True)
