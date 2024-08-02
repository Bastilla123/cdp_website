import requests
from django.conf import settings
import logging
from .models import Log
logging.basicConfig(filename='api.log', format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

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

    logging.info('Execute_request Post url {} data {} headers {}'.format(url, data, headers))
    response = requests.post(url,


                             data=data,
                             headers = headers)
    logging.info('Execute_request Response Statuscode {} Test {}'.format(response.status_code,response.json()))
    response.request.headers["Content-Type"]

    if response.status_code != expected_status:
        logging.exception('Execute_request Response Error Statuscode {} Test {}'.format(response.status_code, response.json()))
        print("Response Statuscode {} ist nicht gleich dem erwartetet Statuscode {} Reponse: {}".format(response.status_code,expected_status,response.json()))
#Insert new ingest
def new_ingest(cdp_event,data):

    applicationid =  cdp_event["cdp_applicationid"]
    eventid = cdp_event["cdp_eventid"]
    print("New Ingest URL {} Applicationid {} Eventid {} Event {} Data {} ".format(cdp_api_baseurl,applicationid,eventid,cdp_event, data))
    url = "{}/api/businessunits/{}/applications/{}/dataevents/{}/event".format(cdp_api_baseurl,cdp_businessunit,applicationid,eventid)

    data["userKey"] = cdp_api_username
    data["secret"] = cdp_api_password
    execute_request(url, data,202)