#!/bin/sh

export PYTHONPATH=.

. env/bin/activate

python3 start.py $*

