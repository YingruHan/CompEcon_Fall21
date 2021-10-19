#!/usr/bin/env python
# coding: utf-8

# # PS5
# ### Ruby Han

# In[2]:


#Housekeeping

import pandas as pd
import numpy as np
import scipy


# In[3]:


#Import the data
raw = pd.read_csv('C:/Users/MSB/Dropbox/fall 2021/Python/class download/CompEcon_Fall21/Matching/radio_merger_data.csv')


# In[4]:


#Inspect the data
raw.describe()


# In[5]:


#Split the data into 2007, 2008
raw7 = raw[raw['year']==2007]
raw8 = raw[raw['year']==2008]


# In[6]:


#split into buyer and target
buy7 = raw7[['buyer_id','buyer_lat','buyer_long','num_stations_buyer','corp_owner_buyer']]
target7 = raw7[['target_id','target_lat','target_long','price','hhi_target','population_target']]
buy8 = raw8[['buyer_id','buyer_lat','buyer_long','num_stations_buyer','corp_owner_buyer']]
target8 = raw8[['target_id','target_lat','target_long','price','hhi_target','population_target']]


# In[7]:


#Permutation to create information for all potential pairs

#first concat the target data frame 45 times for 17 and 54 times for 18
target7 = pd.concat([target7]*45).reset_index(drop=True)
target8 = pd.concat([target8]*54).reset_index(drop=True)

#Then replicate each row of the buyer data, 45 times for 17 and 54 times for 18; concat first then sort
buy7 = pd.concat([buy7]*45).sort_values(by=['buyer_id']).reset_index(drop=True)
buy8 = pd.concat([buy8]*54).sort_values(by=['buyer_id']).reset_index(drop=True)


# In[8]:


#Inspection before concat
target7.describe()
target8.describe()
buy7.describe()
buy8.describe()


# In[9]:


#concat for each year
bt7 = pd.concat([buy7,target7], axis = 1)
bt7.head()
bt8 = pd.concat([buy8, target8,], axis = 1)
bt8.head()


# In[25]:


#Calculate the distance
import geopy

for index, row in bt7.iterrows():
    distance = geopy.distance.geodesic((row['buyer_lat'],row['buyer_long']), (row['target_lat'],row['target_long'])).miles
    bt7.at[index, 'distance'] = distance


# In[26]:


for index, row in bt8.iterrows():
    distance8 = geopy.distance.geodesic((row['buyer_lat'],row['buyer_long']), (row['target_lat'],row['target_long'])).miles
    bt8.at[index, 'distance'] = distance8


# In[27]:


#Combine the two dataframes
bt = bt7.append(bt8, ignore_index = True)


# In[ ]:


#Define the objective function
def MSE(params, data):
    '''
    Args are the bt data and initial guesses
    '''
    alpha, beta=params[0], params[1]
    MSE=0
    
    for index, row in bt.iterrows():
         LHS1= row['num_stations_buyer'] * row['population_target'] + alpha * row['corp_owner_buyer'] * row['population_target'] +  beta * row['Distance'] 
        
        LHS2= row['num_stations_buyer'] * row['population_target'] + alpha * row['corp_owner_buyer'] * row['population_target'] + beta * row['Distance8']
        
        LHS=LHS1 + LHS2
        
        
        RHS1= row['num_stations_buyer'] * row['population_target'] + alpha * row['corp_owner_buyer'] * row['population_target'] + beta * row['Distance8'] 
        
        RHS2= row['num_stations_buyer'] * row['population_target'] + alpha * row['corp_owner_buyer'] * row['population_target'] + beta * row['Distance']
        
        RHS=RHS1 + RHS2
        if LHS >= RHS:
            MSE= MSE + 1
    return(-MSE)


# In[ ]:


#Calling the minimizer
param_guess=(1700, 1700)
results1_NM=minimize(MSE, param_guess,
                 method='Nelder-Mead',
                 args=(bt),
                 options={'disp':True})

