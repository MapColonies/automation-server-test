import os
from server_automation.configuration import config_ingestion
from server_automation.ingestion_api import discrete_directory_loader
from server_automation.functions import ingestion_executors
os.environ['ORIG_DISCRETE_PATH'] = '/home/ronenk1/dev/automation-server-test/shp/1'
path = os.environ['ORIG_DISCRETE_PATH']

from mc_automation_tools import postgres
from server_automation.postgress import postgress_adapter


discrete_directory_loader.validate_source_directory(config_ingestion.ORIG_DISCRETE_PATH)
status_code, content = ingestion_executors.start_manuel_ingestion(path)
job_id = postgress_adapter.get_current_job_id('MAS_6_ORT_247993', '1.0')
res = postgress_adapter.get_job_by_id(job_id)
ingestion_executors.follow_running_task(job_id, timeout=config_ingestion.FOLLOW_TIMEOUT)
print(res)