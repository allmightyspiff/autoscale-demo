#!/bin/python
import json
import configparser

import requests
from pprint import pprint as pp

config = configparser.ConfigParser()
config.read('./config.cfg')

url = 'http://10.77.184.131/nitro/v1/config/'
sl_url = 'https://api.service.softlayer.com/rest/v3/'

ip_address = requests.get("%sSoftLayer_Resource_Metadata/getPrimaryBackendIpAddress" % sl_url)
vpx_id = requests.get("%sSoftLayer_Resource_Metadata/getId" % sl_url)

new_serv = {
    "service" : {
        "name": "VPX-%s" % vpx_id.json(),
        "IP": ip_address.json(),
        "servicetype": "HTTP",
        "port": "80"
    }
}

serv_headers = {
    'Content-type': "%sservice+json" %  config.get('netscaler','Content-type'),
    'X-NITRO-USER': config.get('netscaler','X-NITRO-USER'),
    'X-NITRO-PASS': config.get('netscaler','X-NITRO-PASS')
}

pp(serv_headers)

result = requests.post("%sservice?action=add" % url, data = json.dumps(new_serv), headers=serv_headers)
#result = requests.delete("%sservice/%s" % (url,new_serv['service']['name']), headers=serv_headers)
print("STATUS: %s" % result.status_code)
if result.status_code == 201:
    print("SUCCESS")
else:
    print("FAILURE")
    pp(result.json())

