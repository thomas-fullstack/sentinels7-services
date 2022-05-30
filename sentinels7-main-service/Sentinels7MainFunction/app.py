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
        
def get_device_id_device_type_and_table_name(queried_device_name, queried_client_name):
    db = SentinelS7Database(None)
    query = "SELECT serial_number, hypertable_name, vfd_x_600_hyper_table_name, device_type FROM system_view_device_company_device_type_order_category_name where alias = '{}' and name = '{}' limit 1".format(queried_device_name, queried_client_name)
    device_company_row = db.get_select_query_all_results(query)

    if len(device_company_row) > 0:
        device_id = device_company_row[0][0]
        device_type = device_company_row[0][3]
        if device_type == 'VFD_X_600':
            table_name = device_company_row[0][2]
        else: 
            table_name = device_company_row[0][1]
        result = [device_id, table_name, device_type]
        return result
    else:
        return []

def get_multiple_device_ids_device_types_order_category_table_name(queried_devices_alias_list, queried_client_name):
    db = SentinelS7Database(None)
    query = "SELECT id, serial_number, alias, hypertable_name, vfd_x_600_hyper_table_name, device_type, device_order, category_name FROM system_view_device_company_device_type_order_category_name where alias in ({}) and name = '{}'".format(','.join(['%s'] * len(queried_devices_alias_list)), queried_client_name)
    devices_company = db.get_select_query_all_results_with_params(query, queried_devices_alias_list)

    if len(devices_company) > 0:
        return devices_company
    else:
        return []

def send_device_commands(queried_device_name, queried_client_name, command_json):
    result=None
    device_id_device_type_and_table_name = get_device_id_device_type_and_table_name(queried_device_name, queried_client_name)
    
    if len(device_id_device_type_and_table_name) == 3:
        client = boto3.client('iot-data', region_name='us-east-1', verify=False)
        response =  client.publish(
                    # topic='ternstar_company/send_device_commands/10000000d92ef835',
                    # topic='ternstar_company/send_device_commands/10000000a3dd89be',
                    topic='{}/send_device_commands/{}'.format(queried_client_name, device_id_device_type_and_table_name[0]),
                    qos=1,
                    payload=json.dumps(command_json)
                    )
        result=response
    else:
        result=None
    return result

