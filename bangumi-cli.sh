#!/bin/sh

export PYTHONPATH=.

. env/bin/activate

python3 utils/cli.py $*

