#!/usr/bin/env bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
__DIR__="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

echo "Run relatively to in \"${__DIR__}\""

# Get the help:
#
# python3 -m unittest --help

# -s "${__DIR__}"

python3  -m unittest discover -s "${__DIR__}/tests" "$@" -p *_test.py
python3  -m unittest discover -s "${__DIR__}/tests/web" "$@" -p *_test.py