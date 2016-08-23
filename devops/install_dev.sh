#!/bin/bash

#
# Note: If virtual environment commands don't work, either create
#       the env yourself as per the commands shown below, or install
#       libraries globally in a clean ubuntu vm.
#

# Virtual Environment
mkvirtualenv --python=/usr/bin/python3 stack-annotate
workon stack_annotate

# Python and Django libraries
pip install -r requirements.txt
