# pylint: disable=line-too-long
"""
This module provide some common functionality to clean testing environment
"""
import logging
import server_automation.functions.executors as exc
import server_automation.configuration.config as config


_log = logging.getLogger('server.tests.cleanup')


def clean_db():
    """
    This method clean all task written on storage from current running environment
    """
    resp = exc.clear_all_tasks(config.EXPORT_STORAGE_URL)
    _log.info('Cleanup returned with response: %s', resp)
    return resp


if __name__ == '__main__':
    clean_db()
