import json
import os
import io
import psycopg2
from SentinelS7Database import SentinelS7Database
# import requests


def get_device_id_and_table_name(queried_device_name, queried_client_name):
    db = SentinelS7Database(None)
    query = "SELECT serial_number, hypertable_name FROM system_view_device_company_device_type where alias = '{}' and name = '{}' limit 1".format(queried_device_name, queried_client_name)
    device_company_row = db.get_select_query_all_results(query)

    if len(device_company_row) > 0:
        device_id = device_company_row[0][0]
        table_name = device_company_row[0][1]
        result = [device_id, table_name]
        return result
    else:
        return []

def lambda_handler(event, context):
    device_alias = event['device_alias']
    client_id = event['client_id']
    from_date_time_utc_iso_str = event['from_date_time_utc_iso_str']
    to_date_time_utc_iso_str = event['to_date_time_utc_iso_str']
    # print(event)
    
    reporting = SentinelS7Database(None)
    reporting_conn = reporting.get_db_connection()
    reporting_cursor = reporting_conn.cursor()

    try:
        result = None
        queried_device_name = device_alias
        queried_client_name = client_id
        device_id_and_table_name = get_device_id_and_table_name(queried_device_name, queried_client_name)

        if len(device_id_and_table_name) == 2:
            print(device_id_and_table_name[0], device_id_and_table_name[1])
            SQL = "COPY (SELECT * FROM {} WHERE device_id = '{}' and published_at >= '{}' and published_at <= '{}') TO STDOUT WITH CSV HEADER".format(device_id_and_table_name[1], device_id_and_table_name[0], from_date_time_utc_iso_str, to_date_time_utc_iso_str)
            buf = io.StringIO()
            reporting_cursor.copy_expert(SQL, buf)
            buf.seek(0)
            result = buf.read()
            print(result)
    except (Exception, psycopg2.Error) as error:
        print(error)
    reporting_conn.commit()
    reporting_cursor.close()
    reporting_conn.close()

    # TODO implement
    return {
        'statusCode': 200,
        'body': result
    }

