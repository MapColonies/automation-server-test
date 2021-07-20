from server_automation.configuration import config_ingestion
from mc_automation_tools import postgres


def get_current_job_id(product_id, product_version, db_name=config_ingestion.PG_JOB_TASK_DB_NAME):
    """This method query and return uuid of current ingestion job according keys: productId and productVersion"""
    client = postgres.PGClass(config_ingestion.PG_HOST, db_name, config_ingestion.PG_USER, config_ingestion.PG_PASS)
    keys_values = {'resourceId': product_id, 'version': product_version}
    res = client.get_rows_by_keys('Job', keys_values, order_key='creationTime', order_desc=True)
    latest_job_id = res[0][0]
    return latest_job_id




