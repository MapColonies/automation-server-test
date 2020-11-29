import os
from urllib.parse import urljoin
import posixpath
import enum


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
BOX_LIMIT_ERROR = 'ERR_BBOX_AREA_TOO_LARGE' ##
##############################################


PACKAGE_EXT = 'GPKG'


######################        Environment         #########################
EXPORTER_PORT = os.environ.get('EXPORTER_PORT', "8081")
STORAGE_PORT = os.environ.get('STORAGE_PORT', "8080")
DOWNLOAD_PORT = os.environ.get('DOWNLOAD_PORT', "8082")
BASE_SERVICES_URL = os.environ.get('SERVICES_URL', "http://10.45.128.8")
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

# def combine_url(base, *args) -> str:
#     """
#     This method concat / combine and build new url from list parts of url
#     :param base : this is the base relative uri
#     :param *args : sub directories of the url
#     """
#     for i in range(len(args)):
#         base = posixpath.join(base, args[i])
#     return base


EXPORT_REQUEST_PATH = "/home/ronenk1/dev/server/samples/request_short.json"

################################## timings ###################################
MAX_EXPORT_RUNNING_TIME = 60 * 10  # seconds

# PACKAGE_OUTPUT_DIR = '/mnt/outputs'
# PACKAGE_OUTPUT_DIR = '/mnt/exporter-worker/outputs'

PACKAGE_OUTPUT_DIR = os.environ.get('OUTPUT_EXPORT_PATH', '/home/ronenk1/dev/output')


EXPORT_DOWNLOAD_DIR_NAME = os.environ.get('TEST_DIR_NAME', 'test_dir')
EXPORT_DOWNLOAD_FILE_NAME = os.environ.get('TEST_PKG_NAME', 'exporter_tests')

