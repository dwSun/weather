import sys, urllib,json


with open(r'd:\wetWorld.json',encoding='utf8') as inf:
    content = inf.read()
    data = json.loads(content)
    provs = dict()
    for city in data['city_info']:
        if city['cnty'] not in provs:
            provs[city['cnty']] = list()
        provs[city['cnty']].append(city)
    print("proviences: [%d]"%(len(provs)))
    for prov in provs.keys():
        print('[%s]\t\t[%d]'%(prov,len(provs[prov])))
