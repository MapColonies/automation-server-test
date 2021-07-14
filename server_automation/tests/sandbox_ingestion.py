import os
from server_automation.configuration import config_ingestion
from server_automation.ingestion_api import discrete_directory_loader

os.environ['ORIG_DISCRETE_PATH'] = '/home/ronenk1/dev/automation-server-test/shp/1'

discrete_directory_loader.validate_source_directory(config_ingestion.ORIG_DISCRETE_PATH)
