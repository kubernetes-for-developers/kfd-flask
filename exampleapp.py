#!/usr/bin/env python3

import os
from configparser import SafeConfigParser
from pathlib import Path

from flask import Flask
from flask import render_template
import redis

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

if __name__ == '__main__':
    debug_enable = parser.getboolean('features', 'debug', fallback=False)
    redis_host = parser.get('features', 'db', fallback="redis")
    redis_store = redis.StrictRedis(host=redis_host, port=6379, db=0)
    app.run(debug=debug_enable, host='0.0.0.0')
