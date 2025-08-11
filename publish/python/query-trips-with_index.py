#!/usr/bin/env python
# coding: utf-8

# # <span style="color:blue">DynamoDB query with Index
# A ***query*** operation **retrieves** items with specified **partition key**, and **optional** filtering criteria on the **sort key**. The **partition key** must be an **exact match**, but the **sort key** can have more **flexible comparisons**.
# 
# If the main table partition key is not a match for the query, an index can be used.

# # 1) Import AWS Python SDK (Boto) Package

# In[ ]:


import boto3
from boto3.dynamodb.conditions import Key


# In[ ]:


# import standard library to print nice JSON
import json


# # 2) Create DynamoDB client object
# The Python SDK supports two clients:
# - The low level DynamoDB **service client**
# - The higher level DynamoDB **resource client**
# 
# **For this example I'll be using the resource client**, which makes for simpler looking calls.

# In[ ]:


# Creating the DynamoDB Client
ddb = boto3.resource('dynamodb')


# # 3) Use DynamoDB client to perform query against an index

# ### Get table resource
# The resource client follows an object-oriented style. So here I use the resource client to get an object that maps to the table specified. I will subsequently make calls on that object.

# In[ ]:


try:
    # get a reference to the trips table
    trips_table = ddb.Table('travel_planner_trips')
# catch exceptions
except Exception as e:
    print("Error obtaining resource: ", e)


# ## Retrieve trips between a range with *query* using an index
# A ***query*** operation retrieves items with specified partition key, and optional filtering criteria on the sort key. We want to performa a query for trips in a range of dates, but the start_date is not the sort criteria in the main table. To support an efficient query, we have created the **trips_userid_startdate** global secondary index.
# 
# For the *trips_userid_startdate* index, the partition key and sort key are:
# - **Partition key:** *user_id*
# - **Sort key:** *start_date*
# 
# A **query** will **use** a ***KeyConditionExpression*** in the operation to specify the key based query criteria.

# ### Specify data to be retrieved

# In[ ]:


# set variables for the filtering criteria
user_id = "tucker"
from_date = "2025/07/09"
to_date = "2026/12/31"


# ### Perform query operation

# In[ ]:


try:        
    # Perform the query against the index
    db_resp = trips_table.query(
        IndexName='trips_userid_startdate',
        KeyConditionExpression= (
            Key('user_id').eq(user_id) & 
            Key('start_date').between(from_date, to_date)
        )
    )

# catch exceptions
except Exception as e:
    print("Error on query: ")
    print(e)


# ### Get data from response object
# Response objects are in JSON format, which in Python will be in a dictionary. We just need to check the format, and extract the data we want from it.

# #### Print the complete response object if we want to visualize it

# In[ ]:


print("Full response:\n",
      json.dumps(db_resp, indent=4))


# #### Extract just the data we want

# In[ ]:


# iterate through each item, and print a summary for each
for item in db_resp['Items']:
    start_date = item['start_date']
    end_date = item['end_date']
    locations = item['locations']

    print(f'From: {start_date} to {end_date} - {locations}')


# In[ ]:




