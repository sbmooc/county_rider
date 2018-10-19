"""
A module to collect details from users and to return an authorization token for use.
"""

from urllib import request
import json
import pandas as pd
import yaml

import pickle


def collect_user_details():

    with open('config.yaml') as config:
        user_details = yaml.safe_load(config)

    user_id = str(user_details['user_id'])
    access_token = user_details['token']

    return user_id, access_token

def collect_all_user_activities(user_id: str, token: str):

    number_activities_request = request.Request(f'https://www.strava.com/api/v3/athletes/{user_id}/stats',
                                  headers={"Authorization":"Bearer " + token},
                                  method='GET')

    number_activities = json.loads(request.urlopen(number_activities_request).read())['all_ride_totals']['count']

    number_of_pages_required = (number_activities // 100) + 2

    list_ids = []

    # TODO Should add in a while loop here to avoid additional request. Keep requesting data until json.loads is empty.

    for page in range(1, number_of_pages_required):

        activity_request = request.Request(f'https://www.strava.com/api/v3/athlete/activities?page={page}&per_page=100',
                                      headers={"Authorization":"Bearer " + token},
                                      method='GET')

        all_activities = request.urlopen(activity_request)

        for p in json.loads(all_activities.read()):
            if p['type'] == 'Ride':
                list_ids.append((p['id'], p['name']))

    return list_ids, token

def collect_activities_streams(activities: list, token: str):

    complete_latlng = []

    for num, activity in enumerate(activities):

        still_to_go = len(activities) - num
        print(f'requesting {activity[1]}')
        print(f'just {still_to_go} to go')

        try:
            api_request = request.Request(f'https://www.strava.com/api/v3/activities/{activity[0]}/streams?keys=latlng&key_by_type=true',
                                          headers={"Authorization":"Bearer " + token},
                                          method='GET')
            response = request.urlopen(api_request)
        except Exception:
            print(Exception)
            continue

        lat_lng_of_ride = pd.Series(json.loads(response.read())['latlng']['data'], name=activity[1]).astype('object')

        complete_latlng += [lat_lng_of_ride]

        #complete_latlng = pd.concat([complete_latlng, lat_long_of_stream], axis=1, ignore_index=True)

    with open('Data3.pkl', 'wb') as pklfile:
        pickle.dump(complete_latlng, pklfile)

    #complete_latlng.to_pickle('Data.pkl')

    return 'Success'

details = collect_user_details()
activities = collect_all_user_activities(*details)
collect_activities_streams(*activities)

