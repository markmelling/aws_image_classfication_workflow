import json
import os
import boto3

s3 = boto3.resource('s3')  
sns = boto3.client('sns')


if "THRESHOLD" in os.environ:
    THRESHOLD = os.environ["THRESHOLD"]
else:
    THRESHOLD = .80

# SNS_ARN = 'arn:aws:sns:us-east-1:379838984284:ml-workflow-image-classification-failed'
SNS_ARN = os.environ['SNS_ARN']

class Threshold_Error(Exception):
    pass

def lambda_handler(event, context):

    # store event locally
    #with open('/tmp/event.json', 'w') as outfile:
    #    json.dump(event, outfile)

    bucket = event['s3_bucket']
    # Grab the inferences from the event
    inferences = event['inferences']

    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = max(inferences) >= THRESHOLD
   
    image_filename = os.path.basename(event['s3_key'])
    event_filename = image_filename.split('.')[0] + '.json' 

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    # save results to correct folder
    if meets_threshold:
        s3.Bucket(bucket).put_object(Key=f'image_classification_output/{event_filename}', Body=json.dumps(event).encode("utf-8"))
        #s3.Bucket(BUCKET).upload_file('/tmp/event.json',f'image_classification_output/{event_filename}')
        pass
    else:
        s3.Bucket(bucket).put_object(Key=f'image_classification_fail/{event_filename}', Body=json.dumps(event).encode("utf-8"))
        #s3.Bucket(BUCKET).upload_file('/tmp/event.json',f'image_classification_fail/{event_filename}')
        sns.publish(
            TargetArn=SNS_ARN,
            Message=json.dumps(event)
        )
        raise Threshold_Error("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
