import requests
from django.conf import settings


cdc_apikey = settings.CDC_APIKEY
cdc_secret = settings.CDC_SECRET
cdc_userkey = settings.CDC_USERKEY
def log(text):
    print("Text {}".format(text))

def execute_get_request(url):

    #log('Execute_request Get url {}'.format(url))

    response = requests.post(url,


                             data=data,
                             headers = headers)
    #log('Execute_request Response Statuscode {} Json {}'.format(response.status_code,response.json()))

    response.request.headers["Content-Type"]


    return True

def execute_post_request(url,data = {},expected_status = 200):

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    print("Data {} url {}".format(data,url))

    data.update({
            'ApiKey': cdc_apikey,
            'userKey': cdc_userkey,
            'secret': cdc_secret})

    response = requests.post(url,


                             data=data, headers=headers)


    jsonresponsedata = response.json()



    if jsonresponsedata['statusCode'] != expected_status:

        raise Exception("Response Statuscode {} ist nicht gleich dem erwartetet Statuscode {} Reponse: {}".format(jsonresponsedata['statusCode'],expected_status,response.json()))
        #log("Response Statuscode {} ist nicht gleich dem erwartetet Statuscode {} Reponse: {}".format(json['statusCode'],expected_status,response.json()))
        #exit
    return jsonresponsedata
