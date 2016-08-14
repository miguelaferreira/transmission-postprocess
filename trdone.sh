#! /bin/bash

torrent="${TR_TORRENT_DIR}/${TR_TORRENT_NAME}"
destination=

logfile=$2

if [ -z ${logfile} ]; then
    echo "Logging to /var/log/trdone.log"
    logfile="/var/log/trdone.log"
fi

date >> ${logfile}

if [ -z ${destination} ]; then
  echo "Usage: trdone.sh <DESTINATION_DIRECTORY> [<LOG_FILE>]" >> ${logfile}
  echo "---------" >> ${logfile}
  exit 1
fi

if [ -z ${TR_TORRENT_DIR} ] || [ -z ${TR_TORRENT_NAME} ]; then
  echo "Transmission environment variables not set correctly." >> ${logfile}
  echo "Resulting torrent path is ${torrent}" >> ${logfile}
  echo "---------" >> ${logfile}
  exit 2
fi



echo "torrent=${torrent}" >> ${logfile}
  echo "destination=${destination}" >> ${logfile}
  UNRAR_LIB_PATH=/usr/lib/libunrar.so python -m trdone -t ${torrent} -d {destination} >> ${logfile}

echo "#########" >> ${logfile}
