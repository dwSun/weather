#!/usr/bin/env python3
from flask import Blueprint
from flask import request
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
            rc['_id'] = str(rc['_id'])
        else:
            limit = 100
            if request.args.get('limit'):
                limit = int(request.args.get('limit').strip('/'))
            rcs = db.weather.find({}, {"_id": 1}).limit(limit)
            rc = []
            for r in rcs:
                rc.append(str(r['_id']))

        return {'code': 0,
                'msg': '',
                'payload': {
                    'data': rc,
                    'count': db.weather.count()}
                }

    @trace(__name__)
    def delete(self, idx=None):
        log.debug('deleteing [{0}]'.format(idx))
        db.weather.delete_one({"_id": ObjectId(idx)})
        return {'code': 0,
                'msg': '',
                'payload': {}
                }


api.add_resource(Record,
                 '/record/',
                 '/record/<string:idx>/',
                 endpoint='record')
