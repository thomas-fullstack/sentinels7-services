import json
import os
import io
import psycopg2
from SentinelS7Database import SentinelS7Database
# import requests

def lambda_handler(event, context):
    input_data_json = event
    device_id = event['device_id']
    table_name = event['table_name']
    from_date_time_utc_iso_str = event['from_date_time_utc_iso_str']
    to_date_time_utc_iso_str = event['to_date_time_utc_iso_str']
    # print(event)
    
    reporting = SentinelS7Database(None)
    reporting_conn = reporting.get_db_connection()
    reporting_cursor = reporting_conn.cursor()

    try:
        SQL = "COPY (SELECT * FROM {} WHERE device_id = '{}' and published_at >= '{}' and published_at <= '{}') TO STDOUT WITH CSV HEADER".format(table_name, device_id, from_date_time_utc_iso_str, to_date_time_utc_iso_str)
        buf = io.StringIO()
        reporting_cursor.copy_expert(SQL, buf)
        buf.seek(0)
        result = buf.read()
        # print(result)
    except (Exception, psycopg2.Error) as error:
        print(error)
    reporting_conn.commit()
    reporting_cursor.close()
    reporting_conn.close()

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

