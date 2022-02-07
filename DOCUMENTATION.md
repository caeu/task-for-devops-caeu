### Task 1 design and comments
`Flask` is python micro web application that is light, fast and relatively simple to work with, it seems fit for this task.
Since there are no actual webpages served in this application, only a single python file is created, i.e., no template or static directories.

This app requires the `requests`, `flask-caching` and optionally yet recommended the `gunicorn`. All dependencies are listed in the `requirements.txt` file.

The app workflow:
1) take the incoming request
2) extract the uri from the request
3) concatenate it to the source URL and send a request
4) send back the content as json


A dummy backend function is intended for future new features (currently dummy function)


To start the app webserver locally, navigate to directory underwhich `app.py` is located and run:

```
flask run
```

5000 is The default port for Flask to run locally:  `http://127.0.0.1:5000/`

To test, open this link in the browser: `http://127.0.0.1:5000/restaurants`


Note that multithreading is enabled, and the app will start in debug mode

Also, Caching is enbaled with default cache expiry time of 10 seconds.

If this port is occupied by other applications, you can run on a different port, for e.g.:

```
flask run --port=5400
```

Test cases are included. To run them first start the app server (above) then run:
```
python3 ./test_app.py
```

To deploy the server for production, it is recommended NOT to use Flask build-in server, but rather the gunicorn one.
```
gunicorn --bind "0.0.0.0:8000" app:app
```

Optionally, one can add more workers [default 1], upto `(2 * $num_cores) + 1` e.g. if the server has 4 cores:
```
gunicorn --workers 9 ---bind "0.0.0.0:8000" app:app
```
Also optionally, one can add enable multi threading [default 1]. Note that if multi workers are set, then threading will be in gthread mode.
```
gunicorn --threads 2 --bind "0.0.0.0:8000" app:app
```

To stop the server app, flask or gunicorn, kill the process with `Ctrl-c`


