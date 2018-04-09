# Author: Yuwen Chang, Yu Chen, Hou Cheng (A.R.G.O.)
# Last Updated: 2018/04/01
##############################
# Code written for ARGO Marketplace Project: Rad Roads
# https://github.com/argo-marketplace/RadRoads
##############################

# initialize
from __future__ import print_function, division
import sys

import numpy as np
import pandas as pd
import pylab as pl

import osmnx as ox
import networkx as nx
import geopandas as gpd

from collections import Counter
from geopy.distance import vincenty
from shapely.geometry import Point

def GetRoads(city, ntype='all_private'):
    """
    Load road network data (shapefile) locally. If not available,
    download the data through OpenStreetMap Nominatim API first.
    
    Parameters
    ----------
    city : string
        The name of the city (or place) of interest.
    ntype : string
        The type of street network to get.
        {'walk', 'bike', 'drive', 'drive_service', 'all', 'all_private'} 
    Returns
    -------
    G_nodes : geopandas.geodataframe.GeoDataFrame
        The GeoDataFrame of the nodes of city road network.
    G_edges : geopandas.geodataframe.GeoDataFrame
        The GeoDataFrame of the edges of city road network.
    Notes
    -----
    If data download is unsuccessful, check query results on
    the Nominatim web page and see if available results exist.
    """
    
    # load road network from local data
    try:
        G_nodes = gpd.read_file("data/" + city + "/nodes/nodes.shp")
        G_edges = gpd.read_file("data/" + city + "/edges/edges.shp")
        print("Existing local data of " + city + " is loaded as shapefiles\n")

    # download from OpenStreetMap if local data is not available
    except:
        # try different query results
        print("Trying to download the network of " + city + " through OSM Nominatim\n")
        n = 1
        while n <= 5:
            try:
                G = ox.graph_from_place(query=city, network_type=ntype, which_result=n)
                break
            except ValueError:
                n += 1
        ox.save_graph_shapefile(G, filename=city, folder=None, encoding='utf-8')
        G_nodes = gpd.read_file("data/" + city + "/nodes/nodes.shp")
        G_edges = gpd.read_file("data/" + city + "/edges/edges.shp")
        print("Data of " + city + " is downloaded, saved, and loaded as shapefiles\n")
    return G_nodes, G_edges;

