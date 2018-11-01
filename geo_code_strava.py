import pickle
import geopandas
from shapely.geometry import Point


def collect_pickle(name: str):

    activities = pickle.load(open(name, 'rb'))

    return activities


def geo_code_data(activities):

    geo_list = []

    def _reverse_row(row):

        row.reverse()

    for activity in activities:

        activity.apply(_reverse_row)

        geo_list += [geopandas.GeoSeries(activity.apply(Point))]

    return geo_list


result = geo_code_data(collect_pickle('Data3.pkl'))

with open('geo_pickle1.pkl', 'wb') as geo_pickle:

    pickle.dump(result, geo_pickle)

