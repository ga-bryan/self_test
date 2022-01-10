#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/29
@des:   
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"
