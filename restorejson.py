#!/usr/bin/env python3

import json
from bson.objectid import ObjectId
import os
import pymongo
from multiprocessing import Pool

from logger import Logger


l = Logger(__name__ + '.log')
trace = l.trace
log = l.getlog()


def _handle_json(f):
    conn = pymongo.MongoClient("192.168.2.198", 27017)
    db = conn.weather  # 连接库
    log.debug('handle [{0}]'.format(f))
    with open(f) as jsons:
        while True:
            try:
                rec = ''
                rec = jsons.readline()
                if not rec:
                    break

                weather = json.loads(rec)
                weather['_id'] = ObjectId(weather['_id'])

                db.log.save(weather)
            except Exception as ex:
                log.error('failed [{0}] with [{1}]'.format(rec, ex))

    log.debug('log count [{0}]'.format(db.log.count()))
    log.debug('remove [{0}]'.format(f))
    os.remove(f)


def handle_json(f):
    try:
        _handle_json(f)
    except Exception as ex:
        log.error('failed [{0}] with [{1}]'.format(f, ex))


def main():
    jsons = []

    for r, d, fs in os.walk('./jsons'):
        for f in fs:
            f = os.path.join(r, f)
            if f.endswith('.json'):
                jsons.append(f)
                # handle_json(f)
            else:
                log.debug('skip [{0}]'.format(f))

    p = Pool(8)
    p.map(handle_json, jsons)
    p.close()
    p.join()


if __name__ == '__main__':
    main()
