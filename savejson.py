#!/usr/bin/env python3
import datetime
import json
import os

import pymongo

from logger import Logger

conn = pymongo.MongoClient("127.0.0.1", 27017)
db = conn.weather  # 连接库

l = Logger('savejson.log')
trace = l.trace
ll = l.getlog()


def main():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           str(datetime.datetime.now()) + '.json'), 'w') as ojson:
        while db.weather.count() > 2000:
            ll.debug('db count[{0}]'.format(db.weather.count()))
            ids = []
            for log in db.weather.find().limit(1000):
                idx = log['_id']
                ids.append(idx)
                log['_id'] = str(idx)
                ojson.write(json.dumps(log))
                ojson.write('\n')

            for idx in ids:
                db.weather.delete_one({"_id": idx})


if __name__ == '__main__':
    main()

