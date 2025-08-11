#!/usr/bin/env python
# coding: utf-8

# # <span style="color:blue">DynamoDB update_item
# An ***update_item*** operation **updates attributes** of an **existing item**.

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


# # 3) Use DynamoDB client to perform a query

# ### Get table resource
# The resource client follows an object-oriented style. So here I use the resource client to get an object that maps to the table specified. I will subsequently make calls on that object.

# In[ ]:


try:
    # get a reference to the trips table
    trips_table = ddb.Table('travel_planner_trips')
# catch exceptions
except Exception as e:
    print("Error obtaining resource: ", e)


# ## Update a trip to add an itinerary
# An **update** operation updates an attribute on an item.
# 
# For the *travel_planner_trips* table, the partition key and sort key are:
# - **Partition key:** *user_id*
# - **Sort key:** *trip_id*
# 
# An **update** will **use** a ***Key*** parameter in the operation to specify the primary key for the item being updated.

# ### Specify trip to be updated

# In[ ]:


# set variables for the primary key
user_id = "lexi"
trip_id = "2026/10/17_Vermont"


# ### Specify trip data to be update

# In[ ]:


# itinerary to be added
itinerary = [
    {
        "date": "2026/10/17",
        "from_time": "17:30",
        "to_time": "19:00",
        "title": "Dinner at The Skinny Pancake",
        "location": "Burlington",
        "description": "Enjoy a delicious dinner at this popular Vermont pancake restaurant."
    },
    {
        "date": "2026/10/18",
        "from_time": "09:00",
        "to_time": "17:00",
        "title": "Hike at Mount Philo State Park",
        "location": "Charlotte",
        "description": "Explore the scenic trails of Mount Philo, offering breathtaking views of Lake Champlain."
    },
    {
        "date": "2026/10/19",
        "from_time": "09:00",
        "to_time": "11:00",
        "title": "Hike at Smugglers' Notch Resort",
        "location": "Jeffersonville",
        "description": "Take a morning hike through the beautiful trails at Smugglers' Notch before heading home."
    }
]


# ### Perform update_item operation

# In[ ]:


try:
    # Update an item in the table
    db_resp = trips_table.update_item(
        # Define the primary key of the item to update
        Key={
            "user_id": user_id,
            "trip_id": trip_id
        },
        # Define the update expression
        UpdateExpression="SET itinerary = :itinerary",
        # Define the expression attribute values
        ExpressionAttributeValues={
            ":itinerary": itinerary
        }
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




