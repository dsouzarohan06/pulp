#!/bin/bash
#title           :master_sync.sh
#description     :This script will sync and publish all repos on the parent as well as the child node 
#author          :Rohan Dsouza
#usage           :bash master_sync.sh  OR ./master_sync.sh
#=========================================================================================================


> /opt/scripts/all_repos.txt

# <-- This is to make sure that if the session certificate has expired, it will be renewed

pulp-admin repo list > /dev/null	

if [ $? == 77 ];
then
	pulp-admin login -u admin -p admin
	pulp-admin repo list | grep ^Id | cut -d ":" -f2 >> /opt/scripts/all_repos.txt
else
	pulp-admin repo list | grep ^Id | cut -d ":" -f2 >> /opt/scripts/all_repos.txt
fi

# Ends here--> 

declare -a hosts=("pulp-slave-server.local")

# <-- Moving the files to all the slave nodes

for i in "${hosts[@]}"
do
	rsync -parv /opt/scripts/all_repos.txt root@"$i":/opt/scripts/ 
done

# Ends here -->


# <-- Sync and publish start here

for i in `pulp-admin repo list --details | grep -i feed | cut -d ":" -f3 | sed 's/^..//'`
do 	
	createrepo "$i"                       # To make sure that if new rpm's are added to any repo, they'll be available for sync.
done

echo -e "Syncing and Publishing all repos on the master \n";

for i in `pulp-admin repo list | grep -i id | cut -d ":" -f2`
do 
	pulp-admin rpm repo sync run --repo-id "$i"
	pulp-admin rpm repo publish run --repo-id "$i"
done

echo -e "Now, syncing and publishing all repos on the slave \n";

for i in "${hosts[@]}"
do
ssh root@"$i" /bin/bash << EOF
/opt/scripts/slave_sync.sh
EOF

if [ $? -ne 0 ];
then
	echo "`date "+%Y-%m-%d %H:%M:%S"` Sync and publish failed for host: $i" >> /var/log/pulp/sync.log  # Failed syncs will be logged here
fi
done  

# Ends here -->
