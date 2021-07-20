import os
from server_automation.configuration import config_ingestion
from server_automation.ingestion_api import discrete_directory_loader
from server_automation.functions import ingestion_executors
os.environ['ORIG_DISCRETE_PATH'] = '/home/ronenk1/dev/automation-server-test/shp/1'
path = os.environ['ORIG_DISCRETE_PATH']

from mc_automation_tools import postgres
from server_automation.postgress import postgres_adapter


discrete_directory_loader.validate_source_directory(config_ingestion.ORIG_DISCRETE_PATH)
status_code, content = ingestion_executors.start_manuel_ingestion(path)
print(status_code, content)
res = postgres_adapter.get_current_job_id('MAS_6_ORT_247993', '1.0')
print(res)