
# coding: utf-8

# In[16]:


import pandas as pd
import numpy as np


def get_df(csv):
    '''Transforms CSV matrix map into a three column data frame of longitude, latitude, and corresponding value'''
    df = pd.read_csv(csv, header = None)
    longitudes = []
    latitudes = []
    values = []
    
    rxc = df.shape
    for i in range(rxc[0]):
        for j in range(rxc[1]):
            longitudes.append(i)
            latitudes.append(j)
            values.append(df.loc[i,j])
            
    data = pd.DataFrame(np.column_stack([longitudes,latitudes,values]), columns = ['Longitude', 'Latitude', 'Value'])
    return data


# In[20]:




