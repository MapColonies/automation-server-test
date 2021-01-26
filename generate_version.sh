#!/bin/bash
VER=$(python3 setup.py --version | sed 's/+/./g')

echo $(date):automation-test:$VER

echo version=$VER>version.txt
echo version=$VER>>version_history.txt
