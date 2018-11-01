"""
A module to collect details from users and to return an authorization token for use.
"""
import logging
from urllib import request
import json
import pandas as pd
import yaml

import pickle


#TODO - ADD LOGGING

logger = logging.getLogger(__name__)

api_url = 'https://www.strava.com/api/v3'

def collect_user_details():

    with open('config.yaml') as config:
        user_details = yaml.safe_load(config)

    user_id = str(user_details['user_id'])
    access_token = user_details['token']

    return user_id, access_token


def collect_activities(page, token):

    url_req = request.Request(f'{api_url}/athlete/activities?page={page}&per_page=100',
                              headers={"Authorization":"Bearer " + token},
                              method='GET')

    return request.urlopen(url_req).read()


# TODO mock out request to test for this
def collect_all_user_activities(token: str):

    list_ids = []

    complete = False
    page = 1
    while not complete:

        activities = json.loads(collect_activities(page, token))

        if activities:
            for p in activities:
                if p['type'] == 'Ride':
                    list_ids.append((p['id'], p['name']))
            page += 1
        else:
            complete = True

    return list_ids, token


def collect_activities_streams(activities: list, token: str):

    total_latlong = []

    for num, activity in enumerate(activities):

        still_to_go = len(activities) - num
        logger.info(f'Requesting {activity[1]}, {still_to_go} to go')

        try:
            api_request = request.Request(f'{api_url}/activities/{activity[0]}/streams?keys=latlng&key_by_type=true',
                                          headers={"Authorization":"Bearer " + token},
                                          method='GET')
            response = request.urlopen(api_request)
        except Exception:
            logger.exception(f'Unable to collect {activity[1]}, due to: ')
            continue

        lat_lng_of_ride = pd.Series(json.loads(response.read())['latlng']['data'], name=activity[1]).astype('object')

        total_latlong += [lat_lng_of_ride]

    with open('Data3.pkl', 'wb') as pklfile:
        pickle.dump(total_latlong,  pklfile)

    return 'Success'
