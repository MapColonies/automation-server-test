import enum
from server_automation.utils import common as common


class ResponseCode(enum.Enum):
    """
    Types of server responses
    """
    Ok = 200  # server return ok status
    ValidationErrors = 400  # bad request
    StatusNotFound = 404  # status\es not found on db
    ServerError = 500  # problem with error
    DuplicatedError = 409  # in case of requesting package with same name already exists


class EnvironmentTypes(enum.Enum):
    """
    Types of environment.
    """
    QA = 1
    DEV = 2
    PROD = 3

############      environment     ############
ENVIRONMENT_NAME = common.get_environment_variable('ENVIRONMENT_NAME', 'dev')
##############################################

###########      error massages     ##########
BOX_LIMIT_ERROR = 'ERR_BBOX_AREA_TOO_LARGE'
##############################################


PACKAGE_EXT = 'GPKG'

######################        Environment         #########################
EXPORTER_PORT = common.get_environment_variable('EXPORTER_PORT', "8081")
STORAGE_PORT = common.get_environment_variable('STORAGE_PORT', "8080")
DOWNLOAD_PORT = common.get_environment_variable('DOWNLOAD_PORT', "8082")
BASE_SERVICES_URL = common.get_environment_variable('SERVICES_URL', "http://10.45.128.8")
# BASE_SERVICES_URL = common.get_environment_variable('SERVICES_URL', "http://10.45.128.8")
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
MAX_EXPORT_RUNNING_TIME = 60 * common.get_environment_variable('MAX_EXPORT_RUNNING_TIME', 1)  # min

# PACKAGE_OUTPUT_DIR = '/mnt/outputs'
# PACKAGE_OUTPUT_DIR = '/mnt/exporter-worker/outputs'

PACKAGE_OUTPUT_DIR = common.get_environment_variable('OUTPUT_EXPORT_PATH', '/home/ronenk1/dev/output')

EXPORT_DOWNLOAD_DIR_NAME = common.get_environment_variable('TEST_DIR_NAME', 'download_test')
EXPORT_DOWNLOAD_FILE_NAME = common.get_environment_variable('TEST_PKG_NAME', 'test_case_9_exporter_api')


############################### S3 ############################################
S3_EXPORT_STORAGE_MODE = common.get_environment_variable('S3_EXPORT_STORAGE_MODE', False )
S3_DOWNLOAD_EXPIRATION_TIME = common.get_environment_variable("S3_DOWNLOAD_EXPIRED_TIME", 3600)
S3_DOWNLOAD_DIRECTORY = common.get_environment_variable('S3_DOWNLOAD_DIR', '/tmp/')
S3_BUCKET_NAME = common.get_environment_variable('S3_BUCKET_NAME', None)
S3_ACCESS_KEY = common.get_environment_variable('S3_ACCESS_KEY', None)
S3_SECRET_KEY = common.get_environment_variable('S3_SECRET_KEY', None)
S3_END_POINT = common.get_environment_variable('S3_END_POINT', None)

if S3_EXPORT_STORAGE_MODE:
    if not S3_BUCKET_NAME:
        raise Exception('S3_BUCKET_NAME while running on S3 mode')
    elif not S3_ACCESS_KEY:
        raise Exception('S3_ACCESS_KEY while running on S3 mode')
    elif not S3_SECRET_KEY:
        raise Exception('S3_SECRET_KEY while running on S3 mode')
    elif not S3_END_POINT:
        raise Exception('S3_SECRET_KEY while running on S3 mode')






############################ AUTOMATION DEV ENVIRONMENT VARIABLE ##############
DEV_MODE = common.get_environment_variable('DEV_MODE', True)  # todo when will be qa environment should be replaced False

BEST_LAYER_URL = common.get_environment_variable('BEST_LAYER', "http://10.28.11.95:8080/service?REQUEST=GetMap&SERVICE=WMS&LAYERS=combined_layers")
SOURCE_LAYER = common.get_environment_variable('SOURCE_LAYER', 'combined_layers')

