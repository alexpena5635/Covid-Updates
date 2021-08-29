#!/usr/bin/env python3
#from storage import testPostgres
import routes

import flask
import os

# Creating the flask app var
app = flask.Flask(__name__)
port = int(os.environ.get('PORT', 5000))

# Assigning components
app.register_blueprint(routes.pageID)

#app.config['DEBUG'] = True

if __name__ == "main" or __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
    #testPostgres()