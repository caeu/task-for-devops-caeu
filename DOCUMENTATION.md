# Task 1: Design and Instructions
`Flask` is python micro web application that is light, fast, and relatively simple to work with. Therefore, it seems fit for this task.
Since no actual web pages are served in this application, only a single python file is created, i.e., no template or static directories.

This is a python3 app that depends on other python modules `requests`, `flask-caching`, and optionally yet recommended `gunicorn` for deployment. All dependencies are listed in the `requirements.txt` file.

The app workflow:
1) take the incoming request
2) extract the `uri` from the request
3) concatenate it to the source `api` and send a request
4) send back the content as json


A dummy backend function is intended for future new features (currently dummy function).


To start the app webserver locally, make sure the dependencies in the `requirements.txt` are installed:
It is highly recommended to use a virtual environment, e.g. venv, pipenv, or others.
```
pip3 install -r requirements.txt 
``` 
navigate to the directory under which `app.py` is located and run:

```
flask run
```

5000 is the default port for Flask to run locally:  `http://127.0.0.1:5000/`

To test, open this link in the browser: `http://127.0.0.1:5000/restaurants` you should get back a json response (restaurants)


Note that multi-threading is enabled, and the app will start in debug mode.

Also, caching is enabled with a cache expiry time set to 10 seconds.

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
Also optionally, one can enable multi-threading [default 1]. Note that if multi workers are set, threading will be in gthread mode.
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
1) Building the image directly from this repo's url to the server or the local computer
```
docker build "https://github.com/NBISweden/task-for-devops-caeu#master" -t latest
```

2) Or, pull a pre-built and published image on [docker-hub](https://hub.docker.com/repository/docker/caeu/taskfordevopscaeu)
```
docker pull "caeu/taskfordevopscaeu"
```
One can also use the `docker run` command to pull the image and run the container for images published on Docker-hub. The `-p` flag here is to set the port number of the docker container. This port number should match the `EXPOSE` entry in the `Dockerfile`.
```
docker run -p 8000:8000 "caeu/taskfordevopscaeu"
```

1) Or, for development purposes, clone this github repo, and build the image
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

# Task 3: Command Line Script

Included is a command-line tool written in python 3. The tool takes a restaurant name as an argument, and if the restaurant is in the `api` list of restaurants, it will list the dishes offered. Otherwise, it will output the full list of restaurants in Uppsala and Solna. To use the tool, for example, to view the dishes of restaurant "Restaurang Bikupan":
```
./restaurant_menu.py "Restaurang Bikupan"
```
Note that names with special characters should be quoted, or the special characters should be escaped.


# Optional Task: Run load tests
The load tests for the Flask app running on a gunicorn wsgi server within a docker container were implemented locally using three different http benchmark tools. All tests were configured to run for 28 seconds and simulated 20 concurrent connections. Cach-misses are calculated based on a simple print message implemented in the app that gets called within the cached main route function.

The reports show approximately similar results for the capacity of the app. The app server can handle ~2000 requests per second. However, the server's performance in more realistic tests is likely to be much lower due to network I/O constraints. The latency time measurements vary between the tests despite the similar setting configs. It seems there are also a few cache misses in flask-caching. The flask app caching timeout is set to 10 seconds. The cache misses are expected to be three within 28 seconds of a load test. However, the server logs show that the cache misses are slightly more. Further inspection of the actual logs of the server and outgoing requests of the host machine may help narrow down the causes of these relatively few cache misses.

To improve the performance, other than scaling up the network I\O, one can increase the cache timeout. However, this will increase the chances of returning expired results. Moreover, the tests shown here are conducted locally, i.e., the client and the server are on the same hardware. Therefore, realistic tests using specialized external services that can simulate actual internet requests will better reflect the server's capacity. Nevertheless, I would try to determine the bottlenecks, if any, to select the best strategy to improve performance with minimal cost. Also, try other manipulating the wsgi server, like the number of threads versus the number of workers, or try another wsgi server. If nothing helps, the next step would be investing in more hardware resources.

**UPDATE**
It turns out that the cache-misses (if I can call them such) are due to multi-threading. This makes sense. 
I re-did the tests with a single thread. The caching now looks as expected. However, the performance drop is about half.


