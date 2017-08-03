#!/bin/bash
#title           :slave_sync.sh
#description     :This script will sync and publish all repos only on the child node 
#author          :Rohan Dsouza
#usage           :The master pulp server will be running this script via cron 
#=========================================================================================================


echo -e "Now, syncing and publishing all repos on the slave \n";

for i in `pulp-admin repo list | grep -i id | cut -d ":" -f2`; do pulp-admin rpm repo sync run --repo-id "$i" ; pulp-admin rpm repo publish run --repo-id "$i"; done;

echo -e "Syncing and publishing on slave is done. \n";

