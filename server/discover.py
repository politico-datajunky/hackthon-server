# coding: utf-8

import random
from flask import jsonify, request
from server import app

@app.route('/discover_home', methods=['POST'])
def discover_home():
    random_number = random.randint(1, 10)