


import cv2
import sys, time, datetime
import rekognitionApi as api
import s3Api
import displayAd as ad
import params as PARAM

# Get user supplied values
imagePath = sys.argv[1]
#/usr/local/Cellar/opencv3/3.2.0/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml

cascPath = '/usr/local/Cellar/opencv3/3.2.0/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'







####################################
# OPEN_CV STUFF
####################################
PARAM.print_withTimeStamp('>>> Begining of OPEN_CV treatment')

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

PARAM.print_withTimeStamp(">>> END of OPEN_CV treatment, Found {0} faces!".format(len(faces)))

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
PARAM.print_withTimeStamp('>>> Begining of AWS treatment')



if (PARAM.AWS_CONNECT):
    reko = api.connectToRekognitionService()

if (PARAM.AWS_CONNECT):
    labels = api.detectLabels(reko, imagePath, maxLabels=10, minConfidence=70.0)

if (PARAM.DEBUG) and (PARAM.AWS_CONNECT):
    PARAM.printLabelsInformation(labels)

if (PARAM.AWS_CONNECT):
    faceList = api.detectFaces(reko, imagePath)
    faceCounter = 0




if (PARAM.AWS_CONNECT):
    for face in faceList:
        if (PARAM.DEBUG):
           PARAM.printFaceInformation(face, faceCounter)

        ad.FaceTreatment(face, faceCounter)
        faceCounter=faceCounter+1

####################################
PARAM.print_withTimeStamp('>>> END of AWS treatment')


print ('	*** nbMale ' + str(ad.nbMale) )
print ('	*** nbFemale ' + str(ad.nbFemale) )
print ('	*** nbOld ' + str(ad.nbOld) )
print ('	*** nbYoung ' + str(ad.nbYoung) )
print ('	*** nbChild ' + str(ad.nbChild) )

bucket=s3Api.connectToS3()
cible=ad.definirCible(ad.nbMale, ad.nbFemale, ad.nbOld,ad.nbYoung, ad.nbChild)
#url_to_display=s3Api.getAdsURL(bucket, cible)
image_path_to_display=s3Api.getLocallyAds(cible)


print "Main cible= " + str(cible)
print "Main image_path_to_display= " + PARAM.ADS_DIRECTORY + "/" + image_path_to_display
#print "Main url= " + url_to_display

ad.ResetCounter()








