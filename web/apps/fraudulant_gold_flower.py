#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/01/13
@des:   
"""

from flask import Flask, jsonify

app = Flask(__name__)

from design_parttern.fraudulant_gold_flower.model import FraudulentGoldFlower

flower = FraudulentGoldFlower()


@app.route("/start")
def pukes():
    pks = flower.send_pk()
    return jsonify(pks)
