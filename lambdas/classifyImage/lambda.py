import json
import base64
import boto3
# from sagemaker.predictor import Predictor
# from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
# ENDPOINT = 'udacity-workflow-project-model-monitor-2021-12-31-12-27-32'
runtime = boto3.Session().client("sagemaker-runtime")


def lambda_handler(event, context):
    endpoint = event['endpoint']

    # NOTE As an alternative to using sagemake boto3 can
    # be used instead - this means that sagemake doesn't need
    # to be included in the lambda zip

    # session = sagemaker.Session(boto_session=boto3.Session())
    # # Instantiate a Predictor
    # predictor = Predictor(endpoint_name=endpoint, 
    #                       sagemaker_session=session)
    # For this model the IdentitySerializer needs to be "image/png"
    # predictor.serializer = IdentitySerializer("image/png")
    # # Make a prediction:
    # inferences = predictor.predict(data=image)
    # event["inferences"] = json.loads(inferences.decode('utf-8'))
    
    # Decode the image data
    image = base64.b64decode(event['image_data'])
    response = runtime.invoke_endpoint(
        EndpointName=endpoint,
        ContentType="image/png",
        Accept="image/png",
        Body=image,
    )
    result = json.loads(response['Body'].read().decode())
    event["inferences"] = result

    return {
        'statusCode': 200,
        'body': event
    }
