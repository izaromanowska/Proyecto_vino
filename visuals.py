# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 12:43:41 2017

@author: iromanow
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


#data = pd.DataFrame(np.random.rand(10,3), columns = ['flakes','tools','handaxes'])
#data.plot(kind = 'barh', stacked = True)
#plt.savefig('pretty_graph.png')

my_map = Basemap(projection='merc', lat_0=57, lon_0=-135,
                  resolution = 'h', area_thresh = 0.1,
                  llcrnrlon=-136.25, llcrnrlat=56,
                  urcrnrlon=-134.25, urcrnrlat=57.75)

 
my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color='coral')
my_map.drawmapboundary()

lon = -135.3318
lat = 57.0799
x,y = my_map(lon, lat)
my_map.plot(x, y, 'bo', markersize=12)

lons = [-135.3318, -134.8331, -134.6572]
lats = [57.0799, 57.0894, 56.2399]
x,y = my_map(lons, lats)
my_map.plot(x, y, 'bo', markersize=10)

labels = ['Sitka', 'Baranof Warm Springs', 'Port Alexander']
for label, xpt, ypt in zip(labels, x, y):
    plt.text(xpt+10000, ypt+5000, label)

 
my_map.drawmeridians(np.arange(0, 360, 30))
my_map.drawparallels(np.arange(-90, 90, 30))

plt.show()
