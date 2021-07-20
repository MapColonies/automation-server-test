""" configuration for running ingestion tests"""
from mc_automation_tools import common


ORIG_DISCRETE_PATH = common.get_environment_variable('ORIG_DISCRETE_PATH', '/home/ronenk1/dev/automation-server-test/shp/1')
SHAPES_PATH = common.get_environment_variable('SHAPES_PATH', 'Shapes')
TIFF_PATH = common.get_environment_variable('TIFF_PATH', 'tiff')
# SHAPE_FILE_LIST = ['Files.dbf', 'Product.shp', 'Product.dbf', 'ShapeMetadata.shp', 'ShapeMetadata.dbf']
SHAPE_FILE_LIST = ['Files.shp', 'Files.dbf', 'Product.shp', 'Product.dbf', 'ShapeMetadata.shp', 'ShapeMetadata.dbf']


##################################################  Ingestion API's sub urls & API's  ######################################################
INGESTION_MANUAL_TRIGGER = 'trigger'
INGESTION_WATCHER_STATUS = 'status'
INGESTION_START_WATCHER = 'start'
INGESTION_STOP_WATCHER = 'stop'
INGESTION_AGENT_URL = common.get_environment_variable('INGESTION_AGENT_URL', 'https://discrete-agent-dev-agent-route-raster-dev.apps.v0h0bdx6.eastus.aroapp.io')

##################################################  POSTGRESS CREDENTIALS  ######################################################
PG_USER = common.get_environment_variable('PG_USER', None)
PG_PASS = common.get_environment_variable('PG_PASS', None)
PG_HOST = common.get_environment_variable('PG_HOST', None)
PG_JOB_TASK_DB_NAME = common.get_environment_variable('PG_JOB_TASK_DB_NAME', None)