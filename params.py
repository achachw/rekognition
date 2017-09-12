import sys, time, datetime

TEST_MODE=1
DEBUG=1
AWS_CONNECT=0
ON_PI=0


CLIENT_ID="X"
BUCKET_NAME="achachw-ads"

HOMME_ENFANT_SEUL=1
HOMME_JEUNE_SEUL=10
HOMME_SENIOR_SEUL=100

DEUX_HOMMES_JEUNES_OU_PLUS=2
DEUX_HOMMES_SENIORS_OU_PLUS=20
DEUX_HOMMES_ENFANTS_OU_PLUS=200
DEUX_HOMMES_OU_PLUS=2000

FEMME_ENFANT_SEULE=3
FEMME_JEUNE_SEULE=30
FEMME_SENIOR_SEULE=300


DEUX_FEMMES_JEUNES_OU_PLUS=4
DEUX_FEMMES_SENIORS_OU_PLUS=40
DEUX_FEMMES_ENFANTS_OU_PLUS=400
DEUX_FEMMES_OU_PLUS=4000



COUPLE_ENFANT=5
COUPLE_JEUNE=50
COUPLE_SENIOR=500

FAMILLE_AVEC_ENFANT=6
MIXTE=7

ADS_MAC_DIRECTORY="/Users/wachach/Documents/CISCO/AWS/TheScript/rekognition/ads/"
ADS_PI_DIRECTORY="/home/pi/ads/"

def print_withTimeStamp(toPrint):
    ts = datetime.datetime.utcnow()
    print (toPrint + ' >> at ' + str(ts))

def printLabelsInformation(labels):
    for l in labels:
        print('		Label ' + l['Name'] + ', confidence: ' + str(l['Confidence']))

def printFaceInformation(face, faceCounter):
    print('		*** Face ' + str(faceCounter) + ' detected, confidence: ')+str(face['Confidence'])
    print('		Gender: ')+face['Gender']['Value']
    # You need boto3>=1.4.4 for AgeRange
    print('		Age: ')+str(face['AgeRange']['Low'])+"-"+str(face['AgeRange']['High'])
    if (face['Beard']['Value']):
        print ('	Beard')
    if (face['Mustache']['Value']):
        print ('	Mustache')
    if (face['Eyeglasses']['Value']):
        print ('	Eyeglasses')
    if (face['Sunglasses']['Value']):
        print ('	Sunglasses')
    for e in face['Emotions']:
        print e['Type']+'	'+str(e['Confidence'])

