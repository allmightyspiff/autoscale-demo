import json
import requests
from pprint import pprint as pp

#headers = {'Content-type': 'application/x-www-form-urlencoded'}
headers = {
    'Content-type': 'application/vnd.com.citrix.netscaler.lbvserver+json',
    'X-NITRO-USER': 'root',
    'X-NITRO-PASS':'Mbs3SvgD'
    }
user = 'root'
password = 'Mbs4SvgD'

url = 'http://10.77.184.131/nitro/v1/config/'

#session = requests.Session()
#session.auth = (user, password)
#session.headers.update(headers)

response = requests.get(url, headers = headers)
#pp(response.headers)
data = response.json()
print("LBS")
#pp(data)


lbvserver = requests.get("%slbvserver" % url, headers=headers)
#print("LBVSERVER")
#pp(lbvserver.headers)
lb = lbvserver.json()
for thing in lb['lbvserver']:
    print("%s:%s - %s" % ( thing['ipv46'], thing['port'], thing['name']))
    details = requests.get("%slbvserver_binding/%s" % (url,thing['name']),headers=headers)
    bindings = details.json()
    # Assuming only 1 service in a binding...
    for bound in bindings['lbvserver_binding'][0]['lbvserver_service_binding']:
        print("\t%s:%s - %s (%s)" % (bound['ipv46'],bound['port'],bound['servicename'], bound['curstate']))
    #pp(details.json())

print("SERVICES")
service = requests.get("%sservice" % url, headers=headers).json()
for serv in service['service']:
    print("%s:%s - %s (%s)" % (serv['ipaddress'],serv['port'],serv['name'], serv['svrstate']))
#pp(service)



new_serv = {
    "service" : {
        "name": "test-vpx-xxx",
        "IP": "10.77.184.135",
        "servicetype": "HTTP",
        "port": "80"
    }
}

serv_headers = {
    'Content-type': 'application/vnd.com.citrix.netscaler.service+json',
    'X-NITRO-USER': 'root',
    'X-NITRO-PASS':'Mbs3SvgD'
}
#result = requests.post("%sservice?action=add" % url, data = json.dumps(new_serv), headers=serv_headers)
#result = requests.delete("%sservice/%s" % (url,new_serv['service']['name']), headers=serv_headers)
#print("STATUS: %s - RESULT HEADERS" % result.status_code)
#pp(result.headers)
#print("RESULT DATA")
#pp(result.json())

