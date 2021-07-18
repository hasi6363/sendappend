#!/bin/bash

if [ $# -ne 2 ]; then
  echo "usage: ${0} <file path> <email address>"
  echo " e.g.: ${0} /srv/test.txt aaa@bbb.ccc"
  exit 1
fi

FILE=${1}
EMAIL=${2}

echo "FILE:${FILE}"
echo "EMAIL:${EMAIL}"

uuencode ${FILE} $(basename ${FILE}) | mail ${EMAIL}

