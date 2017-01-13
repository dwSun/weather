#!/usr/bin/env python3
from flask import Blueprint
from flask.ext.restful import Api, Resource
from bson.objectid import ObjectId

from logger import Logger
from db import db

l = Logger()
trace = l.trace
log = l.getlog()

app = Blueprint("record", __name__)

api = Api()

@app.record_once
def on_load(state):
    api.init_app(app)


class Record(Resource):
    @trace(__name__)
    def get(self, idx=None):
        if idx:
            log.debug('getting [{0}]'.format(idx))
            rc = db.weather.find_one({"_id": ObjectId(idx)})
        else:
            rc = db.weather.find_one()

        rc['_id'] = str(rc['_id'])
        return rc

    @trace(__name__)
    def delete(self, idx=None):
        log.debug('deleteing [{0}]'.format(idx))
        db.weather.delete_one({"_id": ObjectId(idx)})
        return {}


api.add_resource(Record,
                 '/record/',
                 '/record/<string:idx>/',
                 endpoint='record')
