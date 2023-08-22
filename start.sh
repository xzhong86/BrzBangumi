#!/bin/sh

export PYTHONPATH=.

. env/bin/activate

python3 app-bangumi.py $*

