#!/usr/bin/env python3
from flask import Flask, render_template
import datetime
import requests
import json

from db import db
from record import app as record
from logger import Logger

l = Logger()
trace = l.trace
log = l.getlog()

app = Flask(__name__)


@app.template_global()
def debug():
    return app.debug


@app.route('/weather/', defaults={'name':"北京"})
@app.route('/weather/<string:name>' , methods=['GET'])
def weather(name):
    log.debug('[{0}] weather fetch...'.format(name))
    r = requests.get("http://api.map.baidu.com/telematics/v3/weather?location={0}&output=json&ak=9393a3754af3170551a239fd7bfd7011".format(name))
    if(r.status_code == 200):
        return render_template("weather.html",
                               data=json.loads(r.text)['results'][0])
    else:
        return render_template("weather.html", data=None)

s = """
Hi {name}.</br>
This is your {count} visits.</br>
Your last visit is {time}</br>
"""


@app.route('/', defaults={'name': "Guest"})
@app.route('/<string:name>', methods=['GET'])
def say_hello(name):
    log.debug('[{0}] visits...'.format(name))

    visitor = db.visitors.find_one({"name": name})
    if not visitor:
        db.visitors.insert_one({'name': name,
                                "count": 1,
                                'time': datetime.datetime.now()})
        visitor = db.visitors.find_one({"name": name})
    else:
        db.visitors.update_one({'name': name},
                               {'$inc': {'count': 1},
                                '$set': {'time': datetime.datetime.now()}})
        visitor["count"] = visitor["count"] + 1
    return s.format(**visitor)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


app.register_blueprint(record, url_prefix='/api')

if __name__ == "__main__":
    #app.run()
    app.run(debug=True)
