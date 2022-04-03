import boto3
from botocore.exceptions import ClientError
import json
import urllib3
from urllib import request, parse
import base64
import os
from SentinelS7Database import SentinelS7Database
from balena import Balena
from datetime import datetime

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
      
def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = 0
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff // 30) + " months ago"
    return str(day_diff // 365) + " years ago"

def query_fleet_status(fleet_name, message_fleet_status_to_numbers):
    balena = Balena()
    BALENA_USERNAME =  os.environ['BALENA_USERNAME']
    BALENA_PASSWORD = os.environ['BALENA_PASSWORD']
    credentials = {'username': BALENA_USERNAME, 'password': BALENA_PASSWORD}
    balena.auth.login(**credentials)
    devices = balena.models.device.get_all_by_application(fleet_name)
    # print(devices)

    fleet_offline_message = ""
    matches = ['just now', 'second', 'minute']
    for device in devices:
        if device['is_online'] == False:
            # print(device['device_name'])
            last_connectivity_event = device['last_connectivity_event']
            # print(last_connectivity_event)
            # 2022-04-01T15: 05: 16.837Z
            datetime_object = datetime.strptime(last_connectivity_event[:-1], '%Y-%m-%dT%H:%M:%S.%f')
            # print(datetime_object)
            # print(pretty_date(datetime_object))
            human_friendly_time_ago = pretty_date(datetime_object)
            if any(x in human_friendly_time_ago for x in matches):
                fleet_offline_message = fleet_offline_message + "{} went offline {} \n".format(device['device_name'],human_friendly_time_ago)
            
    # print(fleet_offline_message)
    # Only send the message if any devices went down in the last hour
    if len(fleet_offline_message) > 0:
        send_sms(message_fleet_status_to_numbers, fleet_offline_message)

def lambda_handler(event, context):
    result = None
    # print("Event:")
    # print(event)
    fleet_status_query= event.get('fleet_status_query', False)
    message_fleet_status_to_numbers=  event.get('message_fleet_status_to_numbers', False)
    fleet_name= event.get('fleet_name', False)
    
    # This is a good way to test Twilio SMS.
    # Dev creds will NOT actually send a message to the phone number but will show "Twilio returned " messages
    # with the details. This should help for local and dev testing
    # send_sms(["Phone number to deliver the text"], "Hey this is a test")

    try:
        if fleet_status_query:
            print("Running fleet_status_query")
            query_fleet_status(fleet_name, message_fleet_status_to_numbers)
            print("Finished Running fleet_status_query")

        result = True

    except (Exception) as error:
        print(error)
        result = error

    # TODO implement
    return {
        'statusCode': 200,
        'body': result
    }


