#!/usr/bin/env python3
import flask
import os

import routes
from utils import get_config

# Assign flask app and port
app = flask.Flask(__name__)
port = int(os.environ.get("PORT", 5000))

# Assigning components
app.register_blueprint(routes.page_id)

# Load config from config.json
# If development environment, turn on flask debug mode
config = get_config()
if config["env"] == "dev":
    app.config["DEBUG"] = True


if __name__ == "main" or __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
