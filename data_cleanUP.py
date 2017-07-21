# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 10:24:52 2017

@author: iromanow
"""
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from data_prob import calc_prob
plt.style.use('ggplot')

path = "data_updated.xlsx"
sheets=[ "Hornos","Prensas"]
# 'Prensas', 'Hornos'
def clean_data(sheetname):
    
    extras = 0
    data = pd.read_excel(path, sheetname)
    
    # use some reasonable column names
    if sheetname == 'Prensas':
        data.columns = ['site', 'no_prensas', 'Estimated number', 'date_str', 'date_end']
    else:
        data.columns = ['site', 'no_hornos', 'Estimated number', 'date_str', 'date_end']
        extras = 1
    
    def dudoso(dates):
        """ Retain the certainty value but place it in a separate column """
        if "?" in dates:
            return 1
        else:
            return 0
        
    def year0(dates):
        """ Change aC to negative values """
        if 'aC' in dates:
            return '-' + dates
        else:
            return dates
    
    # cast into strings for manipulation    
    data['date_str'] = data['date_str'].astype(str)   
    data['date_end'] = data['date_end'].astype(str) 
    
    # Retain the certainty value but place it in a separate column
    data['fi_dudoso']= data["date_str"].apply(dudoso)
    data['ft_dudoso']= data["date_end"].apply(dudoso)
    
    # Change aC to negative values
    data['date_str'] = data['date_str'].apply(year0)
    data['date_end'] = data['date_end'].apply(year0)
    
    # Strip the dates from all the crap retaining just the number
    data['date_str_clean'] = pd.Series([x.split()[0] for x in data.date_str.dropna()])
    data['date_end_clean'] = pd.Series([x.split()[0] for x in data.date_end.dropna()])
    
    # Clean data - note the '80/70' values and '100-150', I'll make it more robust in the next iteration
    # note the 'float', there can be no 'nan' in an int array
    data['date_str_clean'] = data.date_str_clean.str.replace('?' , '')
    data['date_str_clean'] = data.date_str_clean.replace('' , np.nan)
    if extras:
        data['date_str_clean'] = data.date_str_clean.str.replace('80/50' , '65')
    data['date_str_clean'] = data['date_str_clean'].astype(float) 
    
    data['date_end_clean'] = data.date_end_clean.str.replace('?' , '')
    data['date_end_clean'] = data.date_end_clean.replace('' , np.nan)
    data['date_end_clean'] = data.date_end_clean.str.replace('100-150' , '125')
    data['date_end_clean'] = data['date_end_clean'].astype(float) 
    
    # For now calculate the average dates 
    data['average date'] = (data['date_end_clean'] + data['date_str_clean']) * 0.5
    

    split_by = lambda x: pd.Series([i for i in reversed(x.split('('))])
    if extras:
        place = data['site'].apply(split_by)
        place.columns = ['province','site_name']
        place['province']=place.province.str.replace(')','')
        data = pd.concat([data, place], axis = 1)    

    else:
        place = data['site'].str.split(r'[,(]+', expand = True)
        place.columns = ['site_name', 'district', 'province']
        place['province'] = place['province'].str.replace(')','')
        data = pd.concat([data, place], axis = 1)  

    
    data.to_csv( sheetname + ' clean_data.csv')
    return data

def data_manipulation(data):
    
    # pivot the data for the figure
    data_time = data.groupby('average date')['Estimated number'].mean()
    
    # use the script for cummulative probabilities and graph it
    s = calc_prob(data)
    return s, data_time

def visual_provinces(data,sheet):
    probs = data.groupby(by=data['province']).apply(calc_prob).unstack()
    probs.T.fillna(0).plot(subplots = True, figsize = (10, 25))
    plt.savefig('results' +str(sheet)+'.pdf')

def visual_total( s, data_time, counter, lw):
    if counter:

#        data_time.plot(color = '#9ecae1', linewidth=lw, label = sheets[counter] + ' average date')
        s.plot(color ='#3182bd', linewidth=lw, label = sheets[counter] , figsize = (20, 10))     
        plt.legend()
        plt.savefig('results_whole.pdf')
    else:
#        data_time.plot(color = '#fdd0a2',linewidth=lw, figsize = (20,10), label = sheets[counter]+ ' average date')
        s.plot(color = '#e6550d',linewidth=lw, label = sheets[counter])
        
     

counter = 0
lw = 2

    
for i in sheets:
    data = clean_data(i)
    
    s, data_time  = data_manipulation(data)
    
    
    visual_provinces(data, i)
#    visual_total(s, data_time, counter, lw)
    counter += 1








