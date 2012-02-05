#!/usr/bin/env python

from flask import Flask, render_template, request
app = Flask(__name__)

import os

@app.route("/")
def list_folder():
    return render_template(
        'index.html'
    )

if __name__ == "__main__":
    app.run(debug=True)
