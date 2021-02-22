#!/bin/sh
#export FILE_LOGS=1 # remove to avoid logging to file - will print only to console
if [ "$CLEAN_UP" = 1 ];
then
    echo "<<<<____CLEAN UP IN PROGRESS____>>>>"
    python /source_code/server_automation/tests/cleanup.py
else
    echo "####____ RUNNING IN TEST MODE ____####"
    export OUTPUT_EXPORT_PATH=/opt/output
    export LOGS_OUTPUT=/opt/logs
    if [ "$JIRA_FILL" = 1 ];
    then
      echo "<<<<____RUNNING WITH JIRA UPDATE____>>>>"
      pytest /source_code/server_automation/tests/test_exporter_tool_jira.py
    else
      echo "<<<<____RUNNING WITHOUT JIRA UPDATE____>>>>"
      pytest /source_code/server_automation/tests/test_exporter_tool.py
    fi
fi
exit

