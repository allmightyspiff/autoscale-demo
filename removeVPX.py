#!/bin/python
import json
import configparser
import SoftLayer

import requests
from pprint import pprint as pp

config = configparser.ConfigParser()
config.read('./config.cfg')

url = 'http://10.77.184.131/nitro/v1/config/'
sl_url = 'https://api.service.softlayer.com/rest/v3/'

#ip_address = requests.get("%sSoftLayer_Resource_Metadata/getPrimaryBackendIpAddress" % sl_url)
#vpx_id = requests.get("%sSoftLayer_Resource_Metadata/getId" % sl_url)

sl_client = SoftLayer.Client()
mask = "mask[id,fullyQualifiedDomainName,primaryBackendIpAddress, hostname]"
object_filter = { 
    'virtualGuests' : {
        'hostname' : {
            'operation': 'vpx-node'
        }
    }
}

guests = sl_client['SoftLayer_Account'].getVirtualGuests(mask=mask,filter=object_filter)


serv_headers = {
    'Content-type': "%sservice+json" %  config.get('netscaler','Content-type'),
    'X-NITRO-USER': config.get('netscaler','X-NITRO-USER'),
    'X-NITRO-PASS': config.get('netscaler','X-NITRO-PASS')
}

for virt in guests:
    print("%s - %s - %s" % (virt['fullyQualifiedDomainName'], virt['id'], virt['primaryBackendIpAddress']))
    result = requests.delete("%sservice/vpx-%s" % (url,virt['id']), headers=serv_headers)
    print("STATUS: %s" % result.status_code)
    if result.status_code == 201 :
        print("\t Removed from netscaler")
    else:
        output = result.json()
        print("%s" % output['message'])
    print("Canceling GUEST")
    sl_client['SoftLayer_Virtual_Guest'].deleteObject(id=virt['id'])
    

