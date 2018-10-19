import pickle
import geopandas
import pandas
from shapely.geometry import Point

def collect_pickle(name: str):

    activities = pickle.load(open(name, 'rb'))

    return activities

def geo_code_series(activities):

    geo_list = []

    for activity in activities:

        row_2 = []

        for _, row in activity.iteritems():

            row_2 += [[row[1], row[0]]]

        new_series = pandas.Series(row_2)

        geo_list += [geopandas.GeoSeries(new_series.apply(Point))]

        #geo_list += [geopandas.GeoSeries(activity.apply(Point))]

    return geo_list

# result = collect_pickle('Data3.pkl')

result = geo_code_series(collect_pickle('Data3.pkl'))

with open('geo_pickle1.pkl', 'wb') as geo_pickle:

    pickle.dump(result, geo_pickle)