1) Using [plow](https://github.com/six-ddc/plow)
```
> plow http://0.0.0.0:8000/restaurant/dufva -c20 -d28s

Benchmarking http://0.0.0.0:8000/restaurant/dufva for 28s using 20 connection(s).
@ Real-time charts is listening on http://[::]:18888

Summary:
  Elapsed        28s
  Count        53470
    2xx        53470
  RPS       1909.638
  Reads    0.967MB/s
  Writes   0.131MB/s

Statistics    Min      Mean     StdDev      Max
  Latency   1.013ms  10.465ms  16.325ms  748.766ms
  RPS       818.84   1909.49    232.55    2041.95

Latency Percentile:
  P50         P75      P90       P95       P99      P99.9     P99.99
  13.704ms  17.78ms  19.489ms  20.654ms  23.641ms  47.807ms  743.436ms

Latency Histogram:
  1.983ms    18285  34.20%
  5.317ms    10101  18.89%
  17.744ms   21547  40.30%
  19.421ms    2300   4.30%
  22.011ms    1058   1.98%
  41.659ms     162   0.30%
  736.977ms      9   0.02%
  743.645ms      8   0.01%
```

Server logs:
```
new call or cache expired! calling external apinew call or cache expired! calling external api

new call or cache expired! calling external apinew call or cache expired! calling external api

new call or cache expired! calling external apinew call or cache expired! calling external api

new call or cache expired! calling external api
new call or cache expired! calling external api
new call or cache expired! calling external api
new call or cache expired! calling external api
new call or cache expired! calling external api
new call or cache expired! calling external api
```

2) Using [hey](https://github.com/rakyll/hey)
```
> hey -z 28s -c 20 http://0.0.0.0:8000/restaurant/dufva

Summary:
  Total:	28.0084 secs
  Slowest:	0.0617 secs
  Fastest:	0.0020 secs
  Average:	0.0101 secs
  Requests/sec:	1975.3719

  Total data:	21024260 bytes
  Size/request:	380 bytes

Response time histogram:
  0.002 [1]	|
  0.008 [15546]	|?????????????????
  0.014 [35924]	|????????????????????????????????????????
  0.020 [3640]	|????
  0.026 [94]	|
  0.032 [4]	|
  0.038 [25]	|
  0.044 [34]	|
  0.050 [28]	|
  0.056 [21]	|
  0.062 [10]	|


Latency distribution:
  10% in 0.0068 secs
  25% in 0.0078 secs
  50% in 0.0099 secs
  75% in 0.0121 secs
  90% in 0.0135 secs
  95% in 0.0144 secs
  99% in 0.0168 secs

Details (average, fastest, slowest):
  DNS+dialup:	0.0000 secs, 0.0020 secs, 0.0617 secs
  DNS-lookup:	0.0000 secs, 0.0000 secs, 0.0000 secs
  req write:	0.0000 secs, 0.0000 secs, 0.0003 secs
  resp wait:	0.0096 secs, 0.0016 secs, 0.0609 secs
  resp read:	0.0005 secs, 0.0000 secs, 0.0319 secs

Status code distribution:
  [200]	55327 responses
```

Server Logs:
```
new call or cache expired! calling external api
new call or cache expired! calling external apinew call or cache expired! calling external api
new call or cache expired! calling external api

new call or cache expired! calling external api
new call or cache expired! calling external api
new call or cache expired! calling external apinew call or cache expired! calling external api

new call or cache expired! calling external api
new call or cache expired! calling external api
new call or cache expired! calling external api
new call or cache expired! calling external api
```

3) Using [wrk](https://github.com/wg/wrk)
```
> wrk -d 28s -c 20 -d30s http://0.0.0.0:8000/restaurant/dufva
Running 30s test @ http://0.0.0.0:8000/restaurant/dufva
  2 threads and 20 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     9.84ms    2.47ms  46.56ms   82.95%
    Req/Sec     1.03k    71.62     1.22k    81.67%
  61339 requests in 30.01s, 31.06MB read
Requests/sec:   2043.65
Transfer/sec:      1.03MB
```
Server Logs:
```
new call or cache expired! calling external apinew call or cache expired! calling external api
new call or cache expired! calling external api
new call or cache expired! calling external api

new call or cache expired! calling external apinew call or cache expired! calling external api
new call or cache expired! calling external api

new call or cache expired! calling external api
new call or cache expired! calling external api
new call or cache expired! calling external api
new call or cache expired! calling external apinew call or cache expired! calling external api

```
