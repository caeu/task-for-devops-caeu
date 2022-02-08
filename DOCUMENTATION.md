# Task 1: Design and Instructions
`Flask` is python micro web application that is light, fast and relatively simple to work with. It seems fit for this task.
Since there are no actual webpages served in this application, only a single python file is created, i.e., no template or static directories.

This a python 3 app and requires installation of other python modules `requests`, `flask-caching` and optionally yet recommended `gunicorn` for deployment. All dependencies are listed in the `requirements.txt` file.

The app workflow:
1) take the incoming request
2) extract the `uri` from the request
3) concatenate it to the source `api` and send a request
4) send back the content as json


A dummy backend function is intended for future new features (currently dummy function).


To start the app web server locally, the make sure the dependencies in the `requirements.txt` are installed:
It is highly recommended to use virtual environment, e.g. venv, pipenv or any other.
```
pip3 install -r requirements.txt 
``` 
navigate to the directory under which `app.py` is located and run:

```
flask run
```

5000 is the default port for Flask to run locally:  `http://127.0.0.1:5000/`

To test, open this link in the browser: `http://127.0.0.1:5000/restaurants` you should get back a json response (restaurants)


Note that multi-threading is enabled, and the app will start in debug mode

Also, caching is enabled with cache expiry time set to 10 seconds.

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

  
<br />

# Task 2: Build and run in a Dockerized container:

#### Requirements:
1) Recent version of [Docker](https://docs.docker.com/get-docker/) is installed **and running** on the intended platform.

#### Building and running:
There are three options:
1) Building the image directly from this repo's url to the server or to the local computer
```
docker build "https://github.com/NBISweden/task-for-devops-caeu#master" -t latest
```

2) Or, pull a pre-built and published image on [docker-hub](https://hub.docker.com/repository/docker/caeu/taskfordevopscaeu)
```
docker pull "caeu/taskfordevopscaeu"
```
One can also use the `docker run` command to pull the image and run the container for images pulished on Docker-hub. The `-p` flag here is to set the port number of the docker container. This port number should match the `EXPOSE` entry in the `Dockerfile`.
```
docker run -p 8000:8000 "caeu/taskfordevopscaeu"
```

3) Or, for development purposes, clone this github repo, and build the image
```diff
git clone "https://github.com/NBISweden/task-for-devops-caeu" . 
# note the dot above is a shorthand for current directory

cd ./task-for-devops-caeu

docker build . 
# the dot here is a shorthand for the Dockerfile
```

Before running the docker container, check that it is build and listed
```
docker images
```
The command above will output a list of installed docker images, take note of the `IMAGE ID`

To run the container
```
docker run -p 8000:8000 <IMAGE ID>
```

To run the container in detached mode
```
docker run -d -p 8000:8000 <IMAGE ID>
```

To stop the container 
```
docker stop <IMAGE ID>
```

For help about docker command line
```
docker --help
```
