import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
sfn_client = boto3.client('stepfunctions')

ENDPOINT_NAME = 'udacity-workflow-project-model-monitor-2022-01-04-22-15-25'

def sf_input(bucket, s3_key):
    return json.dumps({
        "endpoint": ENDPOINT_NAME,
        "image_data": "",
        "s3_bucket": bucket,
        "s3_key": s3_key
    })

def lambda_handler(event, context):
    try:
        for r in event['Records']:
            bucket = r['s3']['bucket']['name']
            s3_key = urllib.parse.unquote_plus(r['s3']['object']['key'], encoding='utf-8')
            #uri = "/".join([bucket, key])
            print('key:', s3_key)
            input = sf_input(bucket,s3_key)
            response = sfn_client.start_execution(stateMachineArn='arn:aws:states:us-east-1:379838984284:stateMachine:MyStateMachine',
                input=json.dumps(input),
            )
            print(response)
  
            return {
              "message": "step function started"
            }
    except Exception as e:
        return {
            "message": e
