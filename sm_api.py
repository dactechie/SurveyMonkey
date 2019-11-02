
import requests

client = requests.session()

headers = {
    "Authorization": "bearer %s" % "gGjGCiPUvNABVM9Wt5MT1LC12m2ptqvUeMRg8WuJvTBoynF5fZpynFzVRj0JiGZlNjEgvJ4.SIBhle1bXVU3T.UJdtRa5WSLseruHn855ySsBPszhnoVL.2Yu1VBe3zf",
    "Content-Type": "application/json"
}

HOST = "https://api.surveymonkey.net"
BASE_URI =  HOST + "/v3/surveys"

#SURVEY_DETAILS_ENDPOINT = f"/v3/surveys/{survey_id}/details"
#SURVEY_RESPONSE_ENDPOINT = f"/v3/surveys/{survey_id}/responses/{response_id}/details"


def get(resource_string):

  uri = BASE_URI + resource_string
  response = client.get(uri, headers=headers)
  return response.json()


def get_surveyschema_by_name(survey_name):
  resp = get("")
  data_list = resp['data']
  survey = list(filter(lambda item: (item['title'] == survey_name) ,data_list))[0]

  return get_survey_details_schema(survey['id'])


def get_survey_details_schema(survey_id):
  return get(f"/{survey_id}/details")


def get_survey_responses(survey_id, response_id):
  return get(f"/{survey_id}/responses/{response_id}/details")