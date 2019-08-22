import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pylab
import pandas as pd


#read in excel file and set to variables
file1 = pd.read_excel('jess_Ca_vs_Mo.xlsx')
file2 = pd.read_excel('raintest.xlsx')

#fix colums etc
#df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
'''
#arrange the data into an xarray dataset with data information
data1 = xr.Dataset({'A':(['year'], file1['Si_cps'].values),
                   'B':(['year'], file1['Ca_cps'].values)},
                   coords={'year':file1['age_AD'].values},
                   attrs={'File Contents':'XRF Data',
                          'Data Owner':'Conroy',
                          'Time Units':'years',
                          'A':'Si',
                          'B':'Ca'})

data2 = xr.Dataset({'A':(['year'], file1['Mo_value'].values)},
                   coords={'year':file1['Mo_Mean_year'].values},
                   attrs={'File Contents':'Concentration Data',
                          'Data Owner':'Stephan Hlohowskyj',
                          'Time Units':'years',
                          'A':'Mo'})
'''
fig, ax1 = plt.subplots()

ax1.plot(file1['age_AD'], file1['Ca_cps'],color='red')

ax2 = ax1.twinx()

ax2.plot(file1['Mo_Mean_year'], file1['Mo_value'],color='goldenrod')
ax2.set_ylabel('Mo/Ti - composite')
ax1.set_xlabel('years')
ax1.set_ylabel('Ca cps')
plt.show()

fig, ax1 = plt.subplots()

ax1.plot(file1['age_AD'], file1['Si_cps'],color='dodgerblue')
ax2 = ax1.twinx()
ax2.plot(file1['Mo_Mean_year'], file1['Mo_value'],color='goldenrod')
ax2.set_ylabel('Mo/Ti - composite')
ax1.set_xlabel('years')
ax1.set_ylabel('Si cps')
plt.show()
