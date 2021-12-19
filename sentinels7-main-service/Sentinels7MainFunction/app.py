import os
import boto3
import json
from datetime import datetime, timezone, timedelta
import decimal
from QueryDeviceTimescale import QueryDeviceTimescale
from SentinelS7Database import SentinelS7Database
import time

# import requests

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)
        
def get_device_id_and_table_name(queried_device_name, queried_client_name):
    db = SentinelS7Database(None)
    query = "SELECT serial_number, hypertable_name FROM system_view_device_company where alias = '{}' and name = '{}' limit 1".format(queried_device_name, queried_client_name)
    device_company_row = db.get_select_query_all_results(query)

    if len(device_company_row) > 0:
        device_id = device_company_row[0][0]
        table_name = device_company_row[0][1]
        result = [device_id, table_name]
        return result
    else:
        return []

def lambda_handler(event, context):
    result = 'Hello from Lambda!'
    if event is not None:
        print("Event:")
        print(event)
        # Start Engine
        if event.get('engine_start', False) and event.get('device_name', False) and event.get('client_name', False):
            queried_device_name = event.get('device_name', False)
            queried_client_name = event.get('client_name', False)
            device_id_and_table_name = get_device_id_and_table_name(queried_device_name, queried_client_name)
            
            if len(device_id_and_table_name) == 2:
                client = boto3.client('iot-data', region_name='us-east-1')
                response =  client.publish(
                            # topic='ternstar_company/send_device_commands/10000000d92ef835',
                            # topic='ternstar_company/send_device_commands/10000000a3dd89be',
                            topic='{}/send_device_commands/{}'.format(queried_client_name, device_id_and_table_name[0]),
                            qos=1,
                            payload=json.dumps({
                                "property": "engine",
                                "value": "start"
                            })
                            )
                result= response
            else:
                result=None
        # Stop Engine
        elif event.get('engine_stop', False) and event.get('device_name', False) and event.get('client_name', False):
            queried_device_name = event.get('device_name', False)
            queried_client_name = event.get('client_name', False)
            device_id_and_table_name = get_device_id_and_table_name(queried_device_name, queried_client_name)
            
            if len(device_id_and_table_name) == 2:
                client = boto3.client('iot-data', region_name='us-east-1')
                response =  client.publish(
                            # topic='ternstar_company/send_device_commands/10000000d92ef835',
                            # topic='ternstar_company/send_device_commands/10000000a3dd89be',
                            topic='{}/send_device_commands/{}'.format(queried_client_name, device_id_and_table_name[0]),
                            qos=1,
                            payload=json.dumps({
                                "property": "engine",
                                "value": "stop"
                            })
                            )
                result= response
            else:
                result=None
        # Start Feed
        elif event.get('feed_start', False) and event.get('device_name', False) and event.get('client_name', False):
            queried_device_name = event.get('device_name', False)
            queried_client_name = event.get('client_name', False)
            device_id_and_table_name = get_device_id_and_table_name(queried_device_name, queried_client_name)
            
            if len(device_id_and_table_name) == 2:
                client = boto3.client('iot-data', region_name='us-east-1')
                response =  client.publish(
                            # topic='ternstar_company/send_device_commands/10000000d92ef835',
                            #topic='ternstar_company/send_device_commands/10000000a3dd89be',
                            topic='{}/send_device_commands/{}'.format(queried_client_name, device_id_and_table_name[0]),
                            qos=1,
                            payload=json.dumps({
                                "property": "feed",
                                "value": "start"
                            })
                            )
                result= response
            else:
                result=None
        # Stop Feed
        elif event.get('feed_stop', False) and event.get('device_name', False) and event.get('client_name', False):
            queried_device_name = event.get('device_name', False)
            queried_client_name = event.get('client_name', False)
            device_id_and_table_name = get_device_id_and_table_name(queried_device_name, queried_client_name)
            
            if len(device_id_and_table_name) == 2:
                client = boto3.client('iot-data', region_name='us-east-1')
                response =  client.publish(
                            # topic='ternstar_company/send_device_commands/10000000d92ef835',
                            # topic='ternstar_company/send_device_commands/10000000a3dd89be',
                            topic='{}/send_device_commands/{}'.format(queried_client_name, device_id_and_table_name[0]),
                            qos=1,
                            payload=json.dumps({
                                "property": "feed",
                                "value": "stop"
                            })
                            )
                result= response
            else:
                result=None
        # Set Frequency Feed
        elif event.get('feed_frequency', False) and event.get('device_name', False) and event.get('client_name', False):
            queried_device_name = event.get('device_name', False)
            queried_client_name = event.get('client_name', False)
            device_id_and_table_name = get_device_id_and_table_name(queried_device_name, queried_client_name)
            
            if len(device_id_and_table_name) == 2:
                client = boto3.client('iot-data', region_name='us-east-1')
                response =  client.publish(
                            # topic='ternstar_company/send_device_commands/10000000d92ef835',
                            #topic='ternstar_company/send_device_commands/10000000a3dd89be',
                            topic='{}/send_device_commands/{}'.format(queried_client_name, device_id_and_table_name[0]),
                            qos=1,
                            payload=json.dumps({
                                "property": "feed",
                                "value": event.get('feed_frequency')
                            })
                            )
                result= response
            else:
                result=None
        elif event.get('partial_or_full_publish', False) and event.get('device_name', False) and event.get('client_name', False):
            queried_device_name = event.get('device_name', False)
            queried_client_name = event.get('client_name', False)
            device_id_and_table_name = get_device_id_and_table_name(queried_device_name, queried_client_name)
            
            if len(device_id_and_table_name) == 2:
                client = boto3.client('iot-data', region_name='us-east-1')
                response =  client.publish(
                            # topic='ternstar_company/send_device_commands/10000000d92ef835',
                            #topic='ternstar_company/send_device_commands/10000000a3dd89be',
                            topic='{}/send_device_commands/{}'.format(queried_client_name, device_id_and_table_name[0]),
                            qos=1,
                            payload=json.dumps({
                                "property": "feed",
                                "value": event.get('partial_or_full_publish')
                            })
                            )
                result= response
            else:
                result=None
        # Set Engine RPM
        elif event.get('engine_speed', False) and event.get('device_name', False) and event.get('client_name', False):
            queried_device_name = event.get('device_name', False)
            queried_client_name = event.get('client_name', False)
            device_id_and_table_name = get_device_id_and_table_name(queried_device_name, queried_client_name)
            
            if len(device_id_and_table_name) == 2:
                client = boto3.client('iot-data', region_name='us-east-1')
                response =  client.publish(
                            # topic='ternstar_company/send_device_commands/10000000d92ef835',
                            # topic='ternstar_company/send_device_commands/10000000a3dd89be',
                            topic='{}/send_device_commands/{}'.format(queried_client_name, device_id_and_table_name[0]),
                            qos=1,
                            payload=json.dumps({
                                "property": "engine_speed",
                                "value": event.get('engine_speed')
                            })
                            )
                result= response
            else:
                result=None
        # Get Feed Item by device_name and client_name (Normal Main Feed Query to DB)
        elif event.get('device_name', False) and event.get('client_name', False):
            queried_device_name = event.get('device_name', False)
            queried_client_name = event.get('client_name', False)
            device_id_and_table_name = get_device_id_and_table_name(queried_device_name, queried_client_name)
                        
            if len(device_id_and_table_name) == 2:
                print(device_id_and_table_name[0])
                print(device_id_and_table_name[1])
                query_device_timescale = QueryDeviceTimescale(None)
                start_time = time.time()
                response = query_device_timescale.run_device_query(device_id_and_table_name[0], device_id_and_table_name[1])
                end_time = time.time()
                print("--- %s seconds ---" % (end_time - start_time))
                result= response
            else:
                result= None
        # Get Feed Item by client_name (Normal Main Feed Query to DB. All devices data associated with a client)
        elif event.get('client_name', False):
            result= []
            # queried_device_name = event.get('device_name', False)
            queried_client_name = event.get('client_name', False)
            
            db = SentinelS7Database(None)
            query = "SELECT id,alias FROM system_view_device_company where name = '{}'".format(queried_client_name)
            device_alias_row = db.get_select_query_all_results(query)
            if len(device_alias_row) > 0:
                for device_alias in device_alias_row:
                    queried_device_name = device_alias[1]
                    print(queried_device_name)
                    device_result = {'device_id': device_alias[0], 'device_alias': device_alias[1], 'device_feed': None}
                    
                    device_id_and_table_name = get_device_id_and_table_name(queried_device_name, queried_client_name)
                                
                    if len(device_id_and_table_name) == 2:
                        print(device_id_and_table_name[0])
                        print(device_id_and_table_name[1])
                        query_device_timescale = QueryDeviceTimescale(None)
                        start_time = time.time()
                        response = None
                        try:
                          response = query_device_timescale.run_device_query(device_id_and_table_name[0], device_id_and_table_name[1])
                        except Exception as e:
                          print("An exception occurred: " + str(e))
                        end_time = time.time()
                        print("--- %s seconds ---" % (end_time - start_time))
                        device_result['device_feed']= response
                    result.append(device_result)
        elif event.get('client_id', False):
            db = SentinelS7Database(None)
            queried_client_id = event.get('client_id', False)
            query = "SELECT id,alias FROM system_view_device_company where name = '{}'".format(queried_client_id)
            device_alias_row = db.get_select_query_all_results(query)

            if len(device_alias_row) > 0:
                result_list = []
                for device_alias in device_alias_row:
                    result_list.append({
                                "id": device_alias[0],
                                "alias": device_alias[1]
                            })
                result = result_list
            else:
                result = None
        elif event.get('email', False) and event.get('key', False) and event.get('value', False):
            db = SentinelS7Database(None)
            queried_email = event.get('email', False)
            queried_key = event.get('key', False)
            queried_value = event.get('value', False)
            
            query = "select id from system_user where email = '{}'".format(queried_email)
            system_user_id = db.get_select_query_all_results(query)[0][0]
            print(system_user_id)
            
            db_update = SentinelS7Database(None)
            db_update_conn = db_update.get_db_connection()
            db_update_cursor = db_update_conn.cursor()
            query = "Update system_user_app_config SET value = {} where user_id = {} and key = '{}'".format(queried_value, system_user_id, queried_key)
            db_update_cursor.execute(query)
            db_update_conn.commit()
            db_update_cursor.close()
            db_update_conn.close()
            
            result = {
                'success': True
            }
        # Get Company Info by User's Email from sentinels7-users
        elif event.get('email', False):
            db = SentinelS7Database(None)
            queried_email = event.get('email', False)
            query = "select * from system_view_user_company_app_config where email = '{}'".format(queried_email)
            user_company_app_config = db.get_select_query_all_results(query)

            if len(user_company_app_config) > 0:
                print(user_company_app_config)
                company_name = user_company_app_config[0][5]
                user_app_config = []
                for app_config in user_company_app_config:
                    user_app_config.append({
                        'key': app_config[1],
                        'value': app_config[2],
                        'type': app_config[3]
                    })
                result = {
                    'company_name': company_name,
                    'user_app_config': user_app_config
                }
            else:
                result = None
    else:
        print("Event object is None")
        result = "Event object is None"
    return result
