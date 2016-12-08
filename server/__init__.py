from flask import Flask

app = Flask(__name__)
app.config.from_object('server.settings.DevelopmentConfig')

import topic
import user
