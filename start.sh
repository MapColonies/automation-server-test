#!/bin/bash

if [[ $CLEAN_UP == "1" ]]
then
    echo "clean up mode"
    python /source_code/server_automation/tests/cleanup.py
else
    echo "test mode"
    export OUTPUT_EXPORT_PATH=/opt/output
    pytest /source_code/server_automation/tests
fi
exit

