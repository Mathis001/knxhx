#!/usr/bin/python
from flask import jsonify, render_template, redirect
from flask.json import JSONEncoder
from flask_restplus import Api
from flask_cors import CORS
from pathlib import Path
import connexion
import json

api = Api(version='1.0', title='KNXHX API',
description='A simple Flask powered API for KNXHX')

# create the application instance
app = connexion.App(__name__, specification_dir='./')

# ignoring alphabetical json sort
app.app.config['JSON_SORT_KEYS'] = False

# Read the swagger.yml file to configure the endpoints
app.add_api('openapi.yaml')
CORS(app.app)

def readJSON(name, default, json_form):
    # Read in optional data, or set default values
    if name in json_form:
        result = json_form[name]
    else:
        result = default
    return result

# load configuration
with open('../config.json') as json_data_file:
    data = json.load(json_data_file)
    hostname = data["api"]["hostname"]
    port = data["api"]["port"]
    ssl = readJSON("ssl", "False", data["api"])
    cert = Path(readJSON("cert_location", "", data["api"]))
    key = Path(readJSON("key_location", "", data["api"]))

# Custom JSON encoder for times
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

# Create redirect message for "/", "/api", "/api/", "/api/v1", and "/api/v1/"
@app.route('/')
@app.route('/api')
@app.route('/api/')
@app.route('/api/v1')
@app.route('/api/v1/')

def home():
    return redirect("/api/v1/ui", code=302)

if __name__ == '__main__':
    if ssl == 'True' and cert.is_file() and key.is_file():
        context = (cert, key)
        app.run(host=hostname, port=port, ssl_context=context)
    else:
        app.run(host=hostname, port=port)
    app.debug = True
