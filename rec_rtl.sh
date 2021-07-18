#!/bin/bash

if [ $# -le 3 ]; then
    echo "usage: rec_rtl <freq> <time_min> <dir> <title> [email]" 
    echo " e.g.: rec_rtl 80.0 30 /srv/rec test"
    exit 1
fi

FREQ="${1}M"
TIME=$((${2}*60))
DIR=${3}
TITLE=${4}
EMAIL=${5}
DATE=`date '+%Y-%m-%d-%H%M'`
FILENAME=${TITLE}_${DATE}.m4a
FILE=${DIR}/${FILENAME}

echo "freq: ${FREQ}"
echo "time: ${TIME}"
echo "dir: ${DIR}"
echo "title: ${TITLE}"
echo "date: ${DATE}"
echo "filename: ${FILENAME}"
echo "file: ${FILE}"
echo "email: ${EMAIL}"

rtl_fm -f ${FREQ} -M wbfm -s 256k -r 32k -g 20 -F 9 - | ffmpeg -ar 32k -f s16le -t ${TIME} -filter_complex lowpass=f=8000 -i - "${FILE}"
if [ $# -le 4 ]; then
    send_file ${DIR} ${FILENAME} ${EMAIL}
fi
