#!/usr/bin/env python
# coding: utf-8

# # <span style="color:blue">DynamoDB put_item
# A ***put_item*** operation **inserts or fully replaces** an **item** on a table.

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

# In[ ]:


# Creating the DynamoDB Client
ddb = boto3.resource('dynamodb')


# # 3) Use DynamoDB resource client to put an item

# ### Create a DynamoDB resource client
# The **resource client** will support **more intuitive** requests, with **simpler manipulation of** the **JSON** structures.

# ### Get table resource
# The resource client follows an object-oriented style. So here I use the resource client to get an object that maps to the table specified. I will subsequently make calls on that object.

# In[ ]:


try:
    # get a reference to the trips table
    trips_table = ddb.Table('travel_planner_trips')
# catch exceptions
except Exception as e:
    print("Error obtaining resource: ", e)


# ## Add a new trip for user with a put operation
# A ***put*** operation inserts or fully replaces an item on a table. At a minimum, the put operation **must include** the **partition key, and** a **sort key** (unless a sort key is not used in the table).
# 
# For the *travel_planner_trips* table, the partition key and sort key are:
# - **Partition key:** *user_id*
# - **Sort key:** *trip_id*
# 
# The trip id is created as a combination of the start date and the first location.

# ### Define trip data to be inserted

# In[ ]:


trip_data = {
    "user_id":"lexi",
    "trip_id": "2026/10/17_Vermont",
    "start_date":"2026/10/17",
    "start_time":"5:30pm",
    "end_date":"2026/10/19",
    "end_time":"11:00am",
    "locations":["Vermont"],
}


# ### Perform put_item operation

# In[ ]:


# Insert the data into the table
try:
    # insert the trip
    db_resp = trips_table.put_item(
        Item = trip_data
    )

except ClientError as e:
    print("Error on put: ")
    print(e)


# ### Get data from response object
# Response objects are in JSON format, which in Python will be in a dictionary. We just need to check the format, and extract the data we want from it.

# #### Print the complete response object if we want to visualize it

# In[ ]:


print("Full response:\n",
      json.dumps(db_resp, indent=4))


# # 3) Use DynamoDB service client to put an item

# ### Create a DynamoDB service client
# The **service client** will require a more **verbose code**, manipulating a **more complex DynamoDB specific JSON** data structure. It's primarily **used for advanced operations**, including database transactions.

# In[ ]:


# Creating the DynamoDB service Client
ddb = boto3.client('dynamodb')


# ## Add a new trip for user with a put operation
# A ***put*** operation inserts or fully replaces an item on a table. At a minimum, the put operation **must include** the **partition key, and** a **sort key** (unless a sort key is not used in the table).
# 
# For the *travel_planner_trips* table, the partition key and sort key are:
# - **Partition key:** *user_id*
# - **Sort key:** *trip_id*
# 
# The trip id is created as a combination of the start date and the first location.

# ### Define trip data to be inserted
# When **using** the **service client**, the **JSON structure** needs to **include DynamoDB specific data type specification** for each data field.

# In[ ]:


trip_data = {
    "user_id": {
            "S": "moose"
        },
    "trip_id": {
        "S": "2026/03/17_Portugal"
    },
    "locations": {
        "L": [
            {
                "S": "Portugal"
            }
        ]
    },
    "start_date": {
        "S": "2026/03/17"
    },
    "end_date": {
        "S": "2026/03/22"
    },
    "start_time": {
        "S": "11:00am"
    },
    "end_time": {
        "S": "3:00pm"
    }
}


# ### Perform put_item operation

# In[ ]:


# Insert the data into the table
try:
    # insert the trip using the service client
    db_resp = ddb.put_item(
        TableName='travel_planner_trips',
        Item = trip_data
    )  

except ClientError as e:
    print("Error on put: ")
    print(e)


# ### Get data from response object
# Response objects are in JSON format, which in Python will be in a dictionary. We just need to check the format, and extract the data we want from it.

# #### Print the complete response object if we want to visualize it

# In[ ]:


print("Full response:\n",
      json.dumps(db_resp, indent=4))


# In[ ]:




