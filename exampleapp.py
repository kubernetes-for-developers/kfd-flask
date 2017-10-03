#!/usr/bin/env python3

import os
from configparser import SafeConfigParser
from pathlib import Path

from flask import Flask
from flask import render_template

parser = SafeConfigParser(os.environ)
config_file = Path(os.environ.get('CONFIG_FILE','/opt/feature.flags'))

if config_file.is_file():
    parser.read(os.environ.get('CONFIG_FILE'))

app = Flask(__name__)

@app.route('/')
def index():
    return "Index Page"

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html',
            greeting=parser.get('features','greeting',fallback="Howdy"),
            name=name)

if __name__ == '__main__':
    debug_enable = parser.getboolean('feaxtures','debug',fallback=False)
    app.run(debug=debug_enable,host='0.0.0.0')
