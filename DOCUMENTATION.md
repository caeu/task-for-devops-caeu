### Task 1 design and comments
`Flask` is python micro webapplication that is light, fast and relatively simple to work with. It seems fit for this task.
Since there are no actual webpages served in this application, only a single python file is created, i.e., no template or static directories.

To run this app, the `requests` library will be imported as well.

The app take a get request, extract the uri and concatenate it to the source URL to sends get request.
Then reads the response as json, parse it as a dictionary and send it to a backend function for processing (currently dummy function)

The function returns the object to main app to be sent as json.

To start the app webserver, navigate to directory underwhich `app.py` is located

and run:

```flask run```

5000 is The default port for Flask to run locally:  `http://127.0.0.1:5000/` 

If this port is occupied by other applications, you can run on a different port, for e.g.:

```flask run --port=5400```
