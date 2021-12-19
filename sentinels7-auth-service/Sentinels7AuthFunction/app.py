import boto3
import hmac
import hashlib
import base64
import os
from boto3.dynamodb.conditions import Key, Attr
from SentinelS7Database import SentinelS7Database

# import requests
USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
S3_CERTS_BUCKET_NAME = os.environ['S3_CERTS_BUCKET_NAME']

client = None
def get_secret_hash(username):
    msg = username + CLIENT_ID
    digest = hmac.new(str(CLIENT_SECRET).encode('utf-8'), msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    dec = base64.b64encode(digest).decode()
    return dec
def initiate_auth(username, password):
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': get_secret_hash(username),
                'PASSWORD': password
            },
            ClientMetadata={
                'username': username,
                'password': password
            })
    except client.exceptions.NotAuthorizedException as e:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotFoundException as e:
        return None, "The username or password is incorrect"
    except Exception as e:
        print(e)
        return None, "Unknown error"
    return resp, None
    
    
def refresh_auth(username, refresh_token):
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token,
                'SECRET_HASH': get_secret_hash(username)
            },
            ClientMetadata={
            })
    except client.exceptions.NotAuthorizedException as e:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotFoundException as e:
        return None, "The username or password is incorrect"
    except Exception as e:
        print(e)
        return None, "Unknown error"
    return resp, None
    
def get_client_name(queried_device_id):
    db = SentinelS7Database(None)
    # print("Device id is: '" + queried_device_id + "'")
    query = "SELECT name FROM system_view_device_company where serial_number = '{}' limit 1".format(queried_device_id)
    # print(query)
    client_id_row = db.get_select_query_all_results(query)
    
    if len(client_id_row) > 0:
        # print("Returning Result: " + result)
        return client_id_row[0][0]
    else:
        result = None

def lambda_handler(event, context):

    global client
    if client == None:
        client = boto3.client('cognito-idp')
    
    # Temporary way returns client_name and cert urls based on device id to the device. This could be more secure 
    if 'device_id' in event:
        device_id = event['device_id']
        device_info = {'client_id': get_client_name(device_id)}
        
        if device_info['client_id'] is not None:
            s3 = boto3.client('s3')
            files = ['iot-certificate.pem', 'iot-private.key', 'root-CA.crt']
            for file in files:
                # Generate the URL to get 'key-name' from 'bucket-name'
                url = s3.generate_presigned_url(
                    ClientMethod='get_object',
                    ExpiresIn=10,
                    Params={
                        'Bucket': S3_CERTS_BUCKET_NAME,
                        'Key': file
                    }
                )
                device_info[file] = url
            return device_info
        return None
    
    if 'username' in event:
        username = event['username']
    else:
        response = {
            'status': 'fail'
        }
        return response
    
    if 'password' in event:
        resp, msg = initiate_auth(username, event['password'])
        
    if 'refresh_token' in event:
        resp, msg = refresh_auth(username, event['refresh_token'])
    if msg != None:
        return {
            'status': 'fail', 
            'msg': msg
        }
    
    response = {
        'status': 'success',
        'id_token': resp['AuthenticationResult']['IdToken']
    }
    
    if 'password' in event:
        response['refresh_token'] = resp['AuthenticationResult']['RefreshToken']
        
    return response