"""
This module is responsible to provide configuration for development purpose.
For example: Development of new automation tests and infra-logic, CI|CD, integration etc.
"""
from mc_automation_tools import common

# routes and url
EXPORT_TRIGGER_URL = common.get_environment_variable('EXPORTER_TRIGGER_API', "https://trigger-raster.apps.v0h0bdx6.eastus.aroapp.io")
EXPORT_UI_URL = common.get_environment_variable('EXPORT_UI_URL', 'http://ui-raster.apps.v0h0bdx6.eastus.aroapp.io/')
MAP_PROXY_URL = common.get_environment_variable('MAP_PROXY_URL', 'http://map-raster.apps.v0h0bdx6.eastus.aroapp.io/')

# S3 environments
S3_BUCKET_NAME = common.get_environment_variable('S3_BUCKET_NAME', None)
S3_ACCESS_KEY = common.get_environment_variable('S3_ACCESS_KEY', None)
S3_SECRET_KEY = common.get_environment_variable('S3_SECRET_KEY', None)
S3_END_POINT = common.get_environment_variable('S3_END_POINT', None)

# map proxy layers env
BEST_LAYER_URL = common.get_environment_variable('BEST_LAYER',
                                                 "http://map-raster.apps.v0h0bdx6.eastus.aroapp.io/service?REQUEST=GetMap&SERVICE=WMS&LAYERS=full_il")
SOURCE_LAYER = common.get_environment_variable('SOURCE_LAYER', 'full_il')


# machines:
POSTGRESS_VM = common.get_environment_variable('POSTGRESS_MACHINE', 'localhost')
KAFKA_VM = common.get_environment_variable('KAFKA_VM', 'localhost')
KAFKA_PORT = common.get_environment_variable('KAFKA_PORT', 9092)
# azure credential:
AZURE_USER_NAME = common.get_environment_variable('AZURE_USER_NAME', 'user')
AZURE_PASSWORD = common.get_environment_variable('AZURE_PASSWORD', 'password')


# general:
HTTP_REQ_TIMEOUT = common.get_environment_variable('HTTP_REQ_TIMEOUT', 20)
