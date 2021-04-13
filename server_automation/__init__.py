# pylint: disable=line-too-long, duplicate-code
"""
base initialization of automation infrastructure - init logger and etc.
"""
import logging
import os
import datetime

log_mode = os.environ.get('DEBUG_LOGS', None)
file_log = os.environ.get('FILE_LOGS', None)
log_output_path = os.environ.get('LOGS_OUTPUT', '/opt/logs')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


ch = logging.StreamHandler()

if not log_mode:
    ch.setLevel(logging.INFO)
else:
    ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if file_log:
    log_file_name = ".".join([str(datetime.datetime.utcnow()), 'log'])  # pylint: disable=invalid-name
    fh = logging.FileHandler(os.path.join(log_output_path, log_file_name))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)
