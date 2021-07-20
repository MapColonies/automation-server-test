# pylint: disable=line-too-long
""" configuration interface """
import enum
from mc_automation_tools import common


class ResponseCode(enum.Enum):
    """
    Types of server responses
    """
    Ok = 200  # server return ok status
    ValidationErrors = 400  # bad request
    StatusNotFound = 404  # status\es not found on db
    DuplicatedError = 409  # in case of requesting package with same name already exists
    GetwayTimeOut = 504  # some server didn't respond
    ServerError = 500  # problem with error


class EnvironmentTypes(enum.Enum):
    """
    Types of environment.
    """
    QA = 1
    DEV = 2
    PROD = 3


####################################      Running global environment variables     #####################################
# pylint: disable=fixme
ENVIRONMENT_NAME = common.get_environment_variable('ENVIRONMENT_NAME', 'dev')
DEV_MODE = common.get_environment_variable('DEV_MODE',
                                           True)  # todo when will be qa environment should be replaced False
TMP_DIR = common.get_environment_variable('TMP_DIR', '/tmp/auto-exporter')
RUNNING_WORKERS_NUMBER = common.get_environment_variable('N_WORKERS', 2)
#######################################################      ERROR MASSAGES     ############################################################
BOX_LIMIT_ERROR = 'ERR_BBOX_AREA_TOO_LARGE'
############################################################   GENERAL   ###################################################################
PACKAGE_EXT = 'GPKG'
#####################################################        Environment         ###########################################################
OPENSHIFT_DEPLOY = common.get_environment_variable('OPENSHIFT_DEPLOY', True)
if not OPENSHIFT_DEPLOY:
    EXPORTER_PORT = common.get_environment_variable('EXPORTER_PORT', "8081")
    STORAGE_PORT = common.get_environment_variable('STORAGE_PORT', "8080")
    DOWNLOAD_PORT = common.get_environment_variable('DOWNLOAD_PORT', "8082")
    BASE_SERVICES_URL = common.get_environment_variable('SERVICES_URL', "http://10.45.128.8")
    EXPORT_TRIGGER_URL = ':'.join([BASE_SERVICES_URL, EXPORTER_PORT])
    EXPORT_STORAGE_URL = ':'.join([BASE_SERVICES_URL, STORAGE_PORT])
    DOWNLOAD_STORAGE_URL = ':'.join([BASE_SERVICES_URL, DOWNLOAD_PORT])
    EXPORT_TRIGGER_URL = common.get_environment_variable('EXPORTER_TRIGGER_API', "http://10.45.128.8")
    EXPORT_UI_URL = common.get_environment_variable('EXPORT_UI_URL', 'http://ui-raster.apps.v0h0bdx6.eastus.aroapp.io/')

else:
    EXPORT_TRIGGER_URL = common.get_environment_variable('EXPORTER_TRIGGER_API',
                                                         "https://trigger-raster.apps.v0h0bdx6.eastus.aroapp.io")
    EXPORT_UI_URL = common.get_environment_variable('EXPORT_UI_URL', 'http://ui-raster.apps.v0h0bdx6.eastus.aroapp.io/')
    MAP_PROXY_URL = common.get_environment_variable('MAP_PROXY_URL', 'http://map-raster.apps.v0h0bdx6.eastus.aroapp.io/')

    # STORAGE_NAME_SPACE = common.get_environment_variable('STORAGE_PORT', "8080")  # TODO - not provided yet
    # DOWNLOAD_PORT = common.get_environment_variable('DOWNLOAD_PORT', "8082")
# BASE_SERVICES_URL = common.get_environment_variable('SERVICES_URL', "http://10.45.128.8")
# BASE_SERVICES_URL = "http://10.28.11.49"


#######################################################  Exporter API's sub urls  ##########################################################
EXPORT_GEOPACKAGE_API = "exportGeopackage"
GET_EXPORT_STATUSES_API = "exportStatus"
STATUSES_API = "statuses"  # not in use on prod
DELETE_API = "delete"  # not in use on prod
DOWNLOAD_API = "downloads"  # not in use on prod

################################################  Requests Status Indexer Service - STATUSES  ##############################################
EXPORT_STATUS_IN_PROGRESS = "In-Progress"
EXPORT_STATUS_COMPLITED = "Completed"
EXPORT_STATUS_PENDING = "Pending"
EXPORT_STATUS_FAILED = "Failed"

# EXPORT_REQUEST_PATH = "/home/ronenk1/dev/server/samples/request_short.json"

############################################################  TIMEOUT CONFIG  ##############################################################
MAX_EXPORT_RUNNING_TIME = 60 * common.get_environment_variable('MAX_EXPORT_RUNNING_TIME', 10)  # min

# PACKAGE_OUTPUT_DIR = '/mnt/outputs'
# PACKAGE_OUTPUT_DIR = '/mnt/exporter-worker/outputs'

PACKAGE_OUTPUT_DIR = common.get_environment_variable('OUTPUT_EXPORT_PATH', '/home/ronenk1/dev/output')

EXPORT_DOWNLOAD_DIR_NAME = common.get_environment_variable('TEST_DIR_NAME', 'download_test')
EXPORT_DOWNLOAD_FILE_NAME = common.get_environment_variable('TEST_PKG_NAME', 'test_case_9_exporter_api')

################################################################## S3 ######################################################################
S3_EXPORT_STORAGE_MODE = common.get_environment_variable('S3_EXPORT_STORAGE_MODE', False)
S3_DOWNLOAD_EXPIRATION_TIME = common.get_environment_variable("S3_DOWNLOAD_EXPIRED_TIME", 3600)
S3_DOWNLOAD_DIRECTORY = common.get_environment_variable('S3_DOWNLOAD_DIR', '/tmp/')
S3_BUCKET_NAME = common.get_environment_variable('S3_BUCKET_NAME', None)
S3_ACCESS_KEY = common.get_environment_variable('S3_ACCESS_KEY', None)
S3_SECRET_KEY = common.get_environment_variable('S3_SECRET_KEY', None)
S3_END_POINT = common.get_environment_variable('S3_END_POINT', None)

# pylint: disable=no-else-raise
if S3_EXPORT_STORAGE_MODE:
    if not S3_BUCKET_NAME:
        raise Exception('S3_BUCKET_NAME while running on S3 mode')
    elif not S3_ACCESS_KEY:
        raise Exception('S3_ACCESS_KEY while running on S3 mode')
    elif not S3_SECRET_KEY:
        raise Exception('S3_SECRET_KEY while running on S3 mode')
    elif not S3_END_POINT:
        raise Exception('S3_SECRET_KEY while running on S3 mode')

###################################################### LAYER CONFIGURATION DATA VARIABLE ###################################################
BEST_LAYER_URL = common.get_environment_variable('BEST_LAYER',
                                                 "http://map-raster.apps.v0h0bdx6.eastus.aroapp.io/service?REQUEST=GetMap&SERVICE=WMS&LAYERS=bluemarble_il")
SOURCE_LAYER = common.get_environment_variable('SOURCE_LAYER', 'bluemarble_il')

######################################################## REPORTING RESULTS VARIABLES #######################################################
USE_JIRA = common.get_environment_variable('USE_JIRA', False)
FILE_URL = common.get_environment_variable('JIRA_CONF', '/opt/jira/jira_config.json')
