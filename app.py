import requests
from flask import Flask

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


# main route
# using 'path' type to allow '/' for subpaths
@app.route("/<path:uri>")
def relay(uri):
    response = requests.get(Dcbtube_url + uri)
    content = response.json()
    content = backend(content)
    
    return content


if __name__ == "__main__":
    app.run(debug=True, threaded=True)