def RadRoads(city, ntype='all_private', limit=5):
    """
    In a given city (or geographical area) in OSM:
    find the straightest and curviest roads by name;
    find the shortest and longest roads by name.
    
    Parameters
    ----------
    city : string
        The name of the city (or place) of interest.
    ntype : string
        The type of street network to get.
        {'walk', 'bike', 'drive', 'drive_service', 'all', 'all_private'}
    limit : integer
        Number of top records to be listed in each category.
    Returns
    -------
    1. name and length of the shortest roads
        and a dataframe of a top list
    2. name and length of the longest roads
        and a dataframe of a top list
    3. name and sinuosity info of the straightest road
        and a dataframe of a top list
    4. name and sinuosity info of the curviest road
        and a dataframe of a top list
    5. network graph plot of the given city
        with top roads marked with colors
    """

    # load data
    # load road network from local data
    try:
        G_nodes = gpd.read_file("data/" + city + "/nodes/nodes.shp")
        G_edges = gpd.read_file("data/" + city + "/edges/edges.shp")
        print("Existing local data of " + city + " is loaded as shapefiles\n")

    # download from OpenStreetMap if local data is not available
    except:
        # try different query results
        print("Trying to download the network of " + city + " through OSM Nominatim\n")
        n = 1
        while n <= 5:
            try:
                G = ox.graph_from_place(query=city, network_type=ntype, which_result=n)
                break
            except ValueError:
                n += 1
        ox.save_graph_shapefile(G, filename=city, folder=None, encoding='utf-8')
        G_nodes = gpd.read_file("data/" + city + "/nodes/nodes.shp")
        G_edges = gpd.read_file("data/" + city + "/edges/edges.shp")
        print("Data of " + city + " is downloaded, saved, and loaded as shapefiles\n")

    ##################################################################
    # NOTICE: 'length' specified with method call may cause problems #
    ##################################################################

    # combine road segments and aggregate the total lengths
    G_edges['length'] = G_edges['length'].astype('float')
    dict_v = {'length': 'sum', 'highway': 'first', 'oneway': 'first'}
    table = G_edges.groupby('name').agg(dict_v).reset_index()
    
    # remove messy segments w/o names
    table = table[table['name'] != '']
    table.dropna(how='any', inplace=True)

    ### LENGTH ###
    
    # calculate shortest and longest roads
    short = table.sort_values(by='length', ascending=True).head(limit)
    long = table.sort_values(by='length', ascending=False).head(limit)

    # extract road names
    roads = list(G_edges['name'].unique())
    roads.remove('') ### remove messy segements without names ###
    rnames = []
    dist_d = []
    dist_l = []
    sinuosity = []

    ### SINUOSITY ###
    
    # calculate sinuosity for each road
    # create a dataframe containing all the segments of a road for each road
    for i, r in enumerate(roads):
        df_road = G_edges[G_edges['name'] == roads[i]]
        # list all the nodes
        road_nodes = list(df_road['from'].values) + list(df_road['to'].values)
        # count all the nodes
        tdict = dict(Counter(road_nodes))
        tdf = pd.DataFrame(list(tdict.items()), columns=['node', 'count'])
        # select nodes that only occur once (terminals of a road)
        tdf_sub = tdf[tdf['count']==1]

        if len(tdf_sub) != 2:

            continue ### skip roads with more than two terminal nodes for now ###

        else:
            # extract coordinates of the two terminal nodes from the city nodes graph
            G_nodes_term = G_nodes[list(map(lambda n: n in list(tdf_sub['node'].values), list(G_nodes['osmid'])))]
            coord1 = list(G_nodes_term.iloc[0,:]['geometry'].coords)[0]
            coord2 = list(G_nodes_term.iloc[1,:]['geometry'].coords)[0]
            p1 = coord1[1], coord1[0]
            p2 = coord2[1], coord2[0]

            # calculate shortest Distance between two nodes
            d_d = vincenty(p1, p2).meters
            # calculate actual route Length
            d_l = df_road['length'].astype('float', error='coerce').sum()
            # calculate sinuosity
            sinu = d_l / d_d

            # append all values to lists
            rnames.append(r) # road name
            dist_d.append(d_d) # shortest Distance
            dist_l.append(d_l) # actual Length
            sinuosity.append(sinu) #sinuosity

    # create a dataframe with sinuosity data
    df_sinu = pd.DataFrame({'name': rnames,
                            'distance': dist_d,
                            'length': dist_l,
                            'sinuosity': sinuosity})

    # calculate straightest and curviest roads
    straight = df_sinu.sort_values('sinuosity', ascending=True).head(limit)
    curve = df_sinu.sort_values('sinuosity', ascending=False).head(limit)

    straight_0 = straight.iloc[0]
    curve_0 = curve.iloc[0]

    # print out output
    print('Shortest road: {:s} ({:.2f} meters)\n'.format(short.iloc[0]['name'], short.iloc[0]['length']))
    print(short,"\n")
    print('Longest road: {:s} ({:.2f} meters)\n'.format(long.iloc[0]['name'], long.iloc[0]['length']))
    print(long,"\n")
    print('Straightest road: {:s}\nroad dist.: {:.2f}\nshortest dist.: {:.2f}\nsinuosity: {:.5f}\n'.format(
        straight.iloc[0]['name'], straight.iloc[0]['length'], straight.iloc[0]['distance'], straight.iloc[0]['sinuosity']))
    print(straight,"\n")
    print('Curviest road: {:s}\nroad dist.: {:.2f}\nshortest dist.: {:.2f}\nsinuosity: {:.5f}\n'.format(
        curve.iloc[0]['name'], curve.iloc[0]['length'], curve.iloc[0]['distance'], curve.iloc[0]['sinuosity']))
    print(curve,"\n")

    # plot the graph of the area
    fig, ax = pl.subplots(figsize=(10,10))
    G_edges.plot(color='silver', ax=ax)

    G_edges[G_edges['name'] == straight.iloc[0]['name']].plot(color='limegreen', ax=ax, label='straightest')
    G_edges[G_edges['name'] == curve.iloc[0]['name']].plot(color='gold', ax=ax, label='curviest')
    G_edges[G_edges['name'] == short.iloc[0]['name']].plot(color='steelblue', ax=ax, label='shortest')
    G_edges[G_edges['name'] == long.iloc[0]['name']].plot(color='indianred', ax=ax, label='longest')

    pl.legend(fontsize='medium')
    pl.show()

# run RadRoads function
if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print ("Invalid number of arguments. Run as: python radroads.py <city> <road_type>")
        sys.exit()

    RadRoads(sys.argv[1], sys.argv[2], limit=5)
