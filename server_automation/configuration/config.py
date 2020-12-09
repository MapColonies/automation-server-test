import os
import enum
from server_automation.utils.common import *


class ResponseCode(enum.Enum):
    """
    Types of server responses
    """
    Ok = 200  # server return ok status
    ValidationErrors = 400  # bad request
    StatusNotFound = 404  # status\es not found on db
    ServerError = 500  # problem with error
    DuplicatedError = 409  # in case of requesting package with same name already exists


###########      error massages     ##########
BOX_LIMIT_ERROR = 'ERR_BBOX_AREA_TOO_LARGE'
##############################################


PACKAGE_EXT = 'GPKG'

######################        Environment         #########################
EXPORTER_PORT = get_environment_variable('EXPORTER_PORT', "8081")
STORAGE_PORT = get_environment_variable('STORAGE_PORT', "8080")
DOWNLOAD_PORT = get_environment_variable('DOWNLOAD_PORT', "8082")
BASE_SERVICES_URL = get_environment_variable('SERVICES_URL', "http://10.45.128.8")
# BASE_SERVICES_URL = "http://10.28.11.49"
###########################################################################


# EXPORT_GP_URL = "http://10.28.11.49:8081"
EXPORT_TRIGGER_URL = ':'.join([BASE_SERVICES_URL, EXPORTER_PORT])
EXPORT_STORAGE_URL = ':'.join([BASE_SERVICES_URL, STORAGE_PORT])
DOWNLOAD_STORAGE_URL = ':'.join([BASE_SERVICES_URL, DOWNLOAD_PORT])

###############  API's sub urls  #############
EXPORT_GEOPACKAGE_API = "exportGeopackage"
STATUSES_API = "statuses"
DELETE_API = "delete"
DOWNLOAD_API = "downloads"
##############################################

############### Requests Status Indexer Service - STATUSES ###################
EXPORT_STATUS_IN_PROGRESS = "In-Progress"
EXPORT_STATUS_COMPLITED = "Completed"
EXPORT_STATUS_PENDING = "Pending"
EXPORT_STATUS_FAILED = "Failed"

# EXPORT_REQUEST_PATH = "/home/ronenk1/dev/server/samples/request_short.json"

################################## timings ###################################
MAX_EXPORT_RUNNING_TIME = 60 * get_environment_variable('MAX_EXPORT_RUNNING_TIME', 10)  # min

# PACKAGE_OUTPUT_DIR = '/mnt/outputs'
# PACKAGE_OUTPUT_DIR = '/mnt/exporter-worker/outputs'

PACKAGE_OUTPUT_DIR = get_environment_variable('OUTPUT_EXPORT_PATH', '/home/ronenk1/dev/output')

EXPORT_DOWNLOAD_DIR_NAME = get_environment_variable('TEST_DIR_NAME', 'test_dir')
EXPORT_DOWNLOAD_FILE_NAME = get_environment_variable('TEST_PKG_NAME', 'exporter_tests')
