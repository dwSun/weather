#!/usr/bin/env python3
import pymongo
import random
import datetime

#conn = pymongo.MongoClient("127.0.0.1",27017)
conn = pymongo.MongoClient("192.168.1.35",27017)
db = conn.logs #连接库
#db.authenticate("tage","123")
#用户认证
#db.user.drop()
#删除集合user
db.log.save({'id':db.log.find().count(),'time':datetime.datetime.now().timestamp()})
#content = db.log.find()
content = db.ls.find_one()
print(content)

#打印所有数据
#for i in content:
#    print (i)
