#!/usr/bin/env python
# coding: utf-8

# # <span style="color:blue">DynamoDB scan
# A ***scan*** operation **retrieves** items **without specifying the partition key**, which forces a **full scan** of the table. **Flexible filtering conditions** can be applied to any attributes.

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


# # 3) Use DynamoDB client to perform a scan

# ### Get table resource
# The resource client follows an object-oriented style. So here I use the resource client to get an object that maps to the table specified. I will subsequently make calls on that object.

# In[ ]:


try:
    # get a reference to the trips table
    trips_table = ddb.Table('travel_planner_trips')
# catch exceptions
except Exception as e:
    print("Error obtaining resource: ", e)


# ## Retrieve trips for a location using *scan*
# A ***scan*** operation retrieves items without specifying the partition key, and supports filtering conditions that can be applied to any attributes. A scan will not perform as well as a query or get, and will utilize more resources since it must scan the entire table. Even if a filter criteria restricts the number of items returned, the scan will still need to examine every item, so RCUs will be consumed for that.
# 
# However, sometimes we must perform scans for special cases. In this example, we will perform a scan for all trips for any users, based on the location (which is not a partition key).
# 
# A **scan** will **use** a ***FilterExpression*** parameter in the operation to specify the filtering criteria.

# ### Specify data to be retrieved

# In[ ]:


# set variables for the filtering criteria
location = "Iceland"


# ### Perform scan operation

# In[ ]:


try:        
    # Perform the scan
    db_resp = trips_table.scan(
        FilterExpression="contains(locations, :location)",
        ExpressionAttributeValues={
            ':location': location
        }
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
    user_id = item['user_id']
    start_date = item['start_date']
    end_date = item['end_date']
    locations = item['locations']

    print(f'User {user_id} - from: {start_date} to {end_date} - {locations}')


# In[ ]:




