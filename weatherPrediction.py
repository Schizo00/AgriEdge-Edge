#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import json
import subprocess
from datetime import datetime


# In[7]:


df = pd.read_csv('weatherTestData.csv')


# In[9]:


# Convert the 'date_column' to datetime type (if it's not already)
df['Date'] = pd.to_datetime(df['Date'])

# Get today's date
today = datetime.now().date()

# Filter the DataFrame to get records for today's date
records_for_today = df[df['Date'].dt.date == today]


# In[15]:


#liveWeatherToday = records_for_today[['WindSpeed3pm', 'Temp', 'Humidity3pm', 'Rainfall']]


# In[20]:


records_for_today.to_csv('liveWeatherToday.csv', index = False)


# In[ ]:

script_name = "weatherPublisher.py"

# Call the second script using subprocess
with open("weatherPublisher.py") as f:
    exec(f.read())


script_name = "temperaturePublisher.py"

# Call the second script using subprocess
with open("temperaturePublisher.py") as f:
    exec(f.read())


script_name = "rainfallPublisher.py"

# Call the second script using subprocess
with open("rainfallPublisher.py") as f:
    exec(f.read())
    

