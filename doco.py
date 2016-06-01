#!/usr/bin/env python3

from flask import Flask, render_template

import pymongo
import os
import random
import datetime
import requests
import urllib
import json
from flask_cdn import CDN

app = Flask(__name__)

app.config['CDN_DOMAIN'] = 'cdnjs.cloudflare.com/ajax'
#app.config['CDN_HTTPS'] = True
app.config['CDN_ENDPOINTS'] = 'libs'

CDN(app)

@app.route('/weather', defaults={'name':"北京"})
@app.route('/weather/<string:name>' , methods=['GET'])
def weather(name):
    r=requests.get("http://api.map.baidu.com/telematics/v3/weather?location={0}&output=json&ak=9393a3754af3170551a239fd7bfd7011".format(name))
    if(r.status_code == 200):
        return render_template("weather.html",data=json.loads(r.text)['results'][0])
    else:
        return render_template("weather.html",data=None)

s="""
Hi {name}.</br>
This is your {count} visits.</br>
Your last visit is {time}</br>
"""

@app.route('/', defaults={'name':"Guest"})
@app.route('/<string:name>' , methods=['GET'])
def say_hello(name):
    try:
        conn = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_HOST'],int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))
        db = conn.doco #连接库
        db.authenticate("admin","TmcJvzvXDup_")
    except KeyError:
        conn = pymongo.MongoClient("127.0.0.1",27017)
        db = conn.doco #连接库

    visitor = db.visitors.find_one({"name":name})
    if not visitor:
        db.visitors.insert_one({'name':name,"count":1,'time':datetime.datetime.now()})
        visitor = db.visitors.find_one({"name":name})
    else:
        db.visitors.update_one({'name':name}, {'$inc': {'count': 1},'$set':{'time':datetime.datetime.now()}})
        visitor["count"] = visitor["count"] +1
    return s.format(**visitor)

if __name__ == "__main__":
    app.run()
    #app.run(debug=True)
