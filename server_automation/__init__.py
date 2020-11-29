import logging
import os

log_mode = os.environ.get('DEBUG_LOGS', None)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
#
# if (logger.hasHandlers()):
#     logger.handlers.clear()

ch = logging.StreamHandler()
if not log_mode:
    ch.setLevel(logging.INFO)
else:
    ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)

