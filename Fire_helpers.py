# ECE 180 project

# Global imports
import urllib2
from StringIO import StringIO
import gzip
import sys
import os
import numpy as np
import pandas as pd
import csv
import itertools
import gmaps

def populate_M_FIRE(yy1,mm1,yy2=2017,mm2=11):
    '''
    This function downloads and unzips monthly Active Fires CSV files from NEO global datasets in
    ftp://neoftp.sci.gsfc.nasa.gov/csv/MOD14A1_M_FIRE/ for a given time interval.
    If only one month-year is given, it downloads data from that month to 11-2017 (Latest available data)

    :param yy1: int, start year
    :param mm1: int, start month
    :param yy2: int, end year
    :param mm2: int, end month
    For example:
    yy1 = 2000
    mm1 = 4
    yy2 = 2000
    mm2 = 6
    populate_M_FIRE(yy1,mm1,yy2,mm2)
    '''
    assert isinstance(yy1, int) and isinstance(mm1, int)
    assert isinstance(yy2, int) and isinstance(mm2, int)
    assert (1 <= mm1 <= 12) and (yy1 >= 2000)
    assert (1 <= mm2 <= 12) and (yy2 >= 2000)

    # Local output directory
    baseURL = 'ftp://neoftp.sci.gsfc.nasa.gov/csv/MOD14A1_M_FIRE/'

    mm = mm1
    yy = yy1
    while yy < yy2 or mm < mm2:
        if mm >= 10:
            fdate = '{}-{}'.format(yy, mm)
        else:
            fdate = '{}-0{}'.format(yy, mm)
        if mm % 12 == 0:
            yy = yy + 1
        mm = mm % 12 + 1

        filename = 'MOD14A1_M_FIRE_' + fdate + '.CSV.gz'
        outFilePath = data_path + 'MOD14A1_M_FIRE_' + fdate + '.csv'

        response = urllib2.urlopen(baseURL + filename)
        compressedFile = StringIO()
        compressedFile.write(response.read())

        # Set the file's current position to the beginning of the file
        # so that gzip.GzipFile can read its contents from the top.
        compressedFile.seek(0)
        decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')

        if not os.path.exists(data_path):
            os.makedirs(data_path)
        with open(outFilePath, 'w') as outfile:
            outfile.write(decompressedFile.read())


def create_global_grid_csv():
    '''
    divides the global degrees (360x180) by the dimensions of the monthly Active Fires CSV files (3600x1800 pixels)
    to determine the geolocation of each element (pixel)
    :return:
    '''
    N_pixels_lon = 3600
    N_pixels_lat = 1800
    delta_lon = 360./N_pixels_lon
    delta_lat = 180./N_pixels_lat
    # create longitude vector
    lon_vec = []
    lon_vec.append(-180)
    for ii in range(N_pixels_lon-1):
        lon_vec.append(lon_vec[ii]+delta_lon)
    # create latitude vector
    lat_vec = []
    lat_vec.append(90)
    for ii in range(N_pixels_lat-1):
        lat_vec.append(lat_vec[ii] - delta_lat)

    return lat_vec, lon_vec


def files_to_dfs():
    '''
    Reads all the csv files from the /data folder and returns a dictionary of the pandas dataframes for each month
    '''
    pds = {}
    for dirpath, dnames, fnames in os.walk("./data/"):
        for f in fnames:
            if f.endswith(".csv"):
                pds[f] = csv_to_df(os.path.join(dirpath, f))
    return pds


def csv_to_df(filename, lat1=90.0, lon1=-180.0, lat2=-90.0, lon2=180.0, keepland=False,keepocean=False):
    '''
    Reads a csv file, converts it to a dataframe of lat-lon-mag columns, filters a particular location coordinate
    and returns the dataframe
    @param filename : string, represents filename
    @param lat1,lat2,lon1,lon2 : float, latitudes and longitudes
    dataframe for points between (lat1,lon1) and (lat2,lon2) are returned
    '''
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        lis = []
        for row in reader:
            lis.extend(map(float, row))

    lat, lon = create_global_grid_csv()
    latlons = [i for i in itertools.product(lat, lon)]

    # 0.1 - represents land, 99999.0 - represents water
    if keepland and keepocean:
        df = pd.DataFrame([x + (y,) for x, y in zip(latlons, lis)],
                          columns=('lat', 'lon', 'mag'))
    elif keepland:
        df = pd.DataFrame([x + (y,) for x, y in zip(latlons, lis) if y not in [99999.0]],
                          columns=('lat', 'lon', 'mag'))
    elif keepocean:
        df = pd.DataFrame([x + (y,) for x, y in zip(latlons, lis) if y not in [0.1]],
                          columns=('lat', 'lon', 'mag'))
    else:
        df = pd.DataFrame([x + (y,) for x, y in zip(latlons, lis) if y not in [0.1, 99999.0]],
                      columns=('lat', 'lon', 'mag'))

    df = df[(df.lat < lat1) & (df.lat > lat2)]
    df = df[(df.lon > lon1) & (df.lon < lon2)]

    return df


def df_to_heatmap(df):
    locations = df[['lat', 'lon']]
    weights = df['mag']
    fig = gmaps.figure()
    fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))

    return fig