#!/bin/sh

export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890

export PYTHONPATH=./lib/

python=python3
#python=/opt/homebrew/bin/python3.10

$python bangumi.py $*


