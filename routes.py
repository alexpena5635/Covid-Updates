# import vars
import storage

import flask

pageID = flask.Blueprint('appID', __name__, template_folder='templates')
@pageID.route('/api/Idaho', methods=['GET']) # Will need to update the call to this from android studio since route changed
def getDataID():
    # Get Covid Data from DB
    data = storage.postgresGETIdahoData()

    return data