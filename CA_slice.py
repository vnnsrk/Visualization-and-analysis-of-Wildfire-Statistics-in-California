# This code creates a pandas data frame for the given bounding box coordinates and saves the output as a csv file

import sys
import os

project_dir = '/Users/andre/PycharmProjects/ECE180/Final_Project_Git/Visualization-and-analysis-of-Wildfire-Statistics-in-California'
sys.path.append(project_dir)
from Fire_helpers import csv_to_df

# ---
# CA bounding box coords
data_path = 'data/MOD14A1_M_FIRE/'
outdir = './data/MM_CA/'
lat1 =  42.1
lon1 = -124.8
lat2 =  32.6
lon2 = -114.2
for dirpath, dnames, fnames in os.walk("./data/MOD14A1_M_FIRE/"):
    for f in fnames:
        if f.endswith(".csv"):
            df = csv_to_df(os.path.join(dirpath, f), lat1, lon1, lat2, lon2,keepland=True)
            df.to_csv(os.path.join(outdir, f[-16:]))
