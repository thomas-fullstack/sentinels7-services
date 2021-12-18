import json
import os
# import psycopg2
from SentinelS7Database import SentinelS7Database
# import requests


def lambda_handler(event, context):
    input_data_json = event
    device_id = event['device_id']
    published_at = event['published_at']
    table_name = event['table_name']
    partial_publish = event['partial_publish']
    modbus_active = event['modbus_active']
    print(event)
    
    db_insert = SentinelS7Database(None)
    db_insert_conn = db_insert.get_db_connection()
    db_insert_cursor = db_insert_conn.cursor()
    if modbus_active == 0 or partial_publish == 1: 
        #  If partial publish set missing params to -999 and populate the measures available
        db = SentinelS7Database(None)
        query = "select json_data from system_modbus_config_json where file_name = '{}' limit 1".format('all_controls_inc_holding_registers_insert_defaults_partial')
        input_data_json_populated = db.get_select_query_all_results(query)[0][0]
        # with open('all_controls_inc_holding_registers.json') as f:
        #     input_data_json_populated = json.load(f)
        for measure_name in input_data_json:
            input_data_json_populated[measure_name] = input_data_json[measure_name]
            # print(input_data_json_populated)
        input_data_json = input_data_json_populated
        
    # fleet_data = []
    print(input_data_json)
    SQL = "INSERT INTO {} (device_id, published_at, measure_name, measure_value) VALUES (%s, %s, %s, %s);".format(table_name)
    for measure_name in input_data_json:
        try:
            if measure_name not in ['partial_publish', 'device_id', 'published_at', 'table_name']:
                measure_value = input_data_json[measure_name]
                fleet_data_row = (device_id, published_at, measure_name, measure_value)
                db_insert_cursor.execute(SQL, fleet_data_row)
                # print(fleet_data_row)
                # fleet_data.append(fleet_data_row)
                # print("The key and value are ({}) = ({})".format(measure_name, measure_value))
                # print(device_id, published_at)
        except (Exception, psycopg2.Error) as error:
            print(error)
    db_insert_conn.commit()
    db_insert_cursor.close()
    db_insert_conn.close()

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Inserted feed row successfully!')
    }

