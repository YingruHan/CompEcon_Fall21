#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# This mini-project will serve as a post ad hoc analysis prep for my first year paper. After submitting it to the department, my advisors and I found some potential errors or places for improvement. This assignment is a perfect opportunity for me to check whether our initial findings have some support by visuals. I will explain the potential problems one by one and talk about the findings from each graph.
# 
# Essentially, my first-year paper uses a 4 year panel from 183 food banks to explore the moderators on the negative relationship between number of fundraising employees and each employees' efficiency. We introduced a new measurement, revenue per fundraising employee, as the DV.

# In[1]:


#first import the data and packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

# Read in data from Excel workbook directly
foodbank = pd.read_excel('C:/Users/MSB/Dropbox/Food Bank Research with Ruby/Aggregated Food Bank Data - Market and Tech.xlsx', 
                         header=0)

#Subset data to 2016-2019
foodbank = foodbank[foodbank['Year']>2015]

#look at data
foodbank.head(n=10)


# In[2]:


list(foodbank.columns)


# # Graph 1 - DV and IV
# 
# The current DV is revenue per fundraising employee, and IV is the number of full-time equivalent employees in the development and fundraising department. However, we just realized that this department might to more than raising funds, i.e. they could be responsible for generating revenue from all three identified revenue streams, government support, earned revenue, and private support (which we referred to as fundraising). Therefore, we thought about combining all of the revenues as the output of the department. I would like to check the relationship of between the two new revenue streams and the DV. As a reference, I would also include the original DV on the same plot.

# In[4]:


# Subset a data for this plot

fb_plot1 = foodbank[['Government Support', 'Earned Revenue', 'Total Fundraising Revenue ($)', 
                        'Development/Fund Raising: FTE']]

#Drop those observations with zero dfFTE
fb_plot1 = fb_plot1[fb_plot1['Development/Fund Raising: FTE']>0]

# further cleaning - take out nan's
fb_plot1.dropna(inplace = True)


# In[5]:


#Generate the current DV
fb_plot1['RevperEmp'] = fb_plot1['Total Fundraising Revenue ($)']/fb_plot1['Development/Fund Raising: FTE']

#generate new DVs
fb_plot1['GvtSptperEmp'] = fb_plot1['Government Support']/fb_plot1['Development/Fund Raising: FTE']
fb_plot1['EarnedRevperEmp'] = fb_plot1['Earned Revenue']/fb_plot1['Development/Fund Raising: FTE']


# In[6]:


# scatter plot with fitted lines
columns = ['RevperEmp','GvtSptperEmp','EarnedRevperEmp']
color = ['navy','darkred','darkgreen']

plt.scatter(fb_plot1['Development/Fund Raising: FTE'], fb_plot1['RevperEmp'],alpha = 0.2, color='blue', label="Fundraising")
plt.scatter(fb_plot1['Development/Fund Raising: FTE'], fb_plot1['GvtSptperEmp'],alpha=0.2, color='red', label="Government")
plt.scatter(fb_plot1['Development/Fund Raising: FTE'], fb_plot1['EarnedRevperEmp'], alpha=0.2, color='green', label = "Earned")
for y, i in zip(columns,color):
    plt.plot(np.unique(fb_plot1['Development/Fund Raising: FTE']), 
         np.poly1d(np.polyfit(fb_plot1['Development/Fund Raising: FTE'],
                              fb_plot1[y], 1))(np.unique(fb_plot1['Development/Fund Raising: FTE'])), 
         color=i, linestyle="--", linewidth=2)

plt.ylabel('Revenue')
plt.xlabel('dfFTE')
plt.title('Revenues and dfFTE')
plt.legend()


# The above graph shows that all three DVs have similar trends with the IV of interest, serving as a baseline validation for the intention to combine the three revenue streams as a final DV. The negative trend is slightly more obvious for earned revenue than the other two DVs.

