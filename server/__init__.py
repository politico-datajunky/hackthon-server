from flask import Flask
app = Flask(__name__)


import server.user
import server.topic
import server.requirements
import server.discover