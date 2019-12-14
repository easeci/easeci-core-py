#!/bin/bash

WORKSPACE=$1

if [[ $UID -ne 0 ]];
then
  echo 'Cannot run script as normal user. Run script with superuser privileges' >&2
  exit 1
fi

PYTHON=$(echo "$(python3 -V)" | awk '{print $2}' | cut -d '.' -f 1-3)
VERSION=$(echo "$PYTHON" | tr --delete .)

MIN_PY_VER='3.7.3'

if [[ "$VERSION" -lt $(echo $MIN_PY_VER | tr --delete .) ]];
then
  echo -e "Your python version ${PYTHON} is older than required\nMinimum version: ${MIN_PY_VER}\nPlease bump your python!" >&2
  exit 1
fi

CURRENT_DIR=$(pwd)
UNIT="${CURRENT_DIR}/systemd/easeci.service"
UNIT_TARGET="/etc/systemd/system"

if [[ -n "$WORKSPACE" ]];
then
  echo "EaseCI workspace specified in ${WORKSPACE}"
  sed -i "s#EASECI_HOME#$WORKSPACE#g" "${UNIT}"
else
  sed -i "s#EASECI_HOME##g" "${UNIT}"
fi

# Python environment preparation
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install uWSGI

RUN_COMMAND="$(whereis uwsgi | cut -d ' ' -f 2) --ini ${CURRENT_DIR}/uwsgi.ini"
sed -i "s#EASECI_RUN#${RUN_COMMAND}#g" "${UNIT}"

cp "${UNIT}" "${UNIT_TARGET}"
#systemctl daemon-reload
#systemctl start easeci