def lambda_handler(event, context):
    result = 'Hello from Lambda!'
    if event is not None:
        print("Event:")
        print(event)
        # Start Engine
        if event.get('engine_start', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                    "property": "engine",
                    "value": "start"
                }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Stop Engine
        elif event.get('engine_stop', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                        "property": "engine",
                        "value": "stop"
                    }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Start Feed
        elif event.get('feed_start', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                        "property": "feed",
                        "value": "start"
                    }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Stop Feed
        elif event.get('feed_stop', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                            "property": "feed",
                            "value": "stop"
                        }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Set Engine RPM
        elif event.get('engine_speed', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                            "property": "engine_speed",
                            "value": event.get('engine_speed')
                        }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Start Motor
        elif event.get('motor_start', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                            "property": "motor",
                            "value": "start"
                        }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Stop Motor
        elif event.get('motor_stop', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                            "property": "motor",
                            "value": "stop"
                        }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Set Motor Hz
        elif event.get('motor_speed', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                            "property": "motor_speed",
                            "value": event.get('motor_speed')
                        }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Auto Mode
        elif event.get('auto_mode', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                            "property": "auto",
                            "value": "true"
                        }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Manual Mode
        elif event.get('manual_mode', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                            "property": "manual",
                            "value": "true"
                        }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Fault Reset
        elif event.get('fault_reset', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                            "property": "fault_reset",
                            "value": "true"
                        }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Set Target Setpoint
        elif event.get('target_setpoint', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                            "property": "target_setpoint",
                            "value": event.get('target_setpoint')
                        }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Set high_pressure_limit
        elif event.get('high_pressure_limit', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                            "property": "high_pressure_limit",
                            "value": event.get('high_pressure_limit')
                        }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Set high_pressure_shutdown
        elif event.get('high_pressure_shutdown', False) and event.get('device_name', False) and event.get('client_name', False):
            command_json = {
                            "property": "high_pressure_shutdown",
                            "value": event.get('high_pressure_shutdown')
                        }
            result= send_device_commands(
                event.get('device_name', False),
                event.get('client_name', False),
                command_json
                )
        # Get Feed Item by device_name and client_name (Normal Main Feed Query to DB)
        elif event.get('device_name', False) and event.get('client_name', False):
            queried_device_name = event.get('device_name', False)
            queried_client_name = event.get('client_name', False)
            device_id_device_type_and_table_name = get_device_id_device_type_and_table_name(queried_device_name, queried_client_name)
                        
            if len(device_id_device_type_and_table_name) == 3:
                # print(device_id_and_table_name[0])
                # print(device_id_and_table_name[1])
                query_device_timescale = QueryDeviceTimescale(None)
                start_time = time.time()
                response = query_device_timescale.run_device_query(device_id_device_type_and_table_name[0], device_id_device_type_and_table_name[1], device_id_device_type_and_table_name[2])
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
            query = "SELECT id,alias FROM system_view_device_company_device_type_order_category_name where name = '{}'".format(queried_client_name)
            device_alias_row = db.get_select_query_all_results(query)
            devices_result = []
            devices_alias = []
            
            if len(device_alias_row) > 0:
                # print(device_alias_row)
                for device_alias in device_alias_row:
                    alias = device_alias[1]
                    # print(devices_alias)
                    devices_alias.append(alias)

            # print(devices_alias)
            device_ids_and_table_name = get_multiple_device_ids_device_types_order_category_table_name(devices_alias, queried_client_name)
            devices_table_name = None
            controls_inc_devices = []
            controls_inc_responses = None
            vfd_x_600_devices = []
            vfd_x_600_responses = None
            if len(device_ids_and_table_name) > 0:
                # print(device_ids_and_table_name)
                for items in device_ids_and_table_name:
                    device_Type = items[5]
                    if device_Type == 'VFD_X_600':
                        devices_table_name = device_ids_and_table_name[0][4]
                        device_result = {'device_id': items[0], 'device_alias': items[2], 'device_feed': None, 'device_serial': items[1], 'device_table_name': devices_table_name, 'device_type': items[5], 'device_order': items[6], 'category_name': items[7]}
                        vfd_x_600_devices.append(device_result)
                    else: # assume controls inc
                        devices_table_name = device_ids_and_table_name[0][3]
                        device_result = {'device_id': items[0], 'device_alias': items[2], 'device_feed': None, 'device_serial': items[1], 'device_table_name': devices_table_name, 'device_type': items[5], 'device_order': items[6], 'category_name': items[7]}
                        controls_inc_devices.append(device_result)
            
            # print(controls_inc_devices)
            # print(vfd_x_600_devices)
            if len(controls_inc_devices) > 0:
                query_device_timescale = QueryDeviceTimescale(None)
                start_time = time.time()
                responses = None
                try:
                    responses = query_device_timescale.run_multiple_devices_query(controls_inc_devices)
                    controls_inc_responses = responses
                    for device_result in controls_inc_devices:
                        # print(device_result)
                        device_serial = device_result['device_serial']
                        # print(responses)
                        for device_feed_item in controls_inc_responses:
                            if device_feed_item['device_id'] == device_serial:
                                device_result['device_feed'] = device_feed_item
                except Exception as e:
                    print("An exception occurred: " + str(e))

            if len(vfd_x_600_devices) > 0:
                query_device_timescale = QueryDeviceTimescale(None)
                start_time = time.time()
                responses = None
                try:
                    responses = query_device_timescale.run_vfd_x_600_multiple_devices_query(vfd_x_600_devices)
                    vfd_x_600_responses = responses
                    for device_result in vfd_x_600_devices:
                        # print(device_result)
                        device_serial = device_result['device_serial']
                        # print(responses)
                        for device_feed_item in vfd_x_600_responses:
                            if device_feed_item['device_id'] == device_serial:
                                device_result['device_feed'] = device_feed_item
                except Exception as e:
                    print("An exception occurred: " + str(e))

                end_time = time.time()
                print("--- %s seconds ---" % (end_time - start_time))
            # for device_result in devices_result:
            #     device_result.pop('device_serial', None)
            #     feed_item = device_result['device_feed']
            #     if feed_item != None:
            #         feed_item.pop('device_id', None)
            overview_fields_controls_inc = ['GPS Latitude', 'GPS Longitude', 'Engine Hours', 'Fuel Rate', 'Key Position', 'Inlet Pressure', 'Control Transducer Level', 'Flow Rate', 'Engine Speed', 'Outlet Pressure 1', 'Battery Voltage', 'Engine Coolant Temp', 'Engine Oil Pressure', 'Fuel Level', 'Amber Warning Lamp', 'Red Stop Lamp', 'Engine Load']
            overview_fields_vfd_x_600 = ['GPS Latitude', 'GPS Longitude', 'Amber Warning Lamp', 'Red Stop Lamp', 'Start/Stop Mode' , 'Auto Mode', 'Motor Hz', 'Inlet Pressure', 'Outlet Pressure', 'Backup Outlet Pressure', 'Flow Rate', 'Flow Total', 'Auto Pressure Set Point', 'High Limit Pressure', 'High Pressure Shutdown', 'Manual Speed', 'Load Percent', 'Backup Power', 'VFD Run Status Verification']
            result = {
                'cx_7500': {
                    'overview_fields' : overview_fields_controls_inc,
                    'data': controls_inc_devices
                },
                'vfd_x_600': {
                    'overview_fields' : overview_fields_vfd_x_600,
                    'data': vfd_x_600_devices
                }
            }
        elif event.get('client_id', False):
            db = SentinelS7Database(None)
            queried_client_id = event.get('client_id', False)
            query = "SELECT id,alias FROM system_view_device_company_device_type_order_category_name where name = '{}'".format(queried_client_id)
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
