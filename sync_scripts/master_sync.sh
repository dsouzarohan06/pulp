#!/bin/bash
#title           :master_sync.sh
#description     :This script will sync and publish all repos on the parent as well as the child node 
#author          :Rohan Dsouza
#usage           :bash master_sync.sh  OR ./master_sync.sh
#=========================================================================================================


echo -e "Syncing and Publishing all repos on the master \n";

for i in `pulp-admin repo list | grep -i id | cut -d ":" -f2`; do pulp-admin rpm repo sync run --repo-id "$i" ; pulp-admin rpm repo publish run --repo-id "$i"; done;

echo -e "Now, syncing and publishing all repos on the slave \n";

ssh pulp-slave.tel-uk.colo /bin/bash <<EOF

/opt/scripts/slave_sync.sh

EOF
