#!/bin/bash

echo -n "Enter python version (Make sure you are on right python version) :  "
read PYTHON_VERSION

export ST_CLI_VERSION="0.1.post+${PYTHON_VERSION}_m1"
echo $ST_CLI_VERSION
echo "************"

rm -rf build dist st_cli.egg-info
python3 setup.py bdist_wheel

# file="st_cli-${ST_CLI_VERSION}-py3-none-any.whl"
cp -v dist/* ~/pycodes/s3_stcli_m1/

echo -n "File has been copied to ~/pycodes/s3_stcli_m1/ dir"

