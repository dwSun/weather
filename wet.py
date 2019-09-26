import sys
import urllib
import json
from urllib import request

cityURL = 'https://api.heweather.com/x3/citylist?search=allchina&key=+======================'


url = 'https://api.heweather.com/x3/weather?cityid=CN101010100&key================='
worldURL = 'https://api.heweather.com/x3/citylist?search=hotworld&key======================'
resp = request.urlopen(worldURL)
content = resp.read()

with open(r'd:\wetWorld.json', 'wb') as of:
    of.write(content)

if(content):
    data = json.loads(content.decode())
