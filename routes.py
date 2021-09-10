# import vars
import storage

import flask
import json

pageID = flask.Blueprint('appID', __name__, template_folder='templates')

# Route for when all counties are wanted in idaho
@pageID.route('/api/Idaho', methods=['GET'])
def getDataID():
    # Get Covid Data from DB
    data = storage.postgresGETIdahoData()
    return data

# Route for when county is requested specfically
@pageID.route('/api/Idaho/<county>', methods=['GET'])
def getDataIDByCounty(county):
    # Get Covid Data from DB
    counties = getDataID()
   
    counties = json.loads(counties)

    # for c in counties:
    #     print(c)
    
    data = ""
    for c in counties:
        #print(c['county'].lower(), county)
        if ( c['county'].lower() == county.lower() ):
            data = json.dumps(c)
            #print(data)

    if not bool(data):
        return "ERROR: County not found"
    
    return data
