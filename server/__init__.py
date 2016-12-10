from flask import Flask

app = Flask(__name__)
app.config.from_object('server.settings.DevelopmentConfig')

import user
import topic
import requirements
import discover
import ground
import skill
