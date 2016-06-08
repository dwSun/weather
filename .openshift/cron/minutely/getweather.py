#!/usr/bin/env python3
import pytz
import datetime
import pymongo
import os
import random
import requests
import urllib
import json
import sys

tz = pytz.timezone('Asia/Shanghai')
now = datetime.datetime.now(tz)

timefmt = "%Y-%m-%d %H:%M:%S"


weather = None
name = '北京'
r=requests.get("http://api.map.baidu.com/telematics/v3/weather?location={0}&output=json&ak=9393a3754af3170551a239fd7bfd7011".format(name))
if(r.status_code == 200):
    weather=json.loads(r.text)['results'][0]

if not weather:
    sys.exit(0)

try:
    conn = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_HOST'],int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))
    db = conn.doco #连接库
    db.authenticate("admin","TmcJvzvXDup_")
except KeyError:
    conn = pymongo.MongoClient("127.0.0.1",27017)
    db = conn.doco #连接库

#print(json.dumps(list(db.weather.find({},{'_id':0}))))

db.weather.insert_one({'weather':weather,'time':now.strftime(timefmt),'utc':now.timestamp()})
