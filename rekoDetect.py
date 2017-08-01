import sys
import rekognitionApi as api




def usage():
    print('\nrekognitionDetect <image> \n')
    print('image         : the image to process')
    print('         labels & face information (stdout)\n')

def printLabelsInformation(labels):
    for l in labels:
        print('Label ' + l['Name'] + ', confidence: ' + str(l['Confidence']))

def printFaceInformation(face, faceCounter):
    print('	*** Face ' + str(faceCounter) + ' detected, confidence: ')+str(face['Confidence'])
    print('Gender: ')+face['Gender']['Value']
    # You need boto3>=1.4.4 for AgeRange
    print('Age: ')+str(face['AgeRange']['Low'])+"-"+str(face['AgeRange']['High'])
    if (face['Beard']['Value']):
        print ('Beard')
    if (face['Mustache']['Value']):
        print ('Mustache')
    if (face['Eyeglasses']['Value']):
        print ('Eyeglasses')
    if (face['Sunglasses']['Value']):
        print ('Sunglasses')
    for e in face['Emotions']:
        print e['Type']+' '+str(e['Confidence'])

image       = str(sys.argv[1])

reko = api.connectToRekognitionService()

labels = api.detectLabels(reko, image, maxLabels=10, minConfidence=70.0)

printLabelsInformation(labels)

faceList = api.detectFaces(reko, image)
faceCounter = 0
for face in faceList:
    printFaceInformation(face, faceCounter)
    faceCounter=faceCounter+1


if (faceCounter == 0):
    message = "No face has been detected, sorry"
else:
    if (faceCounter == 1):
        message = "A single face has been detected"
    else:
        message = str(faceCounter)+ " faces have been detected"

labelText = ''
for l in labels:
    if (l['Confidence'] > 80.0):
        labelText = labelText + l['Name'] + ", "



