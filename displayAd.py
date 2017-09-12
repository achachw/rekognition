import sys, os
import params as PARAM
import boto3





if PARAM.TEST_MODE==0:
    nbMale = nbFemale = nbOld = nbYoung = nbChild = 0
else:
    nbMale = 0
    nbFemale = 3
    nbOld = 3
    nbYoung = 0
    nbChild = 0

def ResetCounter():
    global nbMale 
    global nbFemale 
    global nbOld
    global nbYoung
    global nbChild
    nbMale = nbFemale = nbOld = nbYoung = nbChild = 0


def FaceTreatment(face, faceCounter):
    global nbMale, nbFemale, nbOld, nbYoung, nbChild


    if (face['Gender']['Value']=="Male"):
       nbMale=nbMale+1
    if (face['Gender']['Value']=="Female"):
       nbFemale=nbFemale+1

    if (face['AgeRange']['Low'] > 45) and (face['AgeRange']['High'] > 60 )  :
            nbOld=nbOld+1
    if (face['AgeRange']['Low'] > 18) and (face['AgeRange']['High'] < 55):
       nbYoung=nbYoung+1
    if (face['AgeRange']['High'] < 19):
       nbChild=nbChild+1


    
def definirCible(nbMale, nbFemale, nbOld, nbYoung, nbChild):
#homme seul
    if (nbMale):
        if(nbFemale==0)and(nbOld==0)and(nbYoung==1)and(nbChild==0):
            return PARAM.HOMME_JEUNE_SEUL
	if(nbFemale==0)and(nbOld==1)and(nbYoung==0)and(nbChild==0):
	    return PARAM.HOMME_SENIOR_SEUL
	if(nbFemale==0)and(nbOld==0)and(nbYoung==0)and(nbChild==1):
	    return PARAM.HOMME_ENFANT_SEUL
#hommes seulement
    if (nbMale>1):
        if(nbFemale==0)and(nbOld==0)and(nbYoung>1)and(nbChild==0):
            return PARAM.DEUX_HOMMES_JEUNES_OU_PLUS
	elif(nbFemale==0)and(nbOld>1)and(nbYoung==0)and(nbChild==0):
	    return PARAM.DEUX_HOMMES_SENIORS_OU_PLUS
	elif(nbFemale==0)and(nbOld==0)and(nbYoung==0)and(nbChild>1):
	    return PARAM.DEUX_HOMMES_ENFANTS_OU_PLUS
        elif(nbFemale==0):
            return PARAM.DEUX_HOMMES_OU_PLUS
#femme seul
    if (nbFemale):
        if(nbMale==0)and(nbOld==0)and(nbYoung==1)and(nbChild==0):
            return PARAM.FEMME_JEUNE_SEULE
	if(nbMale==0)and(nbOld==1)and(nbYoung==0)and(nbChild==0):
	    return PARAM.FEMME_SENIOR_SEULE
	if(nbMale==0)and(nbOld==0)and(nbYoung==0)and(nbChild==1):
	    return PARAM.FEMME_ENFANT_SEULE  

#femmes seulement
    if (nbFemale>1):
        if(nbMale==0)and(nbOld==0)and(nbYoung>1)and(nbChild==0):
            return PARAM.DEUX_FEMMES_JEUNES_OU_PLUS
	elif(nbMale==0)and(nbOld>1)and(nbYoung==0)and(nbChild==0):
	    return PARAM.DEUX_FEMMES_SENIORS_OU_PLUS
	elif(nbMale==0)and(nbOld==0)and(nbYoung==0)and(nbChild>1):
	    return PARAM.DEUX_FEMMES_ENFANTS_OU_PLUS
        elif(nbMale==0):
            return PARAM.DEUX_FEMMES_OU_PLUS

#couple jeune
    if (nbFemale==1)and(nbMale==1)and(nbChild==2):
        return PARAM.COUPLE_ENFANT

#couple jeune
    if (nbFemale==1)and(nbMale==1)and(nbYoung==2):
        return PARAM.COUPLE_JEUNE
#couple seniors
    if (nbFemale==1)and(nbMale==1)and(nbOld==2):
        return PARAM.COUPLE_SENIOR

#famille avec enfants
    if (nbFemale>=1)and(nbMale>=1)and(nbChild>=1):
        return PARAM.FAMILLE_AVEC_ENFANT


