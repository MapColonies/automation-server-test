#!/bin/bash


export FILE_LOGS=1 # remove to avoid logging to file - will print only to console



if [[ $CLEAN_UP == "1" ]]
then
    echo "clean up mode"
    python /source_code/server_automation/tests/cleanup.py
else
    echo "test mode"
    export OUTPUT_EXPORT_PATH=/opt/output
    export LOGS_OUTPUT=/opt/logs
    pytest /source_code/server_automation/tests
fi
exit

