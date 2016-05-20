#!/usr/bin/env python3

from flask import Flask

import pymongo
import os
import random
import datetime

app = Flask(__name__)

s="""
Hi {name}.</br>
This is your {count} visits.</br>
Your last visit is {time}</br>
"""

@app.route('/', defaults={'name':"Guest"})
@app.route('/<string:name>' , methods=['GET'])
def say_hello(name):
    conn = pymongo.MongoClient(os.getenv('OPENSHIFT_MONGODB_DB_HOST'),os.getenv('OPENSHIFT_MONGODB_DB_PORT'))
    #mongodb://$OPENSHIFT_MONGODB_DB_HOST:$OPENSHIFT_MONGODB_DB_PORT/
    #conn = pymongo.MongoClient("127.0.0.1",27017)
    db = conn.doco #连接库
    db.authenticate("admin","TmcJvzvXDup_")

    visitor = db.visitors.find_one({"name":name})
    if not visitor:
        db.visitors.insert_one({'name':name,"count":1,'time':datetime.datetime.now()})
        visitor = db.visitors.find_one({"name":name})
    else:
        db.visitors.update_one({'name':name}, {'$inc': {'count': 1},'$set':{'time':datetime.datetime.now()}})
        visitor["count"] = visitor["count"] +1

    return s.format(**visitor)

if __name__ == "__main__":
    app.run(debug=True)
