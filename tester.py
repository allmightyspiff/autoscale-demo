#!/bin/python
import json
import configparser

import requests
from pprint import pprint as pp

config = configparser.ConfigParser()
config.read('./config.cfg')

headers = {
    'Content-type': "%slbvserver+json" %  config.get('netscaler','Content-type'),
    'X-NITRO-USER': config.get('netscaler','X-NITRO-USER'),
    'X-NITRO-PASS': config.get('netscaler','X-NITRO-PASS')
}

url = 'http://10.77.184.131/nitro/v1/config/'
response = requests.get(url, headers = headers)
data = response.json()
print("LBS")

lbvserver = requests.get("%slbvserver" % url, headers=headers)

lb = lbvserver.json()
for thing in lb['lbvserver']:
    print("%s:%s - %s" % ( thing['ipv46'], thing['port'], thing['name']))
    details = requests.get("%slbvserver_binding/%s" % (url,thing['name']),headers=headers)
    bindings = details.json()
    # Assuming only 1 service in a binding...
    for bound in bindings['lbvserver_binding'][0]['lbvserver_service_binding']:
        print("\t%s:%s - %s (%s)" % (bound['ipv46'],bound['port'],bound['servicename'], bound['curstate']))


print("SERVICES")
service = requests.get("%sservice" % url, headers=headers).json()
for serv in service['service']:
    print("%s:%s - %s (%s)" % (serv['ipaddress'],serv['port'],serv['name'], serv['svrstate']))


