#!/usr/bin/env python
# coding: utf-8

# # Question 1 : Importing the neighbourhood data and creating the data frame
# 

# In[2]:


# installing geocoder
get_ipython().run_line_magic('pip', 'install geocoder')


# In[3]:


# importing  the necessary packages for data importing and cleaning
from bs4 import BeautifulSoup
import requests
import pandas as pd
import geocoder


# In[4]:


# importing url
file = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M").text
# extracting table from imported html code
soup = BeautifulSoup(file,'lxml')
table =soup.find_all('table')[0]
# converting table to pandas dataframe
df = pd.read_html(str(table))[0]
# dropping entries without assigned borough name and assigning neighbourhood names where none are assigned
df = df[df.Borough != 'Not assigned'].sort_values(by='Postcode')
df.reset_index(inplace=True, drop=True)
for i,neigh in enumerate(df.Neighbourhood):
    if neigh == 'Not assigned':
        df.Neighbourhood[i] = df.Borough[i]
        
# adding suffix ', '  to each value in the Neighbourhood column
df['Neighbourhood'] = df['Neighbourhood'] + ', '
# creating  a new dataframe  and populating it with unique postcodes and combined neighbourhood values
df1 = pd.DataFrame()
for code in df.Postcode.unique():
    var = df.loc[df.Postcode == code]
    hood =var.Neighbourhood
    row = var.iloc[0,:]
    row['Neighbourhood'] = "".join(hood)
    df1= df1.append(row)
    # reordering the columns in the new dataframe
columns = ['Postcode' , 'Borough' , 'Neighbourhood']
df1 =df1[columns]

# restting the indeces and removing the old ones
df1.reset_index(inplace=True, drop=True)
# removing the ', ' suffix  from the neighbourhood values that was added for ease of addition
df1.Neighbourhood = df1.Neighbourhood.str.rstrip(', ')
# printing  the resulting dataframe
df1.head(10)


# # Question 2: Adding latitude and longitude data

# In[5]:


# creating empty lists to contain latitude  and longitude data
latitudes = []
longitudes = []
# looping through all postcodes in df1 and finding thier respective lat&long coordinates
for code in df1.Postcode:
    lat_lng_coords = None 
    while (lat_lng_coords is None):
        # geocoder.google did not work, hence using another search agent , arcgis
        g = geocoder.arcgis('{}, Toronto, Ontario'.format(code)) 
        lat_lng_coords = g.latlng
        lat = lat_lng_coords[0]
        lng = lat_lng_coords[1]
    # populating the latitudes and longitudes lists
    latitudes.append(lat)
    longitudes.append(lng)
    
# creating columns in the dataframe containit latitude and longitude coordinates
df1['Latitude'] = latitudes
df1['Longitude'] = longitudes

# viewing the final dataframe
df1.head(10)
    


# # Question 3: Foursquare and neighbourhood clustering

# In[6]:


# inputting foursquare credentials
CLIENT_ID = 'KD1KQGFKVSSP3YYM3OOMLDSKAVCOWQCPYR4IKZVUN3VY2CSS'
CLIENT_SECRET='F5ZTS44MOR2OQ1SPELD1RF3ER52O3HO4VDDVVNTGESN0D5J4'
VERSION = '20180605'


# In[38]:


# defining function  for extracting venue details in the vicinity of a given location
def getNearbyVenues(names, latitudes, longitudes, radius=500, limit=10):
    
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
       # create the API request  URL
 


# In[41]:


import pandas as pd
import numpy as np
import requests

from bs4 import BeautifulSoup


source = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text

soup = BeautifulSoup(source, 'html5lib')

postal_codes_dict = {} # initialize an empty dictionary to save the data in
for table_cell in soup.find_all('td'):
    try:
        postal_code = table_cell.p.b.text # get the postal code
        postal_code_investigate = table_cell.span.text
        neighborhoods_data = table_cell.span.text # get the rest of the data in the cell
        borough = neighborhoods_data.split('(')[0] # get the borough in the cell
        
        # if the cell is not assigned the
        
          # if the cell is not assigned then ignore it
        if neighborhoods_data == 'Not assigned':
            neighborhoods = []
        # else process the data and add it to the dictionary
        else:
            postal_codes_dict[postal_code] = {}
            
            try:
                neighborhoods = neighborhoods_data.split('(')[1]
            
                # remove parantheses from neighborhoods string
                neighborhoods = neighborhoods.replace('(', ' ')
                neighborhoods = neighborhoods.replace(')', ' ')

                neighborhoods_names = neighborhoods.split('/')
                neighborhoods_clean = ', '.join([name.strip() for name in neighborhoods_names])
            except:
                borough = borough.strip('\n')
                neighborhoods_clean = borough
  # add borough and neighborhood to dictionary
            postal_codes_dict[postal_code]['borough'] = borough
            postal_codes_dict[postal_code]['neighborhoods'] = neighborhoods_clean
    except:
        pass
    
# create an empty dataframe
columns = ['PostalCode', 'Borough', 'Neighborhood']
toronto_data = pd.DataFrame(columns=columns)
toronto_data

# populate dataframe with data from dictionary
for ind, postal_code in enumerate(postal_codes_dict):
    borough = postal_codes_dict[postal_code]['borough']
    neighborhood = postal_codes_dict[postal_code]['neighborhoods']
    toronto_data = toronto_data.append({"PostalCode": postal_code, 
                                        "Borough": borough, 
                                        "Neighborhood": neighborhood},
                                        ignore_index=True)
# print number of rows of dataframe
toronto_data.shape[0]


# In[ ]:





# In[ ]:




