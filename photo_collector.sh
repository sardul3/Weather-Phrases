#!/bin/bash

# check whether I Drive is connected by looking for the photo directory
# If not, call link_idrive script

# "-d" tests whether a directory exists.
# "! -d" tests whether a directory does not exist.
if [ ! -d /mnt/idrive/photos ]; then
	echo "I Drive disconnected, trying to reconnect"
	/home/wx/callup_scripts/link_idrive
	#/mnt/idrive/link_idrive.sh
fi


# if I Drive is connected, run python script. Otherwise, abort
if [ -d /mnt/idrive/photos ]; then
	echo "I Drive successfully connected. Running photo script"
	# run the python script
	python3 /home/wx/photo_collector.py
else
	echo "I Drive failed to connect. Aborting script"
fi
