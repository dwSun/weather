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
citys = ['CN101010100', 'CN101020100', 'CN101030100', 'CN101040100', 'CN101050101', 'CN101060101', 'CN101060201', 'CN101070101', 'CN101070201', 'CN101080101', 'CN101090101', 'CN101090501', 'CN101180101', 'CN101180901', 'CN101100101', 'CN101120101', 'CN101120201', 'CN101120301', 'CN101120501', 'CN101120601', 'CN101120901', 'CN101121301', 'CN101190101', 'CN101190201', 'CN101190401', 'CN101190501', 'CN101190601', 'CN101190701', 'CN101190801', 'CN101190901', 'CN101191101', 'CN101210101', 'CN101210201', 'CN101210301', 'CN101210401', 'CN101210501', 'CN101210701', 'CN101210901', 'CN101230101', 'CN101230201', 'CN101230501', 'CN101240101', 'CN101220101', 'CN101220301', 'CN101200101', 'CN101200201', 'CN101200901', 'CN101250101', 'CN101280101', 'CN101280701', 'CN101280800', 'CN101281601', 'CN101281701', 'CN101300101', 'CN101310101', 'CN101260101', 'CN101290101', 'CN101270101', 'CN101270401', 'CN101170101', 'CN101160101', 'CN101150101', 'CN101130101']

def getWeather(city):
    weather = None
    querystring = {"cityid":city}
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
    for city in citys:
        getWeather(city)