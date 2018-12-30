#!/usr/bin/python


print "Content-type: text/html\r\n\r\n"


from M2Crypto import httpslib
import base64
import simplejson
import cgi
import commands
import string
import random
import os


# Set the basic info
username = '<%= scope['pulp::server::default_login'] %>'
password = '<%= scope['pulp::server::default_password'] %>'
hostname = '<%= scope['pulp::admin::pulp_server'] %>'
port = 443

# Create the auth header
raw = ':'.join((username, password))
#encoded = base64.encodedstring(raw)[:-1]
encoded = base64.encodestring(raw)[:-1]
headers = {}
headers['Authorization'] = 'Basic ' + encoded

# We'll need this later on
body = None # Fill in with a dict for a POST

#Make the connection, and get some info
connection = httpslib.HTTPSConnection(hostname, port)

htmlHead = """
<html><head>
<title>Pulp::Directi - <--title--> </title>
<meta http-equiv="refresh" content="<--refresh-->">
<script language=Javascript>
        function takeaction(id,lpath,local){
                document.location.href = '?action=sync&id=' + id +'&lpath=' + lpath + '&local=' + local
        }
        function deleterepo(id){
                var ans = confirm("Are you sure ?")
                if (ans){
                        document.location.href = '?action=delete&id=' + id
                }
        }
        function syncrepo(id,file){
                alert("OK")
        }
</script>
<style>
a{text-decoration:none;}
.home {background-color: black; padding: 10px 20px 10px 20px; margin:0 auto;}
.home a{ text-decoration : none; color: white; size:14px}
.home a:hover{color: red}

tr.head { text-align:center}
tr.even {background-color:#EEEEEE;}
tr:hover{background-color:#999999}

</style>
        
</head>
<body>
<div class=home><a href=https://pulp-austin.india.endurance.com/index.py>HOME </a>- - <a taregt=_blank href=https://pulp-austin.india.endurance.com/upload.py?f=/rpms> NEW</a></div>
"""

htmlRedirect = """
<html><head>
<meta http-equiv="Refresh" content="0; url=/index.py?action=status&file=<--file-->&id=<--id-->&lpath=<--lpath-->" />
</head>
"""

def Conn(url, method='GET'):
        connection.request(method, url, body=body, headers=headers)
        response = connection.getresponse()
        return simplejson.loads(response.read())


def rand_gen(chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(10))



arguments = cgi.FieldStorage()

if arguments.has_key('getinfo'):
        getinfo = arguments['getinfo'].value
        response_str = Conn('/pulp/api/v2/repositories/'+getinfo+'/importers/')
        url = response_str["config"]["feed"]
        url = url.replace("file:///mnt","")
        print simplejson.dumps({'lpath': url})
        exit(1)

if arguments.has_key('action'):
        action = arguments['action'].value
        if arguments.has_key('id'):
                id = arguments['id'].value

        if action == 'new':
                print htmlHead.replace("<--title-->","New Repo")

        elif action == 'sync':
                response_str = Conn('/pulp/api/v2/repositories/')
		lpath = arguments['lpath'].value
                file = rand_gen()
                commands.getoutput("echo \"Starting Sync for repo <b>"+id+"</b>. The page will auto refresh every 5 secs. \" > /mnt/tmp/"+file )
                commands.getoutput("echo \"/opt/scripts/sync.py "+id+" "+lpath+" \" >> /mnt/tmp/"+file )
                os.system("/opt/scripts/sync.py "+id+" "+lpath+" >> /mnt/tmp/"+file+" &")
                         
                htmlRedirect = htmlRedirect.replace("<--file-->",file)
                htmlRedirect = htmlRedirect.replace("<--lpath-->",lpath)
                print htmlRedirect.replace("<--id-->",id)


        elif action == 'status':
                file = arguments['file'].value
                htmlHead = htmlHead.replace("<--title-->","Sync::Status::"+id)
                print htmlHead.replace("<--refresh-->","5")
                f=open("/mnt/tmp/"+file, 'r')
                print "<pre>"
                print f.read()
                f.close()

        elif action == 'delete':
                print htmlHead.replace("<--title-->","Delete::"+id )
                response_str = Conn('/pulp/api/v2/repositories/'+id+'/', 'DELETE')
                if response_str['scheduled_time']:
                        print "Repo " + id + " is due for deletion as of " + response_str['scheduled_time']
                else:
                        print "Repo does not exist"
        else:
                print "Nothing to see here. Go <a href=https://pulp-austin.india.endurance.com/index.py>HOME</a>"


else:
        response_str = Conn('/pulp/api/v2/repositories/')
        html = htmlHead.replace("<--title-->","Repositories")
        print html
	#print simplejson.dumps(response_str)
        print "<table align=center>"
        print "<tr class=head><td>ID</td><td>Packages</td><td>Source</td><td>Last Sync</td><td></td></tr>"
        count = 0
        for repo in response_str:
                #rpath = repo['source']['url'].replace('file:///mnt','')
		repo_info = Conn('/pulp/api/v2/repositories/'+ repo['id'] +'/importers/')
                rpath = repo['id'].replace(repo['id'],'/pulp/repos/'+repo['id']+'/')
                lpath = repo_info[0]['config']['feed'].replace('file:///mnt','')
                if count % 2 == 0:
                        print "<tr class=even>"
                else:
                        print "<tr>"
                print "<td><a target=_blank href="+rpath+">"+ repo['id'] + "</a></td>"
		if repo['content_unit_counts']:
                	print "<td>"+ str(repo['content_unit_counts']['rpm']) + "</td>"
		else:
                	print "<td>0</td>"
                if repo['id'] == 'local':
                        print "<td><a href=https://pulp-austin.india.endurance.com/upload.py?f="+repo['config']['feed'].replace('file:///mnt','')+">"+ repo['config']['feed'] + "</a></td>"
                        print "<td>"+ str(repo['last_sync']) + "</td><td><input type=button value='sync now' onclick=takeaction(\""+repo['id']+"\",\""+lpath+"\",\"yes\")></td>"
#                       print "<input type=button value='delete' onClick=\"deleterepo('"+repo['id']+"')\"</td>"
                else:
                        print "<td><a target=_blank href=https://pulp-austin.india.endurance.com/upload.py?f="+lpath+">"+ repo_info[0]['config']['feed'] + "</a></td>"
                        print "<td>"+ str(repo_info[0]['last_sync']) + "</td>"
			print "<td><input type=button value='sync now' onclick=takeaction(\""+repo['id']+"\",\""+lpath +"\",\"yes\")></td>"
#                       print "<input type=button value='delete' onClick=\"deleterepo('"+repo['id']+"')\"</td>"
                print "</tr>"
                count=count+1
