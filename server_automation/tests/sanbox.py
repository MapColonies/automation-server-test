import json

from server_automation.exporter_api import base_requests as conn
from server_automation.exporter_api import storage_utils as sc
from server_automation.configuration.config import *
from server_automation.utils import common
from server_automation.functions import executors as exc
from server_automation.configuration import config
# url = "http://10.28.11.49:8081/exportGeopackage"
request = json.load(open("/home/ronenk1/dev/server/samples/request_sanity.json", "r"))
exc.clear_all_tasks(config.EXPORT_STORAGE_URL)
conn.send_get_request("http://10.45.128.8:8082/downloads/uuuu/uuuuu.GPKG")
s_code, content = exc.send_export_request(request_path=config.EXPORT_REQUEST_PATH)
#
res = exc.exporter_follower(EXPORT_STORAGE_URL, content['uuid'])
# res = exc.exporter_follower(EXPORT_STORAGE_URL, '951cb3e2-7fbd-4d52-8dec-6b9f393fec5a')

file_location = res['fileURI']
pkg_url = common.combine_url(config.PACKAGE_OUTPUT_DIR, *(file_location.split('/')[-2:]))

res = exc.validate_geo_package(pkg_url)

# exc.exporter_follower(common.combine_url(EXPORT_STORAGE_URL), "c0448ccd-5377-4eb9-8692-e96e71a826b6")
s_code, content = common.response_parser(sc.get_all_statuses(EXPORT_STORAGE_URL))
exc.send_export_request()
sample_uuid = "67a570b7-f67a-4709-8854-1ef5b969a97d"
resp = sc.get_uuid_status(common.combine_url(EXPORT_STORAGE_URL, STATUSES_API), sample_uuid)
s_code, content = common.response_parser(resp)
conn.send_post_request(common.combine_url(EXPORT_TRIGGER_URL, EXPORT_GEOPACKAGE_API), request)
print(common.combine_url(EXPORT_TRIGGER_URL, EXPORT_GEOPACKAGE_API))

resp = sc.delete_by_uuid(common.combine_url(EXPORT_STORAGE_URL, STATUSES_API),[sample_uuid])
s_code, content = common.response_parser(resp)
