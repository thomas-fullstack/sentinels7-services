
from ntpath import join
# import requests
import json
from SentinelS7Database import SentinelS7Database
import psycopg2
import psycopg2.extras

table_name= "system_external_cbw_field"

def get_config_from_db(connection,device_id,table_name):
    print("get data from `{table}` table".format(table=table_name))
    #get existing cbw device field
    get_field_query = "SELECT * FROM {table} where device_id={device}"

    cursor = connection.cursor()
    cursor.execute(get_field_query.format(table=table_name,device=device_id))
    result = cursor.fetchall()
    return result


# This is useful to seed the field config
# def add_config_to_db(connection,device_id,table_name):
#     print("insert  field to {table} table".format(table=table_name))

#     aliases = {
#             "digitalIO1": {
#                 "alias":"Float Position",
#                 "unit":["Low","High"],
#                 "order":0,
#                 "type":"bool",
#                 "value":""
#             },
#             "digitalIO2": {
#                 "alias":"Siren/Beacon",
#                 "unit":["Off","On"],
#                 "type":"bool",
#                 "order":1,
#                 "value":""
#             },
#             "analogInput1": {
#                 "alias":"Level 1",
#                 "unit":"ft",
#                 "type":"number",
#                 "order":2,
#                 "value":""
#             },
#             "analogInput2": {
#                 "alias":"Level 2",
#                 "unit":"ft",
#                 "type":"number",
#                 "order":3,
#                 "value":""
#             },
#             "analogInput3":{
#                 "alias":"Pressure",
#                 "unit":"psi",
#                 "type":"number",
#                 "order":4,
#                 "value":""
#             },
#             "analogInput4": {
#                 "alias":"Analog Flow Rate",
#                 "unit":"BPM",
#                 "type":"number",
#                 "order":5,
#                 "value":""
#             },
#             "frequencyInput1" :{
#                 "alias":"Pulse Flow Rate",
#                 "unit":"BPM",
#                 "type":"number",
#                 "order":6,
#                 "value":""
#             },
#             "vin" :{
#                 "alias":"Battery Voltage",
#                 "unit":"Volts",
#                 "type":"number",
#                 "order":7,
#                 "value":""
#             },
#         }



   
#     result = get_config_from_db(connection,device_id,table_name)

#     aliasKeys = list(aliases.keys())
#     cursor = connection.cursor()

#     for row in result:
#         aliasName = row[1]
#         if aliasName in aliases.keys():
#             aliasKeys.remove(aliasName)


#     for key in aliasKeys:
#         data =aliases[key]
#         unit=data['unit']
#         if(isinstance(data['unit'],list)):
#             unit= ','.join(data['unit'])
        
#         query = "INSERT INTO public."+table_name+" (id,field_name, alias, unit,type,"+'"order"'+",device_id) VALUES (nextval('system_external_cbw_field_id_seq'),%s, %s, %s, %s,%s,%s)"
#         values = (key,data['alias'],unit,data['type'],data['order'],device_id)
#         cursor.execute(query, values)

#         print(" Inserted rows successfully!")
#     connection.commit()
#     cursor.close()


def get_data(connection,device_id):
     
    selQ = "SELECT * FROM system_view_external_cbw_device_field_order_category where id='{device}'"

    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(selQ.format(device=device_id))
    result = cursor.fetchall()

    rows = []
    for row in result:
        rows.append(dict(row))

    single = rows[0]
    meta = {
        "category_name":single['category_name'],
        "device_alias":single['alias'],
        "device_feed":{
            "device_id":single['serial_number'],
            "holding_registers":[],
            "published_at":""
        },
        "device_id":single['id'],
        "device_serial":single['serial_number'],
        "device_type":single['device_type'],
        "device_order":single['device_order']

    }

    for dat in rows:
        meta['device_feed']['holding_registers'].append({
            "unit": dat['unit'].split(','),
            "alias": dat['field_alias'],
            "order": dat['field_order'],
            "type":dat['type'],
            "value": "Not Available"})
    
    return meta

def check_device(serial,connection):
     cur = connection.cursor()
     cur.execute("SELECT id FROM system_device WHERE serial_number='{id}'".format(id=serial))
     return cur.fetchone()


def lambda_handler(event, context):
    if 'device_id' not in event:
        return {
            'statusCode': 400,
            'body': "Device id not found"
            }
    db_insert = SentinelS7Database(None)
    connection = db_insert.get_db_connection()

    device_id_param = event['device_id']

    res = check_device(device_id_param,connection)

    if res is None:
        return {
        'statusCode': 404,
        'body': "Device not found"
        }
        
    device_id=res[0]

    # add_config_to_db(connection,device_id,table_name)

    data =  get_data(connection,device_id)

    return data

