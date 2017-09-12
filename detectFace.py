


import cv2
import sys, time, datetime
import rekognitionApi as api
import s3Api
import displayAd as ad
import params as PARAM

try:
    import picamera
    PARAM.ON_PI=1
    print "picamera found, on PI "                 
except ImportError:
    print "no piCamera so on MAC machine "
    PARAM.ON_PI=0
    

# Get user supplied values
imagePath = sys.argv[1]
#/usr/local/Cellar/opencv3/3.2.0/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml

cascPath = '/usr/local/Cellar/opencv3/3.2.0/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'




def OPEN_CV_STUFF(image_to_treat):
	PARAM.print_withTimeStamp('>>> Begining of OPEN_CV treatment')
	image = cv2.imread(image_to_treat)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


	faces = faceCascade.detectMultiScale(
	    gray,
	    scaleFactor=1.1,
	    minNeighbors=5,
	    minSize=(30, 30),
	    flags = cv2.CASCADE_SCALE_IMAGE
	)

	PARAM.print_withTimeStamp('>>> Begining of OPEN_CV treatment')
	if (len(faces)):
		PARAM.print_withTimeStamp(">>> END of OPEN_CV treatment, Found {0} faces!".format(len(faces)))
	return faces, len(faces)

def AWS_STUFF(image_to_treat):
	
	PARAM.print_withTimeStamp('>>> Begining of AWS treatment')
	if (PARAM.AWS_CONNECT):
		reko = api.connectToRekognitionService()

	if (PARAM.AWS_CONNECT):
		labels = api.detectLabels(reko, image_to_treat, maxLabels=10, minConfidence=70.0)

	if (PARAM.DEBUG) and (PARAM.AWS_CONNECT):
    		PARAM.printLabelsInformation(labels)

	if (PARAM.AWS_CONNECT):
    		faceList = api.detectFaces(reko, image_to_treat)
    		faceCounter = 0




	if (PARAM.AWS_CONNECT):
		for face in faceList:
		        if (PARAM.DEBUG):
           			PARAM.printFaceInformation(face, faceCounter)

        		ad.FaceTreatment(face, faceCounter)
        		faceCounter=faceCounter+1

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
	print "Main image_path_to_display= " + image_path_to_display

	PARAM.print_withTimeStamp('>>> END of AWS treatment')
	ad.ResetCounter()
        return image_path_to_display


def displayAd(image_path_to_display):
	if (PARAM.ON_PI):
     		os.system( "fbi -noverbose " + image_path_to_display)
	else:
     		image_to_display=cv2.imread(image_path_to_display)	
     		for (x, y, w, h) in opencv_faces:
            
            		cv2.imshow("Faces found" ,image_to_display)
            		cv2.waitKey(0)
    		
			cv2.destroyAllWindows()



###########
#START HERE
###########




faceCascade = cv2.CascadeClassifier(cascPath)

if (PARAM.ON_PI==1):
	camera = picamera.PiCamera()
	while True:
		print "IN THE LOOP"
		time.sleep(5)
		camera.capture('image_taken.jpg', resize=(250, 150))
		opencv_faces, opencv_faces_detected=OPEN_CV_STUFF('image_taken.jpg')
		if (opencv_faces_detected>0):
			image_path_to_display=AWS_STUFF('image_taken.jpg')
			displayAd(image_path_to_display)
		else:
			PARAM.print_withTimeStamp('>>> NO FACES DETECT WITH OPEN_CV')
else:
	image_to_treat=imagePath	
	opencv_faces, opencv_faces_detected=OPEN_CV_STUFF(image_to_treat)
	if (opencv_faces_detected>0):
		image_path_to_display=AWS_STUFF(image_to_treat)
		displayAd(image_path_to_display)
	else:
		PARAM.print_withTimeStamp('>>> NO FACES DETECT WITH OPEN_CV')














