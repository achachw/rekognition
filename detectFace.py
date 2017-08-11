


import cv2
import sys, time, datetime
import rekognitionApi as api

# Get user supplied values
imagePath = sys.argv[1]
#/usr/local/Cellar/opencv3/3.2.0/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml

cascPath = '/usr/local/Cellar/opencv3/3.2.0/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'
def print_withTimeStamp(toPrint):
    ts = datetime.datetime.utcnow()
    print (toPrint + ' >> at ' + str(ts))


####################################
# OPEN_CV STUFF
####################################
print_withTimeStamp('Begining of OPEN_CV treatment')

# 1. Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)
test = faceCascade.load(cascPath)


# 2. Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 3. Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.CASCADE_SCALE_IMAGE
)

print_withTimeStamp("((OPEN_CV)) Found {0} faces!".format(len(faces)))

####################################
# DEBUG, DRAW, ...
####################################
# Draw a rectangle around the faces
#for (x, y, w, h) in faces:
#    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
#cv2.imshow("Faces found" ,image)
#cv2.waitKey(0)



####################################
# AWS STUFF
####################################
print_withTimeStamp('Begining of AWS treatment')

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



reko = api.connectToRekognitionService()

labels = api.detectLabels(reko, imagePath, maxLabels=10, minConfidence=70.0)

printLabelsInformation(labels)

faceList = api.detectFaces(reko, imagePath)
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









