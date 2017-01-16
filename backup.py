#!/usr/bin/env python3
import requests
import json
from bson.objectid import ObjectId
import time
from multiprocessing.dummy import Pool


from db import db
from logger import Logger

l = Logger()
trace = l.trace
log = l.getlog()

limit = 10
api = 'http://www.dwsun.com.cn//api/record/{0}/'

apiLimit = api.format('?limit={0}'.format(limit))


def retrieve(idx):
    try:
        r = requests.get(api.format(idx), timeout=180)
        ret = r.json()
        weather = ret['payload']['data']
        idx = weather['_id']

        weather['_id'] = ObjectId(idx)

        db.weather.save(weather)
        r = requests.delete(api.format(idx), timeout=180)
    except requests.exceptions.ConnectionError as ex:
        log.error('failed with[{0}]'.format(ex))


def main():
    while True:
        r = requests.get(apiLimit, timeout=180)
        ret = r.json()
        weather = ret['payload']['data']
        count = ret['payload']['count']
        if count < 1000:
            log.debug('remote count[{0}], stop retrieve'.format(count))
            break
        pool = Pool()
        pool.map(retrieve, weather)
        pool.close()
        pool.join()

        lcount = db.weather.count()
        log.debug('remote count[{0}] local count[{1}]'.format(count, lcount))


if __name__ == '__main__':
    main()
