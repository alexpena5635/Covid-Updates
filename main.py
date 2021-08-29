#!/usr/bin/env python3
import routes

import flask
import os

# Creating the flask app var
app = flask.Flask(__name__)
port = int(os.environ.get("PORT", 5000))

# Assigning components
app.register_blueprint(routes.pageID)

if __name__ == "main":
    app.run(host='0.0.0.0', port=port)