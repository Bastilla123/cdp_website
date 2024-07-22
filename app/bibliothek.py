import requests
from django.conf import settings

cdp_api_baseurl = settings.CDP_API_BASEURL
cdp_api_username = settings.CDP_API_USERNAME
cdp_api_password = settings.CDP_API_PASSWORD
cdp_businessunit = settings.CDP_BUSINESSUNIT



def execute_request(url,data,expected_status):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }


    response = requests.post(url,


                             data=data,
                             headers = headers)

    response.request.headers["Content-Type"]
    print("Status: {}".format(response.status_code))
    if response.status_code != expected_status:
        print("Response Statuscode {} ist nicht gleich dem erwartetet Statuscode {} Reponse: {}".format(response.status_code,expected_status,response.json()))
#Insert new ingest
def new_ingest(cdp_event,data):

    applicationid =  cdp_event["cdp_applicationid"]
    eventid = cdp_event["cdp_eventid"]
    print("New Ingest URL {} Applicationid {} Eventid {} Event {} Data {} ".format(cdp_api_baseurl,applicationid,eventid,cdp_event, data))
    url = "{}/api/businessunits/{}/applications/{}/dataevents/{}/event".format(cdp_api_baseurl,cdp_businessunit,applicationid,eventid)
    print("Url "+str(url))
    data["userKey"] = cdp_api_username
    data["secret"] = cdp_api_password
    execute_request(url, data,202)