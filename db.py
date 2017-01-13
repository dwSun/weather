#!/usr/bin/env python3
import pymongo
import os
import json

try:
    conn = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_HOST'],
                               int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))
    db = conn.weather
    db.authenticate("admin", "16cFcmpKvWyl")
except KeyError:
    conn = pymongo.MongoClient("127.0.0.1", 27017)
    db = conn.weather

if __name__ == "__main__":
    print(db.weather.find_one())
