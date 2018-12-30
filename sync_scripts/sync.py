#!/usr/bin/python

from M2Crypto import httpslib
from M2Crypto import SSL
SSL.Connection.clientPostConnectionCheck = None
import base64
import simplejson
import cgi
import random
import string
import sys
import datetime
import os


now = datetime.datetime.now()

username = '<%= scope['pulp::server::default_login'] %>'
password = '<%= scope['pulp::server::default_password'] %>'
port = 443

id = sys.argv[1]
lpath = sys.argv[2]
#chksum = sys.argv[3]

body = None
raw = ':'.join((username, password))
encoded = base64.encodestring(raw)[:-1]
headers = {}
headers['Authorization'] = 'Basic ' + encoded


#hosts = ["pulp.aus-tx.colo", "pulp.tx1-tx.colo", "pulp.gpx-mum.colo", "pulp-vsnl.directi.com", "pulp.tel-uk.colo", "pulp.tel-hk.colo", "pulp.sdh-tr.colo"]
#hosts = ["pulp.tx1-tx.colo", "pulp.gpx-mum.colo", "pulp-vsnl.directi.com", "pulp.tel-uk.colo", "pulp.tel-hk.colo", "pulp.sdh-tr.colo"]
hosts = ["pulp-1.aus-tx.colo", "pulp-1.gpx-mum.colo", "pulp-1.tel-hk.colo", "pulp-2.aus-tx.colo" , "pulp-2.gpx-mum.colo" , "pulp-2.tel-hk.colo", "pulp-3.tel-uk.colo", "pulp-4.tel-uk.colo"]

def Conn(url, hostname, method='GET'):
        connection = httpslib.HTTPSConnection(hostname, port)
        connection.request(method, url, body=body, headers=headers)
        response = connection.getresponse()
        #return simplejson.loads(response.read())
        return response.read()

def rand_gen(chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(10))

print  "Sync status on all servers as of " + now.strftime("%Y-%m-%d %H:%M") + "\n\n\n"

print os.system("/usr/bin/createrepo  /mnt"+lpath)


for hostname in hosts:
	print "\n"
	print "Now Syncing on server => " + hostname +" for repo " + id
	url = "/pulp/api/v2/repositories/"+id+"/actions/sync/"
	Conn(url,hostname,'POST')
	print "Sync began on " + hostname
	print "\n"

