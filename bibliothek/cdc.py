from .own_requests import execute_post_request
from django.conf import settings

from bibliothek import *
import json



def get_last_consent():
    consentlist = get_list_constenstatements()

    returnlist = []
    for key, value in consentlist["preferences"].items():

        if value['isActive'] == True:

            if 'de' in value["langs"]:

                legal = get_legal_statment('de', key)


                lastversion = str(int(legal['legalStatements']['publishedDocVersion']))
                returndict = {'key':key,'lastversion':lastversion,'isMandatory':value['isMandatory']}
                if 'documentUrl' in legal['legalStatements']['versions'][lastversion]:
                    returndict['downloadurl'] = legal['legalStatements']['versions'][lastversion]['documentUrl']

                returnlist.append(returndict)



    return returnlist


def get_legal_statment(language,consentId):

    url = "https://accounts.{}/accounts.getLegalStatements".format(settings.CDC_SERVER)
    data = {

        'lang': language,
        'consentId': consentId,
    }
    response = execute_post_request(url, data, 200)

    return response

def get_list_constenstatements():

    url = "https://accounts.{}/accounts.getConsentsStatements".format(settings.CDC_SERVER)

    return execute_post_request(url)

    #json = insert_full_account()
    #print(json)

    #json = get_list_constenstatements()
    #print(json)

    #json = get_legal_statment('de','newsletter_via_mail')
    #print(json)



def insert_FullAccount(payload):

    url = "https://accounts.eu1.gigya.com/accounts.importFullAccount"


    #print("Payload "+str(payload))
    return execute_post_request(url, payload)


#insert_FullAccount('789101921011111111111','{"firstName":"Sebastian", "lastName":"Jung", "email": "sebastian.jung@intense.de"}','{"terms":{"tos":{"isConsentGranted":true,"actionTimestamp":"2024-08-12T14:24:11.707Z","lastConsentModified":"2024-08-12T14:24:11.707Z","entitlements":[]}}}')

