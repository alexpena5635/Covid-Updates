import flask

import storage

page_id = flask.Blueprint("appID", __name__, template_folder="templates")

# GET all county data for a given state
@page_id.route("/api/<state>", methods=["GET"])
def get_data(state):
    # Get Covid Data from DB
    counties_data = storage.get_state_data(state)
    return counties_data


# GET a single county's data for a given state
@page_id.route("/api/<state>/<county>", methods=["GET"])
def get_data_by_county(state, county):
    # Get covid data from DB
    county_data = storage.get_county_data(state, county)
    return county_data
