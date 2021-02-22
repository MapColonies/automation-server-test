# pylint: disable=line-too-long, invalid-name, broad-except
""" developing testing file """
import datetime
import os

from server_automation.tests import test_exporter_tool as tester, request_sampels
import logging
import json
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
# from server_automation.functions import executors as exc
# from server_automation.configuration import config
# try:
#     tester.test_export_geopackage()
#     tester.test_box_size_limit()
#     tester.test_export_on_storage()
#     tester.test_download_package()
# except Exception as e:
#     print(e)
# finally:
#     exc.delete_requests(config.EXPORT_STORAGE_URL, tester.uuids)

# import requests
# headers = {
#   'Content-Type': 'application/json',
#   'Authorization': 'OTU1NTA3MTEtNDM5Yi0zYzkyLWE2ODUtMTIzNzJkNGVjMjFjIDVmZDVjZjNhNjQyMDg5MDE0MTEwMWQ4YSBVU0VSX0RFRkFVTFRfTkFNRQ',
#   'zapiAccessKey': 'mBH1U-iI87H5D2KRs74xT8qDK5geZyo7wGUpUSIJPkQ'
# }
# resp = requests.get('https://rnd-hub.atlassian.net/rest/api/2/issue/MAPCO-287', params={'permissions': 'BROWSE_PROJECTS'}, headers=headers)
# logger.info("response code: %d", resp.status_code)
# logger.info("response message: %s", resp.content)
# # _log.debug("response message: %s" % resp.text)



import server_automation.exporter_api.trigger_api  as trigger_api
request = request_sampels.get_request_sample('et_req_2')
request = json.loads(request)
x = trigger_api.ExporterTrigger()
# x.post_exportGeopackage(request)
resp = x.get_exportStatus()
print(json.loads(resp.content))
resp = x.get_status_by_uuid("b4429f14-bd25-4e39-9adc-635a7a703210")
print(resp)