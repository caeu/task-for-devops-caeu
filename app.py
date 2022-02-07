import requests
from flask import Flask, abort, jsonify

# Source api
Dcbtube_url = 'https://menu.dckube.scilifelab.se/api/'


# Instantiate the flask app
app = Flask(__name__)


# Function for backend processing can be 
# extended or moved to another source file
def backend(content):
    '''
    Receives object of type dict
    '''
    # processing if needed
    
    return (content)

@app.errorhandler(404)
def api_error(e):
    # return error as json
    return jsonify(error=str(e)), 404


@app.errorhandler(501)
def api_error(e):
    # return error as json
    return jsonify(error=str(e)), 501


# main route
# using 'path' type to allow '/' for subpaths
@app.route("/<path:uri>")
def relay(uri):
    try:
        response = requests.get(Dcbtube_url + uri)
        content = backend(response.json())
        
        try:
            'application/json' in response.headers.get("Content-Type")
            return content
        
        except:
            abort(501, descrption = "Not implmented")
            
    except:
        abort(404, description = "Resource not found")
            
    

if __name__ == "__main__":
    app.run(debug=True, threaded=True)