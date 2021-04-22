""" This module include executers to check environment deployment"""
import logging
from mc_automation_tools import bash_utils

_log = logging.getLogger('automation_tools.environment_validators')


def is_postgress_alive(ssh_conn):
    stdin, stdout, stderr = bash_utils.execute_command(ssh_conn, 'service postgresql status')
    stdout = stdout.readlines()
    if stdout:
        res = any("Active: active" in list for list in stdout)
        _log.info(f'Postgress service active running status: {res}')
        return res
    else:
        _log.error(f"postgresql service not exists on machine, related error:\n {stderr.readlines()}")
        return False
