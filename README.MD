This is a small, offline application to identify the counties that a cyclist has cycled in the UK.

Very much still WIP. 

Currently requires user to manually set up a strava app and get a token, which is used through a config file. 

At the moment it completes by pickling a geoDataFrame of all the counties in which you've had at least one point going through. 

Takes *a long* time to run to completion. 

Requires optimisation:

- Timing and speeding up loops and code. Taking advantage of pandas built in functionality for this
- Not checking every point, but instead checking at a pre-determined interval
- Removing a county and all points associated with it if already been cycled through


Additional work to do: 

- Set up as a web app
- Calculate number of requests required
- Set up to work with worker threads so as not to block or take a long time
- Write a proper readme so other people can use it