# # Graph 2 - adding a new control variable
# 
# Further exploration of the literatue made us find out that employee turnover is also a factor that can affect the relationship between fundraising revenue per employee and number of employees. Our data base does have employee retention as a type of report. Therefore, in this section, I will first extract this variable from 4 different reports and combine and convert them into a single excel file, then explore this variable's distribution.

# In[7]:


#import the raw data
ret1619 = pd.read_excel('C:/Users/MSB/Dropbox/Food Bank Data/FA Data/Human Resources/Food Bank Staffing/Paid Staff/Employee Retention - FY2019.xlsx', 
                         sheet_name="FB Details", skiprows=5, header=0)
ret1619.head(10)


# In[8]:


list(ret1619.columns)


# In[9]:


#only keep the data that I need
ret1619=ret1619[['Org Id','Employee Retention','Employee Retention.1','Employee Retention.2','Employee Retention.3']]


# In[10]:


#rename the column names so that they indicate year
ret1619 = ret1619.rename(columns={'Employee Retention':'2019','Employee Retention.1': '2018',
                       'Employee Retention.2':"2017",'Employee Retention.3':'2016'})


# In[11]:


list(ret1619.columns)


# In[12]:


# reshape the data to a panel
ret1619 = pd.melt(ret1619, id_vars="Org Id", value_vars=['2016','2017','2018','2019'])
ret1619


# In[13]:


#rename the columns
ret1619 = ret1619.rename(columns={'variable':'Year','value':'Retention'})


# In[14]:


# save it as an excel file so that I can incoporate it into my original excel sheet for later analysis
ret1619.to_excel("employee retention 16-19.xlsx")


# In[15]:


# now explore the distribution of this variable
plt.style.use('ggplot')
sns.histplot(ret1619, x = 'Retention', kde=True)
plt.title('Distribution of Employee Retention Rate 16-19')


# The fact that there are negative retention indicates the possibilty of reporting errors. After going back to the original dataset and manually calculating the retention rates for those foodbank-years with negative retention, I did find such errors. Therefore, I decide to take out these values and replot.

# In[16]:


plt.style.use('ggplot')
sns.histplot(ret1619[ret1619['Retention']>0]['Retention'], kde=True)
plt.title('Distribution of Employee Retention Rate 16-19')


# It seems that I would need to transform this variable when including it into my model. Since it is left-skewed, I may need to use square root transformation.

# # Graph 3 - Food Price and Pounds Distributed

# In this section, I would like to explore the reasons behind food price's moderating role on the relationship b/w DV and IV. Specifically, my analysis has told me that food banks located in a high food price region enjoy a lower reduction in DV. As a post ad hoc analysis, we think that this might result from the fact that food banks in low food price regions do not have much going on. Therefore, I would like to explore the relationship between food price and pounds of food distributed for each year.

# In[17]:


from bokeh.plotting import figure 
from bokeh.io import output_notebook, show
from bokeh.palettes import Spectral4 as palette
from bokeh.transform import factor_cmap

output_notebook()


# In[28]:


# Create a subset of data that I would need for this graph
fb_plot2 = foodbank[['Cost per Meal', 'Pounds Distributed', 'Year']]
fb_plot2 = fb_plot2.astype({'Year':str})
fb_plot2.dtypes


# In[29]:


# First create the lists that I would need in the graph
year = ['2016','2017','2018','2019']
p = figure(title = 'Local Food Price and Pounds Distributed 16-19')
p.xaxis.axis_label = 'Cost per Meal'
p.yaxis.axis_label = 'Pounds Distributed (Annually)'


# In[30]:


p.scatter('Cost per Meal', 'Pounds Distributed', source = fb_plot2, legend_group ='Year', fill_alpha=0.4, size=12,
         color = factor_cmap('Year', 'Spectral4', year))

p.legend.title = "Year"

show(p)


# The above graph demonstrates an overall upward relationship between cost per meal and pounds distributed. Our intuition was correct - food banks located in low food price regions are less active in serving the food insecure population. In addition, as time progresses, dots are moving towards the right, and the dispersion between dots becomes larger. These observations indicate the inflation of food prices as well as the enlarging differences in capabilities among food banks. 
