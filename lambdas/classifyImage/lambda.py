import json
import sagemaker
import base64
import boto3
from sagemaker.predictor import Predictor
from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
# ENDPOINT = 'udacity-workflow-project-model-monitor-2021-12-31-12-27-32'


def lambda_handler(event, context):
    endpoint = event['endpoint']
    session = sagemaker.Session(boto_session=boto3.Session())

    # Decode the image data
    image = base64.b64decode(event['image_data'])

    # Instantiate a Predictor
    predictor = Predictor(endpoint_name=endpoint, 
                          sagemaker_session=session)


    # For this model the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")
    
    # Make a prediction:
    #inferences = ## TODO: fill in
    inferences = predictor.predict(data=image)
    
    # We return the data back to the Step Function    
    # event["inferences"] = inferences.decode('utf-8')
    event["inferences"] = json.loads(inferences.decode('utf-8'))
    return {
        'statusCode': 200,
        'body': event
    }
