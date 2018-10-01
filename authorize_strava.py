"""
A module to collect details from users and to return an authorization token for use.
"""

from urllib import request
import json
import pandas as pd


def collect_user_details():
    access_token = input('What is your strava access token?')
    user_id = input('What is your user id?')

    return user_id, access_token

def collect_all_user_activities(token: str, user_id: str):

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

    complete_latlng = pd.Series()

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

        lat_long_of_stream = pd.Series(json.loads(response.read())['latlng']['data'], name=activity[1]).astype('object')

        complete_latlng = pd.concat([complete_latlng, lat_long_of_stream], axis=1, ignore_index=True)

    complete_latlng.to_pickle('Data.pkl')

    return 'Success'

