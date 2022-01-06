import json
import os
import boto3

s3 = boto3.resource('s3')  
sns = boto3.client('sns')


THRESHOLD = .93
BUCKET = 'project-ml-workflow'
SNS_ARN = 'arn:aws:sns:us-east-1:379838984284:ml-workflow-image-classification-failed'

def lambda_handler(event, context):
    
    # store event locally
    #with open('/tmp/event.json', 'w') as outfile:
    #    json.dump(event, outfile)

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
        s3.Bucket(BUCKET).put_object(Key=f'image_classification_output/{event_filename}', Body=json.dumps(event).encode("utf-8"))
        #s3.Bucket(BUCKET).upload_file('/tmp/event.json',f'image_classification_output/{event_filename}')
        pass
    else:
        s3.Bucket(BUCKET).put_object(Key=f'image_classification_fail/{event_filename}', Body=json.dumps(event).encode("utf-8"))
        #s3.Bucket(BUCKET).upload_file('/tmp/event.json',f'image_classification_fail/{event_filename}')
        sns.publish(
            TargetArn=SNS_ARN,
            Message=json.dumps(event)
        )
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
