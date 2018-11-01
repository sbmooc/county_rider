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


