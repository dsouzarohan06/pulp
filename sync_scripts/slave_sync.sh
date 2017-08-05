#!/bin/bash/
#title           :slave_sync.sh
#description     :This script will sync and publish all repos only on the child node 
#author          :Rohan Dsouza
#usage           :The master pulp server will be running this script via cron 
#=========================================================================================================


REPOS_FILE=/opt/scripts/all_repos.txt


# <-- This is to make sure that if the session certificate has expired, it will be renewed

pulp-admin repo list > /dev/null

if [ $? == 77 ];
then
        pulp-admin login -u admin -p admin
fi

# Ends here--> 


if [ $(diff "$REPOS_FILE" <(pulp-admin repo list | grep ^Id | cut -d ":" -f2) | wc -l) -ne 0 ]
	then
		if [ $(diff "$REPOS_FILE" <(pulp-admin repo list | grep ^Id | cut -d ":" -f2) | grep "<" | wc -l) -ne 0 ]
			then
			for i in `diff "$REPOS_FILE" <(pulp-admin repo list | grep ^Id | cut -d ":" -f2) | grep "<" | sed 's/<//'`
			do
			# Enter the IP / Name of the master server
			pulp-admin rpm repo create --repo-id "$i" --feed http://pulpserver.local/pulp/repos/"$i"/ --relative-url "$i"/ --serve-http true
			done
		else
			for i in `diff "$REPOS_FILE" <(pulp-admin repo list | grep ^Id | cut -d ":" -f2) | grep ">" | sed 's/>//'`
			do
			pulp-admin rpm repo delete --repo-id $i
			done
		fi
fi


for i in `pulp-admin repo list | grep -i id | cut -d ":" -f2`; do pulp-admin rpm repo sync run --repo-id "$i" ; pulp-admin rpm repo publish run --repo-id "$i"; done;

echo -e "Syncing and publishing on slave is done. \n";

