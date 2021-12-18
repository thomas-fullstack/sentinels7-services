import boto3
from botocore.exceptions import ClientError
import json
import urllib3
from urllib import request, parse
import base64
import os
from SentinelS7Database import SentinelS7Database

# import requests

def send_ses_email(message_body):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = ""
    
    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT1 = ""
    RECIPIENT2 = ""
    # RECIPIENT3 = ""
    
    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"
    
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"
    
    # The subject line for the email.
    SUBJECT = "Ternstar - SentinelS7 notification"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Ternstar - SentinelS7 notification\r\n" + message_body)
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Amazon SES Test (SDK for Python)</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
          AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """            
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:

        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT1,
                    RECIPIENT2
                ],
            },
            Message={
                'Body': {
                    # 'Html': {
                    #     'Charset': CHARSET,
                    #     'Data': BODY_HTML,
                    # },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def send_sms(sms_numbers, messageBody):
    TWILIO_SMS_URL =  os.environ['TWILIO_SMS_URL']
    TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    
    for sms_number in sms_numbers:
        to_number1 = sms_number
        from_number = os.environ['TWILIO_FROM_NUMBER']
        body = messageBody
    
        if not TWILIO_ACCOUNT_SID:
            return "Unable to access Twilio Account SID."
        elif not TWILIO_AUTH_TOKEN:
            return "Unable to access Twilio Auth Token."
        elif not to_number1:
            return "The function needs a 'To' number in the format +12023351493"
        elif not from_number:
            return "The function needs a 'From' number in the format +19732644156"
        elif not body:
            return "The function needs a 'Body' message to send."
    
        # insert Twilio Account SID into the REST API URL
        populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
        post_params1 = {"To": to_number1, "From": from_number, "Body": body}
        # post_params2 = {"To": to_number2, "From": from_number, "Body": body}
        # post_params3 = {"To": to_number3, "From": from_number, "Body": body}
    
        # encode the parameters for Python's urllib
        data1 = parse.urlencode(post_params1).encode()
        # data2 = parse.urlencode(post_params2).encode()
        # data3 = parse.urlencode(post_params3).encode()
        
        req = request.Request(populated_url)
    
        # add authentication header to request based on Account SID + Auth Token
        authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        base64string = base64.b64encode(authentication.encode('utf-8'))
        req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
    
        try:
            # perform HTTP POST request
            with request.urlopen(req, data1) as f:
                print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
            # with request.urlopen(req, data2) as f:
            #     print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
            # with request.urlopen(req, data3) as f:
            #     print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
        except Exception as e:
            # something went wrong!
            return e
    
def get_feed_data(user_devices_info):
    client = boto3.client('lambda')
    # print("input param to feed")
    # print(user_devices_info)
    encoded_data = json.dumps(user_devices_info).encode('utf-8')
    response = client.invoke(
        FunctionName = os.environ['MAIN_SERVICE_ARN'],
        InvocationType = 'RequestResponse',
        Payload = encoded_data
    )
    
    responseFromChild = json.load(response['Payload'])
    # print("feed response")
    # print(responseFromChild)
    return responseFromChild
    
def get_notification_message(resp_dict):
    emailBody = None
    if resp_dict != None:
        for register in resp_dict['holding_registers']:
            # print(str(register))
            # if register["alias"] == 'Outlet Pressure 1':
            #     print(str(register["alias"]))
            #     print(str(register["value"]))
            # if register["alias"] == 'Outlet Pressure 1' and register["value"] >= 30:
            #     emailBody = "WARNING: "
            #     emailBody += "Outlet Pressure is: " + str(register["value"])
                
            if register["alias"] == 'Red Stop Lamp':
                print(str(register["alias"]))
                print(str(register["value"]))
            if register["alias"] == 'Red Stop Lamp' and register["value"] != 'off':
                emailBody = "WARNING: "
                emailBody += "Red Warning Lamp is: " + str(register["value"])
                emailBody += "\n"
                
            # if register["alias"] == 'Amber Warning Lamp':
            #     print(str(register["alias"]))
            #     print(str(register["value"]))
            # if register["alias"] == 'Amber Warning Lamp' and register["value"] != 'Off':
            #     emailBody += "WARNING: "
            #     emailBody += "Amber Warning Lamp is: " + str(register["value"])
            #     emailBody += "\n"
            
            # if register["alias"] == 'Engine Speed' and register["value"] <= 200:
            #     # print(str(register))
            #     emailBody = "WARNING: "
            #     emailBody += "Engine speed is: " + str(register["value"])
                
            # if register["alias"] == 'Auto Start State' and register["value"] <= 200:
            #     # print(str(register))
            #     emailBody += ", WARNING: "
            #     emailBody += "Auto Start State is: " + str(register["value"])
    return emailBody
    
def get_feed_token(post_param):
    encoded_data = json.dumps(post_param).encode('utf-8')
    http2 = urllib3.PoolManager()
    r2 = http2.request('POST', 'https://zj9ih8yjcj.execute-api.us-east-1.amazonaws.com/sentinels7/oauth/token', headers={'Content-Type': 'application/json'},
             body=encoded_data)
    feed_token = json.loads(r2.data.decode('utf-8'))
    return feed_token['id_token']

def get_device_alarms_notification_status(device_id):
    db = SentinelS7Database(None)
    query = "SELECT * FROM system_view_device_alarm_alias_field_notify where device_id = '{}'".format(device_id)
    device_alarm_alias_field_notify_rows = db.get_select_query_all_results(query)
    # print(device_alarm_alias_field_notify_rows)
    
    alarms_notification_status = []
    for item in device_alarm_alias_field_notify_rows:
        alarms_notification_status.append({
            "notification_status": item[2],
            "alias": item[4],
            "alarm_alias_field_id": item[1]
        })
    return alarms_notification_status
    
def set_notified_last_time_status(device_id, device_alarms_notification_status):
    print("Update these things")
    print(device_id)
    print(device_alarms_notification_status)
    db_update = SentinelS7Database(None)
    db_update_conn = db_update.get_db_connection()
    db_update_cursor = db_update_conn.cursor()
    
    for item in device_alarms_notification_status:
        query = "Update system_device_alarm_notify SET notified = {} where device_id = {} and alarm_alias_field_id = {}".format(item['notification_status'], device_id, item['alarm_alias_field_id'])
        db_update_cursor.execute(query)
        
    db_update_conn.commit()
    db_update_cursor.close()
    db_update_conn.close()
    # dynamo = boto3.resource('dynamodb').Table('sentinels7-clients')
    # response = dynamo.scan()
    # result = None
    # items = response['Items']
    # for item in items:
    #     for device in item['devices']:
    #         if device['alias'] == device_id:
    #             device['alarms_notification_status'] = device_alarms_notification_status
    #             print(item)
    #             dynamo.put_item(Item= item)
    # return result
    
def check_operator(register_value, alarm_expected_value, alarm_operator):
    result = False
    if alarm_operator == '!=' and register_value != alarm_expected_value:
        result = True
    if alarm_operator == '<=' and register_value <= alarm_expected_value:
        result = True
    return result
    
def set_alarm_flags_and_send_notifications(device_id, user_devices_info, sms_numbers, alarm_fields, allFeedData, device_alarms_notification_status):
        # print(device_alarms_notification_status)
    alarm_messages_list = []
    alarm_messages_to_revert = []
    print(alarm_fields)
    if allFeedData != None:
        for register in allFeedData['holding_registers']:
            for field in alarm_fields:
                if register["alias"] == field["alias"]:
                    if check_operator(register["value"], field["expected_value"], field["operator"]):
                        messageBody = "WARNING: \n {} is: {} \n Device Name: {} \n Company Name: {}".format(str(register["alias"]), str(register["value"]), user_devices_info['device_name'], user_devices_info['client_name'])
                        field["message"] = messageBody
                        register_alias = register["alias"]
                        for notification_status in device_alarms_notification_status:
                            if register["alias"] == notification_status["alias"]:
                                field["alarms_notification_status"] = notification_status["notification_status"]
                        alarm_messages_list.append(field)
                    else:
                        for notification_status in device_alarms_notification_status:
                            if register["alias"] == notification_status["alias"]:
                                # revert it back to false as feed is back to normal
                                alarm_messages_to_revert.append(field)
        print("Alert")
        print(alarm_messages_list)
        print("Revert Alert")
        print(alarm_messages_to_revert)
    
    for messages in alarm_messages_list:
        if messages['alarms_notification_status'] == False:
            print("Set notification Status Flag to True")
            for notification_status in device_alarms_notification_status:
                    if messages["alias"] == notification_status["alias"]:
                        notification_status["notification_status"] = True
                        # print("Send Please")
                        send_sms(sms_numbers, messages["message"])
            # print(messages)
        else:
            print("Notification was already sent. No need to send until it happens again.")
            
    for messages in alarm_messages_to_revert:
        for notification_status in device_alarms_notification_status:
                if messages["alias"] == notification_status["alias"]:
                    notification_status["notification_status"] = False
                    
    # print(device_alarms_notification_status)
    set_notified_last_time_status(device_id, device_alarms_notification_status)

def get_device_sms_numbers(device_id):
    db = SentinelS7Database(None)
    query = "SELECT * FROM system_view_device_user_contact where device_id = '{}'".format(device_id)
    device_user_contact_rows = db.get_select_query_all_results(query)
    # print(device_user_contact_rows)
    
    sms_numbers = []
    for item in device_user_contact_rows:
        sms_numbers.append(item[3])
    return sms_numbers

def get_device_alarm_fields(device_id):
    db = SentinelS7Database(None)
    query = "SELECT * FROM system_view_device_company_alarm_field where device_id = '{}'".format(device_id)
    device_company_alarm_field_rows = db.get_select_query_all_results(query)
    # print(device_company_alarm_field_rows)
    
    alarm_fields = []
    for item in device_company_alarm_field_rows:
        alarm_fields.append({
                "expected_value": item[3],
                "alias": item[8],
                "operator": item[4]
            })
    return alarm_fields
    
def lambda_handler(event, context):
    # print("Event:")
    # print(event)
    
    db = SentinelS7Database(None)
    query = "SELECT * FROM system_view_device_company"
    device_company_rows = db.get_select_query_all_results(query)
    # print(device_company_rows)
    
    for item in device_company_rows:
        device_name = item[2]
        device_id = item[0]
        company_name = item[4]
        user_devices_info = {
                'device_name': device_name,
                'client_name': company_name
            }
        alarm_fields = get_device_alarm_fields(device_id)
        if len(alarm_fields) > 0:
            sms_numbers = get_device_sms_numbers(device_id)
            if len(sms_numbers) > 0:
                allFeedData = get_feed_data(user_devices_info)
                if allFeedData != None:
                    print("We are ready")
                    device_alarms_notification_status = get_device_alarms_notification_status(device_id)
                    set_alarm_flags_and_send_notifications(device_id, user_devices_info, sms_numbers, alarm_fields, allFeedData, device_alarms_notification_status)
            
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps("executed successfully")
    }
