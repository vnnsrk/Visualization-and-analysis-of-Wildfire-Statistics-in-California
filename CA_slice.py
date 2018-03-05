# This code creates a pandas data frame for the given bounding box coordinates and saves the output as a csv file

import sys
import os

project_dir = '/Users/andre/PycharmProjects/ECE180/Final_Project_Git/Visualization-and-analysis-of-Wildfire-Statistics-in-California'
os.chdir(project_dir)
sys.path.append(project_dir)
from Fire_helpers import csv_to_df

# ---
data_path = './data/MOD14A1_M_FIRE/'
outdir = './data/MM_CA/'
outdir_keepall = './data/MM_CA_keep_landocean/'
# CA bounding box coords
lat1 =  42.1
lon1 = -124.8
lat2 =  32.6
lon2 = -114.2

for dirpath, dnames, fnames in os.walk(data_path):
    for f in fnames:
        if f.endswith(".csv"):
            print 'processing: ' + os.path.join(dirpath, f)
            df = csv_to_df(os.path.join(dirpath, f), lat1, lon1, lat2, lon2,keepland=True)
            df_keepall = csv_to_df(os.path.join(dirpath, f), lat1, lon1, lat2, lon2, keepland=True, keepocean=True)

            df.to_csv(os.path.join(outdir, f[-16:]))
            df_keepall.to_csv(os.path.join(outdir_keepall, f[-16:]))
            print f[-16:] + ' Done!'