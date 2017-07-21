# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 11:53:33 2017

@author: iromanow
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

data = pd.read_csv('1.0_week.csv')

print(data['latitude'][:5], data['longitude'][:5])

plt.figure(figsize=(16,12))

eq_map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
              lat_0=0, lon_0=-130)
eq_map.drawcoastlines()
eq_map.drawcountries()
#eq_map.fillcontinents(color = 'gray')
eq_map.bluemarble()
eq_map.drawmapboundary()
eq_map.drawmeridians(np.arange(0, 360, 30))
eq_map.drawparallels(np.arange(-90, 90, 30))
lons = list(data['longitude'])
lats = list(data['latitude'])
magnitudes = list(data['mag'])

#x,y = eq_map(lons, lats)
#eq_map.plot(x, y, 'ro', markersize=6)
def get_marker_color(magnitude):
    # Returns green for small earthquakes, yellow for moderate
    #  earthquakes, and red for significant earthquakes.
    if magnitude < 3.0:
        return ('go')
    elif magnitude < 5.0:
        return ('yo')
    else:
        return ('ro')

min_marker_size = 2.25
for lon, lat, mag in zip(lons, lats, magnitudes):
    x,y = eq_map(lon, lat)
    msize = mag * min_marker_size
    marker_string = get_marker_color(mag)
    eq_map.plot(x, y, marker_string, markersize=msize)

title_string = "Earthquakes of Magnitude 1.0 or Greater\n"
title_string += "%s through %s" % (str(data['time'].iloc[-1][:10]), str(data['time'].iloc[0][:10]))
plt.title(title_string)


 
plt.show()