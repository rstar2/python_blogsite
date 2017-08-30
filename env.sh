#! /bin/bash

if [ "$1" == 'install' ]
then
    # if this is the first time 
    # install the Virtual environment,
    # activate it and install needed Python packages
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
else
    # if this is normal day work - activate the environment and open VSCodess
    source env/bin/activate
    if [ "$1" == "code" ]
    then
        code .
    fi
fi
