import pickle
import geopandas

county_df = geopandas.read_file('counties.json')

strava_series = pickle.load(open('geo_pickle1.pkl', 'rb'))

ride_1 = strava_series[100]

point_1 = ride_1[1]

total_counties = set()

ride_1 = strava_series[2]

completed_rides = set()

for n, ride in enumerate(strava_series):
    print(len(strava_series)-n)
    for _, point in ride.iteritems():
        for row in county_df.itertuples():
            try:
                if point.within(row.geometry):
                    completed_rides.add(row.NAME_2)
                    continue
            except Exception as e:
                print(e)
                continue

with open('completed.pkl', 'wb') as com_pickle:
    pickle.dump(completed_rides, com_pickle)


