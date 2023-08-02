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


liveWeatherToday = records_for_today[['WindSpeed3pm', 'Temp', 'Humidity3pm', 'Rainfall']]


# In[20]:


liveWeatherToday.to_csv('liveWeatherToday.csv', index = False)


# In[ ]:

print('1')
script_name = "weatherPublisher.py"

# Call the second script using subprocess
try:
    completed_process = subprocess.run(["python", script_name], capture_output=True)
    print(completed_process.stdout)    
except subprocess.CalledProcessError as e:
    print('error')

