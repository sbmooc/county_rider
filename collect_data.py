"""
A module to collect necessary data from Strava.
"""
import json
import logging
from urllib import request

import geopandas
import pandas as pd
from shapely.geometry import Point

#TODO - ADD LOGGING

logger = logging.getLogger(__name__)

api_url = 'https://www.strava.com/api/v3'


def collect_activities(page: int, token: str):

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

    return list_ids


def collect_activities_streams(token: str) -> list:

    activities = collect_all_user_activities(token)

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

        if num > 4:
            break

    return total_latlong


def geo_code_data(activities: list) -> pd.DataFrame:

    geo_list = []

    def _reverse_row(row):

        row.reverse()

    for activity in activities:

        activity.apply(_reverse_row)

        geo_list += [geopandas.GeoSeries(activity.apply(Point))]

    return geo_list

