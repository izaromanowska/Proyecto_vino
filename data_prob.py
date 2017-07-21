# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 14:21:48 2017

@author: iromanow
"""

from __future__ import division
import pandas as pd


# to do: use the column names as values passed in (but make them default), so that they can be user specified. 


def calc_prob(data):
#    get the oldest date, and the youngest date to calculate the range for the dictionary
    minimum = data['date_str_clean'].min().astype(int)
    maximum = data['date_end_clean'].max().astype(int)
    
#    initiate the dictionary
    x = dict.fromkeys(range(minimum, maximum), 0)   
    
#    calculat the 'probability of existence' for any one year = year / range of dates times the number of hornos/prensas (volume)
    data['range'] =  data['Estimated number'] * (1 / (data['date_end_clean'] - data['date_str_clean'] ))
#    print(data['range'])
    
#    drop nans because they fuck with recasting into integers
    data = data.dropna(subset=['date_str_clean'])
    data = data.dropna(subset=['date_end_clean'])
    
#   for each site
    for row in range(len(data['site'])):
#        for each year
        for year in range(data['date_str_clean'].astype(int).iloc[row], data['date_end_clean'].astype(int).iloc[row]):
#           update that year with the probability of that site
            x[year] += data['range'].iloc[row]

#   recast it into a useful data structure
    s = pd.Series(x, name='Probability')
    s.index.name = 'Year'
    s.reset_index()

    return s

