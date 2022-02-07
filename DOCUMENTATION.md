### Task 1 design and comments
`Flask` is python micro web application that is light, fast and relatively simple to work with. It seems fit for this task.
Since there are no actual webpages served in this application, only a single python file is created, i.e., no template or static directories.

This a python 3 app and requires installation of other python modules `requests`, `flask-caching` and optionally yet recommended `gunicorn` for deployment. All dependencies are listed in the `requirements.txt` file.

The app workflow:
1) take the incoming request
2) extract the `uri` from the request
3) concatenate it to the source `api` and send a request
4) send back the content as json


A dummy backend function is intended for future new features (currently dummy function).


To start the app web server locally, navigate to the directory underwhich `app.py` is located and run:

```
flask run
```

5000 is the default port for Flask to run locally:  `http://127.0.0.1:5000/`

To test, open this link in the browser: `http://127.0.0.1:5000/restaurants` you should get back a json response (restaurants)


Note that multithreading is enabled, and the app will start in debug mode

Also, caching is enbaled with cache expiry time set to 10 seconds.

If the port `5000` is occupied by other applications, start the server on a different port, for e.g.:

```
flask run --port=5400
```

Test cases are included. The app server should be running (above) to run the tests:
```
python3 ./test_app.py
```

To deploy the server for production, it is recommended NOT to use Flask build-in server, but rather the gunicorn one.
```
gunicorn --bind "0.0.0.0:8000" app:app
```

Optionally, one can add more workers [default 1], upto `(2 * $num_cores) + 1` ,where `$num_cores` is the number of cpu cores of the machine, e.g. if the machine has 4 cores:
```
gunicorn --workers 9 ---bind "0.0.0.0:8000" app:app
```
Also optionally, one can enable multi threading [default 1]. Note that if multi workers are set, then threading will be in gthread mode.
```
gunicorn --threads 2 --bind "0.0.0.0:8000" app:app
```

To stop the server app, flask or gunicorn, kill the process with `Ctrl-c`


