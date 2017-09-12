import sys, os, random
import params as PARAM
import boto3



def connectToS3():
	s3 = boto3.resource('s3')
        return s3.Bucket(name=PARAM.BUCKET_NAME)
def getAdsURL(bucket, cible):
    
    prefix="Clients/"+PARAM.CLIENT_ID+"/ads/"+str(cible)+"/"
    url=''
    for obj in bucket.objects.filter(Prefix=prefix):       
       	path, filename = os.path.split(obj.key)
	#print "filename " +filename+"."
       	#print "path " +path+"."
	if(filename != ""):	
       		url="https://s3-eu-west-1.amazonaws.com/"+PARAM.BUCKET_NAME+"/Clients/"+PARAM.CLIENT_ID+"/ads/"+str(cible)+"/"+filename
		return url 
        	
    return "AD NOT FOUND!"

def getLocallyAds(cible):
    if (PARAM.ON_PI):
	local_directory=PARAM.ADS_PI_DIRECTORY
    else:
	local_directory=PARAM.ADS_MAC_DIRECTORY
    files = os.listdir(local_directory+str(cible)+"/")
    index = random.randrange(0, len(files))
    return local_directory+str(cible) +"/" +files[index]
    
