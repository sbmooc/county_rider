import pandas as pd

from shapely.geometry import Point, Polygon
import matplotlib.pyplot

import pickle
import geopandas

counties = geopandas.read_file('counties.json')

geo_data = pickle.load(open('geo_pickle1.pkl', 'rb'))

completed_rides = set()

for ride in geo_data:
    for _, point in ride.iteritems():
        if _ % 10 != 0:
            continue
        else:
            for row in counties.itertuples():
                try:
                    if point.within(row.geometry):
                        completed_rides.add(row.NAME_2)
                        continue
                except Exception as e:
                    print(e)
                    continue

with open('completed.pkl', 'wb') as com_pickle:
    pickle.dump(completed_rides, com_pickle)


rides = pickle.load(open('geo_pickle1.pkl', 'rb'))

result = pd.concat(rides)

geo_result = geopandas.GeoSeries(result.apply(Point))

counties = geopandas.GeoSeries.from_file('counties.json')

counties_bounds = counties.total_bounds

four_points = [(counties_bounds[0], counties_bounds[1]),
               (counties_bounds[0], counties_bounds[3]),
               (counties_bounds[2], counties_bounds[3]),
               (counties_bounds[2], counties_bounds[1])]

poly = Polygon(p for p in four_points)

poly.crs = {'init': 'espg:4326'}
counties.crs = {'init' :'epsg:4326'}
geo_result.crs = {'init':'epsg:4326'}

geo_result_1 = geo_result.where(geo_result.within(poly))

base = counties.plot(color='white', edgecolor='black')
geo_result_1.plot(ax=base, marker='o', color='red', markersize=1)

matplotlib.pyplot.show()
