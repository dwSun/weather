#!/usr/bin/env python3

import json
from bson.objectid import ObjectId
import time

from db import db
from logger import Logger

l = Logger('backup.log', log_f=True)
trace = l.trace
log = l.getlog()


def main():
    with open('weather.json') as wet:
        
        for rec in wet:
            weather = json.loads(rec)
            weather['_id'] = ObjectId(weather['_id']['$oid'])
            
            db.weather.save(weather)
            print('saved [{0}]'.format(weather['_id']))


if __name__ == '__main__':
    main()
