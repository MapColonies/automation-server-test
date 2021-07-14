"""
This module implement wrapping layer to mc - raster - trigger api for exporting. it provide trigger class that implements and extend
functionality
"""
import json
import logging
from server_automation.configuration import config
from mc_automation_tools import common as common
from mc_automation_tools import base_requests as br

# from server_automation.utils import common, base_requests as br

_log = logging.getLogger("server_automation.exporter_api.trigger_api")


class ExporterTrigger:
    """
    This class wrapping Exporter trigger service's api and provide useful extended methods
    """
    def __init__(self):
        self._base_url = config.EXPORT_TRIGGER_URL
        self._export_url = common.combine_url(self._base_url, config.EXPORT_GEOPACKAGE_API)
        self._get_status_url = common.combine_url(self._base_url, config.GET_EXPORT_STATUSES_API)

    def post_exportGeopackage(self, request):
        """
        This method will trigger standard geopackage export request process
        """
        if not isinstance(request, dict):
            _log.error(f'Request should be provided as valid json format:\n{request} => {type(request)}')
            raise TypeError('Request should be provided as valid json format')

        resp = br.send_post_request(self._export_url, request)
        return resp

    def get_exportStatus(self):
        """
        This method send get request to trigger API and return all task status data
        """
        resp = br.send_get_request(self._get_status_url)
        return resp

    def get_status_by_uuid(self, uuid):
        """
        This method return single status by providing uuid
        """

        all_statuses = self.get_exportStatus()
        if not all_statuses.content:
            _log.info('No statuses for export exists')
            return None
        status_code = all_statuses.status_code
        all_statuses = json.loads(all_statuses.content)
        res_status = None
        for status in all_statuses:
            if status['taskId'] == uuid:
                res_status = status
                break

        return res_status, status_code
