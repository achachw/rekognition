import boto3


defaultRegion = 'us-east-1'
defaultUrl = 'https://rekognition.us-east-1.amazonaws.com'

def connectToRekognitionService(regionName=defaultRegion, endpointUrl=defaultUrl):
    return boto3.client('rekognition', region_name=regionName, endpoint_url=endpointUrl)

def detectFaces(rekognition, imageFilename, attributes='ALL'):
    with open(imageFilename, 'rb') as image:
    	resp = rekognition.detect_faces(
            Image ={'Bytes' : image.read()},
            Attributes=[attributes])


    return resp['FaceDetails']

def compareFaces(rekognition, imageBucket, imageSourceFilename, imageTargetFilename):
    resp = rekognition.compare_faces(
            SourceImage = {"S3Object" : {'Bucket' : imageBucket, 'Name' : imageSourceFilename}},
            TargetImage = {"S3Object" : {'Bucket' : imageBucket, 'Name' : imageTargetFilename}})
    return resp['FaceMatches']

def detectLabels(rekognition,  imageFilename, maxLabels=100, minConfidence=0):
    with open(imageFilename, 'rb') as image:
    	resp=rekognition.detect_labels(
        	Image ={'Bytes' : image.read()},
        	MaxLabels = maxLabels, MinConfidence = minConfidence)
    return resp['Labels']
