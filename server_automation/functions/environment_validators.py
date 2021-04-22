""" This module include executers to check environment deployment"""
import paramiko
from mc_automation_tools import bash_utils

def is_postgress_alive(ssh_conn):
    stdin, stdout, stderr = bash_utils.execute_command('service postgresql status')
    pass