import requests
from flask import Flask, abort, jsonify
from flask_caching import Cache

# Source api
Dcbtube_url = 'https://menu.dckube.scilifelab.se/api/'


# Instantiate the flask app
app = Flask(__name__)

# setup flask config, mainly for cache
config = {"CACHE_TYPE": "SimpleCache",
         "CACHE_DEFAULT_TIMEOUT": 10
}

# tell Flask to use the above config
app.config.from_mapping(config)
cache = Cache(app)

# Function for backend processing can be 
# extended or moved to another source file
def backend(content):
    '''
    Receives object of type dict
    '''
    # processing if needed
    
    # print this message if cache is not used
    # just to test the cache is working
    print(f'new call or cache expired! calling external api')
    
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
@cache.cached()
def relay(uri):
    try:
        response = requests.get(Dcbtube_url + uri)
        response.raise_for_status()
        
        try:
            'application/json' in response.headers.get("Content-Type")
            content = backend(response.json())
            return content
        
        except:
            abort(501, descrption = "Not implmented")
            
    except:
        abort(404, description = "Resource not found")
            
    

if __name__ == "__main__":
    app.run(debug=True, threaded=True)