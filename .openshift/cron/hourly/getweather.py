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
url = "http://apis.baidu.com/heweather/weather/free"

headers = {
'apikey': "3f995bc3ef0da20226ca3766560eee11",
}

def getWeather(city):
    weather = None
    querystring = {"city":city}
    response = requests.request("GET", url, headers=headers, params=querystring)
    if(response.status_code == 200):
        weather=response.json()
    else:
        sys.exit(0)
    try:
        conn = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_HOST'],int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))
        db = conn.doco #连接库
        db.authenticate("admin","TmcJvzvXDup_")
    except KeyError:
        conn = pymongo.MongoClient("127.0.0.1",27017)
        db = conn.doco #连接库

    print(json.dumps(list(db.weather.find({},{'_id':0}))))

    db.weather.insert_one({'city':city,'weather':weather['HeWeather data service 3.0'][0],'time':now.strftime(timefmt),'utc':now.timestamp()})
    #db.weather.drop()

if __name__ == '__main__':
    citys = ['北京', '上海' , '广州','杭州']
    for city in citys:
        getWeather(city)
