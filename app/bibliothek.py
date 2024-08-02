import requests
from django.conf import settings
import logging
from .models import Log


cdp_api_baseurl = settings.CDP_API_BASEURL
cdp_api_username = settings.CDP_API_USERNAME
cdp_api_password = settings.CDP_API_PASSWORD
cdp_businessunit = settings.CDP_BUSINESSUNIT

def log(loglevel,text):
    Log(loglevel = loglevel, text = text).save()

def execute_request(url,data,expected_status):

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    log('i','Execute_request Post url {} data {} headers {}'.format(url, data, headers))

    response = requests.post(url,


                             data=data,
                             headers = headers)
    log('i','Execute_request Response Statuscode {} Json {}'.format(response.status_code,response.json()))

    response.request.headers["Content-Type"]

    if response.status_code != expected_status:

        log('e',"Response Statuscode {} ist nicht gleich dem erwartetet Statuscode {} Reponse: {}".format(response.status_code,expected_status,response.json()))

#Insert new ingest
def new_ingest(cdp_event,data):

    applicationid =  cdp_event["cdp_applicationid"]
    eventid = cdp_event["cdp_eventid"]

    url = "{}/api/businessunits/{}/applications/{}/dataevents/{}/event".format(cdp_api_baseurl,cdp_businessunit,applicationid,eventid)

    data["userKey"] = cdp_api_username
    data["secret"] = cdp_api_password
    execute_request(url, data,202)