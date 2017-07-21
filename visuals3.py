# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 12:27:38 2017

@author: iromanow
"""

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

data = pd.read_csv('Ox_data.csv', encoding='latin-1')

plt.figure(figsize=(16,12))

# main plotting function, set the projection, the center point(lat_0, lon_0) - this must be in the
# plotted area, resolution h, l, the threshold is for how bing a landbody has to be to be plotted
# then set the left lower corner and right upper corner (rem, that lat0, lon0 must be inside)
# only some projections allow for this kind of zooming, here we use mercator
my_map = Basemap(projection='merc', lat_0=40, lon_0=9,
                  resolution = 'h', area_thresh = 100.0,
                  llcrnrlon=-10, llcrnrlat=30,
                  urcrnrlon=40, urcrnrlat=50)

my_map.drawcoastlines()
my_map.drawcountries()
my_map.shadedrelief()# the alternative is bluemarble, etopo, or fillcontinents('color')
#my_map.bluemarble()
my_map.drawmapboundary()

# extra plotted data has to come as lists - this could be pushed in the next line but readability
lons = list(data['loclong'])
lats = list(data['loclat'])

x,y = my_map(lons, lats)
my_map.plot(x, y, 'd', markersize=10, markeredgewidth=0.5, markerfacecolor='gold')
plt.savefig('distribution_prensas.png')
plt.show()
