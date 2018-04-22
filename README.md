# RadRoads
Using OSMnx to find Rad Roads in any city!
![RadRoads](https://github.com/argo-marketplace/RadStreets/blob/master/cover-photo.jpg)

You may import [radroads.py](https://github.com/argo-marketplace/RadRoads/blob/master/notebooks/radroads.py) as functions into your Jupyter Notebooks, as shown in this [demo](https://github.com/argo-marketplace/RadRoads/blob/master/notebooks/demo_radroads.ipynb). Or, manually download radroads.py and use it as a script. Simply put the geographical area of interest as an argument.

# Usage:

```
- git clone https://github.com/argo-marketplace/RadRoads.git

- Check requirements.txt for required packages.

- python radroads.py "City, State" "network_type"

- python radroads.py "Brooklyn, NY" "all"
```

Refer http://nominatim.openstreetmap.org/ for correct City,State syntax.

network_type values via [OSMnx](https://github.com/gboeing/osmnx):

- `drive` - get drivable public streets (but not service roads)
- `drive_service` - get drivable streets, including service roads
- `walk` - get all streets and paths that pedestrians can use (this network type ignores one-way directionality)
- `bike` - get all streets and paths that cyclists can use
- `all` - download all non-private OSM streets and paths
- `all_private` - download all OSM streets and paths, including private-access ones


Rad Roads will return
```
Top 5 roads on each list:
1. Shortest
2. Longest
3. Straightest
4. Curviest
And a graph plot with the top 1 being colorized.
```


## Why

Roads, everybody loves complaining about them - very few actually study them. Here is one way to uncover insights and have fun!

## What
*Open Street Map - Network* or **OSMnx** is an incredible Python package that lets you study your city's streets in new and interesting ways, programmatically.

This project aims to create a few explore fun network based statistics that can be applied on a given city's street network. In this project, we will focus on New York City, Los Angeles, and Boulder's Streets.

For any given city, you can use OSMnx to calculate:

- What is the the longest, contiguous road?
- What is the shortest road?
- What is the curviest road? [**Check out Lombard Street in San Francisco**](https://www.openstreetmap.org/way/402111597)
- What is the straightest road? (Great for cities to plan Autonomous vehicle pilots)
- The road with the most intersections.
- Other rad stats!? You tell us!

## How (Resources)

- **Add your rad stat to the notebooks folder!**
- [Introduction and examples](http://geoffboeing.com/2016/11/osmnx-python-street-networks/)
- [Example notebooks to get you started](https://github.com/gboeing/osmnx-examples/tree/master/notebooks)
- [Network Statistics on Streets](http://osmnx.readthedocs.io/en/stable/osmnx.html?highlight=basic_stats#module-osmnx.stats)
- Former CUSP student and Street Data Warrior Princess, [Manushi Majumdar's](https://www.linkedin.com/in/manushimajumdar/) explorations
   - https://github.com/ManushiM/street101/blob/master/streets101_lion_osmnx.ipynb
   - https://github.com/ManushiM/CartoCamp_Workshops/blob/master/Workshop1_April2017/CartoCamp_OSMnx.ipynb

# Next Steps

1. Review [Geo-Street-Talk-Global](https://github.com/Streets-Data-Collaborative/geo-street-talk-global)
    - Does the ReadMe provide enough information for you to get started?
    - Is the code well commented?
    - Can any sections of code be cleaned up or made more modular?
    - What extensions can you think of to make the project more useful?

2. Introduce improvements
    - ~~Use Sinuosity as a measure instead of Circuity. [geopandas implementation](https://github.com/Geosyntec/gisutils/blob/a4034d5dfed472588548306860d010b3dd99a980/gisutils/algo.py)~~
    - Apply filters for results (e.g., longest, shortest)
    - ~~Merge a single RadRoads() function that shows the following for each input city with :~~
        - ~~Longest Segment [Red]~~
        - ~~Shortest Segment [Blue]~~
        - ~~Straightest Segment [Green]~~
        - ~~Most Sinusoisal segment aka Curviest [Yellow]~~
    - [Index based on Name and From-To Nodes](https://www.openstreetmap.org/way/260042856#map=17/40.01316/-105.28674&layers=D): OSM contains `Node` information for every `Way` and this can be used to identify, spatially, the street segments.
    - [Colorize street types](http://geoffboeing.com/2016/11/osmnx-python-street-networks/)
    - Insert Google map interactive window

3. Polish notebooks and fix in-notebook issues

4. ~~Blog post on current results~~

5. Think in the [larger context](https://github.com/Streets-Data-Collaborative/Autonomous_Transportation_Analyzer) and plan for the next

6. Other things to ponder:
    - How to utilize this characteristics to evaluate ride/walk/street quality, preparedness of AV of a city, etc.?
    - Create a profile for road network characteristics that can be compared worldwide. Maybe a regional view is more meaningful than identifying a single street (longest, straightest)?
    - Other examples: identifying straightest roads between two points can be used to ask "which city has the straightest connections between CBD and populated residential areas?"

7. Random notes:
    - The longest and shortest street may turn out to be highways: filtering; avoid 'Motorway' in our outcome?
    - Group by names: may combine two different streets with same name: verify whether all segments of a road is connected; segs of a same road shares the same OSMid?; add new street index besides street name: OSM nodes from, OSM nodes to. i.e: Street name OSM nodes from-OSM nodes to
    - Shp file does not have the double edges (length doubled for two-way roads) problem?
    - Other attributes that might be good to look into: direction, width?
