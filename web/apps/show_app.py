#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/22
@des:
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/rain_stars")
def rain_stars():
    return render_template("rain_star.html")


@app.route("/fireworks")
def fireworks():
    return render_template("fireworks.html")


if __name__ == "__main__":
    app.run()
