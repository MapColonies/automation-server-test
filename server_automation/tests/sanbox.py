import json

from server_automation.tests import test_exporter_tool as tester
from server_automation.functions import executors as exc
from server_automation.configuration import config
try:
    tester.test_export_geopackage()
    tester.test_box_size_limit()
    tester.test_export_on_storage()
    tester.test_download_package()
except Exception as e:
    print(e)
finally:
    exc.delete_requests(config.EXPORT_STORAGE_URL, tester.uuids)
