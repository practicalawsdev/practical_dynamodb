#!/usr/bin/env python
# coding: utf-8

# # <span style="color:blue">DynamoDB get_item
# A **get_item** operation **retrieves** a **specific item based on its primary key**.

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
# **For this example we'll see both clients**.

# ### Create a DynamoDB resource client
# The **resource client** will support **more intuitive** requests, with **simpler manipulation of** the **JSON** structures.

# In[ ]:


# Creating the DynamoDB resource Client
ddb = boto3.resource('dynamodb')


# # 3) Use DynamoDB resource client to get an item

# ### Get table resource
# The resource client follows an object-oriented style. So here I use the resource client to get an object that maps to the table specified. I will subsequently make calls on that object.

# In[ ]:


try:
    # get a reference to the tripa table
    trips_table = ddb.Table('travel_planner_trips')
# catch exceptions
except Exception as e:
    print("Error obtaining resource: ", e)


# ## Retrieve specifc trip with a *get*
# A ***get*** operation retrieves a specific item based on its primary key. The primary key can be just the partition key if that's unique, or a combination of the partition key and sort key.
# 
# For the *travel_planner_trips* table, the partition key and sort key are:
# - **Partition key:** *user_id*
# - **Sort key:** *trip_id*
# 
# A **get** will **use** a ***Key*** parameter in the operation to specify the primary key.

# ### Specify data to be retrieved

# In[ ]:


# set variables for the primary key
user_id = "tucker"
trip_id = "2025/07/10_Iceland"


# ### Perform get_item operation

# In[ ]:


try:        
    # get trips matching user_id and trip_id
    db_resp = trips_table.get_item(
        Key={
            'user_id': user_id,
            'trip_id': trip_id
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


# print a summary of the trip item
item = db_resp['Item']
print(f"Locations: {item['locations']}")
print(f"Start date: {item['start_date']}")
print(f"End date: {item['end_date']}")


# # 3) Use DynamoDB service client to get an item

# ### Create a DynamoDB service client
# The **service client** will require a more **verbose code**, manipulating a **more complex DynamoDB specific JSON** data structure. It's primarily **used for advanced operations**, including database transactions.

# In[ ]:


# Creating the DynamoDB service Client
ddb = boto3.client('dynamodb')


# ## Retrieve specifc trip with a *get*
# A ***get*** operation retrieves a specific item based on its primary key. The primary key can be just the partition key if that's unique, or a combination of the partition key and sort key.
# 
# For the *travel_planner_trips* table, the partition key and sort key are:
# - **Partition key:** *user_id*
# - **Sort key:** *trip_id*
# 
# 
# For this example, I'll be filtering on the following:
# - **user id**: *tucker*
# - **trip_id**: *2025/07/10_Iceland*

# In[ ]:


# set variables for the filtering criteria
user_id = "tucker"
trip_id = "2025/07/10_Iceland"

try:        
    # get trips matching user_id and trip_id
    db_resp = ddb.get_item(
        TableName='travel_planner_trips',
        Key={
            'user_id': {'S': user_id},
            'trip_id': {'S': trip_id}
        }
    )

# catch exceptions
except Exception as e:
    print("Error on query: ")
    print(e)


# ### Get data from response object
# Response objects are in JSON format, which in Python will be in a dictionary. We just need to check the format, and extract the data we want from it.
# 
# Note that the response for the service client is a bigger structure. That's because it includes data type designators ("S" for strings, "L" for lists and so on) for each value.

# #### Print the complete response object if we want to visualize it

# In[ ]:


print("Full response:\n",
      json.dumps(db_resp, indent=4))


# #### Extract just the data we want
# We'll still drill down the JSON structure to retrieve specific data, but with the extended JSON structure of the service client that will look a little longer.

# In[ ]:


# iterate through location list structure to create a plain list of locations
locations = []
for loc in db_resp['Item']['locations']['L']:
    locations.append(loc['S'])

# print a summary of the trips locations start date and end date
print(f"Locations: {locations}")
print(f"Start date: {db_resp['Item']['start_date']['S']}")
print(f"End date: {db_resp['Item']['end_date']['S']}")


# In[ ]:




