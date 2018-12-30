#!/usr/bin/env python

import yaml
import os
import socket
import fileinput
import fcntl

# To make sure only one instance of this script runs.
pid_file = ("/var/run/sync-script.pid")
fp = open(pid_file,'w')

try:
  fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
  print "Already an instance of this script is in memory. Hence, exiting."
  exit(1)

fyaml = '/etc/pulp/pulp.yaml'
frepo = '/etc/pulp/repo.list'

f = open(fyaml)

dataMap = yaml.safe_load(f)

f.close

if socket.gethostname() in ('pulp-1.aus-tx.colo','pulp-2.aus-tx.colo'):
        master = 'true'
else:
        master = 'false'

# Deleting Orphan RPM's
os.system("/usr/bin/curl -X DELETE -k -u '<%= scope['pulp::server::default_login'] %>:<%= scope['pulp::server::default_password'] %>' https://localhost/pulp/api/v2/content/orphans/")
# Making sure that the cert does not expire
os.system("/usr/bin/pulp-admin login -u <%= scope['pulp::server::default_login'] %> -p <%= scope['pulp::server::default_password'] %>")
#get present repos
os.system("/usr/bin/pulp-admin repo list | grep ^Id | awk {'print $2'}>" + frepo)


for repo in dataMap['repos']:
        f1 = open(frepo)
        if repo in f1.read():
                print "Repo " + repo + " found. Nothing to do."
		if dataMap['repos'][repo]['type'] == 'remote':
			os.system("/usr/bin/pulp-admin rpm repo sync run --repo-id "+repo)
			os.system("/usr/bin/pulp-admin rpm repo publish run --repo-id "+repo)
		if dataMap['repos'][repo]['type'] == 'local':
			os.system("/usr/bin/createrepo "+" /mnt/rpms/"+str(dataMap['repos'][repo]['source']))
			os.system("/usr/bin/pulp-admin rpm repo sync run --repo-id "+repo)
			os.system("/usr/bin/pulp-admin rpm repo publish run --repo-id "+repo)
        else:
                print "Repo " + repo + " Not found"
                if dataMap['repos'][repo]['type'] == 'remote':
                        os.system("/usr/bin/pulp-admin rpm repo create --repo-id " + repo + " --feed "+ str(dataMap['repos'][repo]['source']) + " --relative-url " + repo + " --remove-missing true")
                        os.system("/usr/bin/pulp-admin rpm repo sync run --repo-id "+repo)
                        os.system("/usr/bin/pulp-admin rpm repo publish run --repo-id "+repo)
                if dataMap['repos'][repo]['type'] == 'local':
                        if master == 'false':
                                os.system("/usr/bin/pulp-admin rpm repo create --repo-id " + repo + " --feed https://pulp-austin.india.endurance.com/pulp/repos/"+ repo +"/" + " --relative-url "+ repo + " --verify-feed-ssl false" + " --remove-missing true")
                                os.system("/usr/bin/pulp-admin rpm repo sync run --repo-id "+repo)
                                os.system("/usr/bin/pulp-admin rpm repo publish run --repo-id "+repo)
                        if master == 'true':
                                if 'chksum' in dataMap['repos'][repo]:
                                        os.system("/usr/bin/createrepo "+" /mnt/rpms/"+str(dataMap['repos'][repo]['source']))
                                        os.system("/usr/bin/pulp-admin rpm repo create --repo-id " + repo + " --feed file:///mnt/rpms/"+str(dataMap['repos'][repo]['source']) + " --relative-url " + repo + " --remove-missing true" )
                                        os.system("/usr/bin/pulp-admin rpm repo sync run --repo-id "+repo)
                                        os.system("/usr/bin/pulp-admin rpm repo publish run --repo-id "+repo)
                                else:
                                        os.system("/usr/bin/createrepo "+" /mnt/rpms/"+str(dataMap['repos'][repo]['source']))
                                        os.system("/usr/bin/pulp-admin rpm repo create --repo-id " + repo + " --feed file:///mnt/rpms/"+str(dataMap['repos'][repo]['source']) + " --relative-url "+ repo + " --remove-missing true")
                                        os.system("/usr/bin/pulp-admin rpm repo sync run --repo-id "+repo)
                                        os.system("/usr/bin/pulp-admin rpm repo publish run --repo-id "+repo)
        f1.close


#Cleaning the repo.list file
for repo in dataMap['repos']:
        for line in fileinput.input(frepo,inplace =1):
                line = line.strip()
                if not repo in line:
                        print line



#Delete repos not in puppet
for repo in open(frepo):
        repo = repo.rstrip()
        print "Repo "+repo+" not in puppet "
        os.system("/usr/bin/pulp-admin rpm repo delete --repo-id "+repo)



