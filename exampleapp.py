#!/usr/bin/env python3

import os
import time

from configparser import SafeConfigParser
from pathlib import Path

from flask import Flask
from flask import render_template, make_response, request

from jaeger_client import Config
from flask_opentracing import FlaskTracer

from prometheus_client import Summary, Counter, Histogram
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

import requests
import redis
import signal
import sys

FLASK_REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Flask Request Latency',
				['method', 'endpoint'])
FLASK_REQUEST_COUNT = Counter('flask_request_count', 'Flask Request Count',
				['method', 'endpoint', 'http_status'])

# defaults to reporting via UDP, port 6831, to localhost
def initialize_tracer():
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1
            },
            'logging': True
        },
        service_name='flask-service'
    )
    return config.initialize_tracer() # also sets opentracing.tracer

def before_request():
    request.start_time = time.time()

def after_request(response):
    request_latency = time.time() - request.start_time
    FLASK_REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
    FLASK_REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

def sigterm_handler(_signo, _stack_frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

# initialize the configuration parser with all the existing environment variables
parser = SafeConfigParser(os.environ)
# default location of ./feature.flags is used if the environment variable isn’t set
config_file = Path(os.environ.get('CONFIG_FILE', './feature.flags'))
# verify file exists before attempting to read and extend the configuration
if config_file.is_file():
    parser.read(os.environ.get('CONFIG_FILE'))

redis_store = None
app = Flask(__name__)

@app.route('/')
def index():
    return "Index Page"

@app.route('/activeconfig')
def activeconfig():
    output = ""
    for each_section in parser.sections():
        output += "SECTION: "+each_section+"\n"
        for (each_key, each_val) in parser.items(each_section):
            output += each_key+" : "+each_val+"\n"
    return output

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html',
                           greeting=parser.get('features', 'greeting', fallback="Howdy"),
                           name=name)

@app.route('/alive')
def alive():
    return "Yes"

@app.route('/ready')
def ready():
    if redis_store.ping():
        return "Yes"
    else:
        flask.abort(500)

@app.route('/metrics')
def metrics():
    return make_response(generate_latest())

@app.route('/remote')
def pull_requests():
    github_url = "https://api.github.com/repos/opentracing/opentracing-python/pulls"
    r = requests.get(github_url)
    json = r.json()
    pull_request_titles = map(lambda item: item['title'], json)
    return 'PRs: ' + ', '.join(pull_request_titles)

if __name__ == '__main__':
    debug_enable = parser.getboolean('features', 'debug', fallback=False)
    redis_host = parser.get('features', 'db', fallback="localhost")
    redis_store = redis.StrictRedis(host=redis_host, port=6379, db=0)
    app.before_request(before_request)
    app.after_request(after_request)
    flask_tracer = FlaskTracer(initialize_tracer, True, app)
    app.run(debug=debug_enable, host='0.0.0.0')
