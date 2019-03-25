#!/usr/bin/env python
# coding: utf-8

# For this assignment, you will be required to explore and cluster the neighborhoods in Toronto.
# 
# Start by creating a new Notebook for this assignment. Use the Notebook to build the code to scrape the following Wikipedia page, https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M, in order to obtain the data that is in the table of postal codes and to transform the data into a pandas dataframe like the one shown below:

# import pandas as pd
# import numpy as np
# from bs4 import BeautifulSoup
# import requests

# In[7]:


web_link = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
web_text= requests.get(web_link).text
Canada_data = BeautifulSoup(web_text, 'lxml')


# In[8]:


table_columns = ['Postalcode','Borough','Neighborhood']
toronto = pd.DataFrame(columns = table_columns)
content = Canada_data.find('div', class_='mw-parser-output')
table = content.table.tbody
postcode = 0
borough = 0
neighborhood = 0

for tr in table.find_all('tr'):
    i = 0
    for td in tr.find_all('td'):
        if i == 0:
            postcode = td.text
            i = i + 1
        elif i == 1:
            borough = td.text
            i = i + 1
        elif i == 2: 
            neighborhood = td.text.strip('\n').replace(']','')
    toronto = toronto.append({'Postalcode': postcode,'Borough': borough,'Neighborhood': neighborhood},ignore_index=True)

# Ignore cells with a borough that is Not assigned
toronto = toronto[toronto.Borough!='Not assigned']
toronto = toronto[toronto.Borough!= 0]
toronto.reset_index(drop = True, inplace = True)
i = 0
for i in range(0,toronto.shape[0]):
    if toronto.iloc[i][2] == 'Not assigned':
        toronto.iloc[i][2] = toronto.iloc[i][1]
        i = i+1                               
df = toronto.groupby(['Postalcode','Borough'])['Neighborhood'].apply(', '.join).reset_index()
df.head(10)


# In[9]:


df = df.dropna()
empty = 'Not assigned'
df = df[(df.Postalcode != empty ) & (df.Borough != empty) & (df.Neighborhood != empty)]
df.head(10)


# In[10]:


df.shape


# In[15]:


get_ipython().system('ipython nbconvert toronto_part1.ipynb --to html')


# In[ ]:




