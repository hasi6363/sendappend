#!/bin/bash

usage_exit() {
  echo "usage: ${0} -t <type> -s <station_id> -d <minute> -o <output_dir> -n <name_suffix> [-i address] [-p password] [-m mail]"
  echo " e.g.: ${0} -t radiko -s FMT -d 30 -m aaa@bbb.ccc -n TEST -o /srv/radiko"
  echo "       then recoded file is /srv/radiko/TEST_YYYY-mm-dd-HHMM.m4a"
  exit 1
}

ID=""
PASSWORD=""
EMAIL=""
OUTDIR=""
SUFFIX=""

while getopts t:s:d:o:n:i:p:m:h OPT
do
    case $OPT in
        t)  TYPE="-t ${OPTARG}"
            echo "TYPE:${OPTARG}"
            ;;
        s)  STATION_ID="-s ${OPTARG}"
            echo "STATION_ID:${OPTARG}"
            ;;
        d)  TIME="-d ${OPTARG}"
            echo "TIME:${OPTARG}"
            ;;
        o)  OUTDIR=${OPTARG%/}
            echo "OUTDIR:${OPTARG%/}"
            ;;
        n)  SUFFIX=${OPTARG}
            echo "SUFFIX:${OPTARG}"
            ;;
        i)  ID="-i ${OPTARG}"
            echo "ID:${OPTARG}"
            ;;
        p)  PASSWORD="-p ${OPTARG}"
            echo "PASSWORD:${OPTARG}"
            ;;
        m)  EMAIL=${OPTARG}
            echo "EMAIL:${OPTARG}"
            ;;
        h)  usage_exit
            ;;
        \?) usage_exit
            ;;
    esac
done

shift $((OPTIND - 1))

if [ -z "${OUTDIR}" ]; then
  usage_exit
fi

if [ -z "${SUFFIX}" ]; then
  usage_exit
fi

FILENAME=${SUFFIX}_$(date +\%Y-\%m-\%d-\%H\%M)
FILE=${OUTDIR}/${FILENAME}

echo "FILE:${FILE}"
RADISH="radi.sh ${TYPE} ${STATION_ID} ${TIME} ${ID} ${PASSWORD} -o ${FILE}"
echo ${RADISH}
eval ${RADISH}

if [ -n "${EMAIL}" ]; then
  SENDFILE=$(find ${OUTDIR}/ -maxdepth 1 -name ${FILENAME}.*)
  echo "SENDFILE:${SENDFILE}"
  if [ -n "${SENDFILE}" ]; then
    SENDAPPEND="sendappend ${SENDFILE} ${EMAIL}"
    echo ${SENDAPPEND}
    eval ${SENDAPPEND}
  fi
fi

