# this program is for inserting bulk data into the database one by one from the datalist

import requests
import json

# Define the FastAPI endpoint URL
endpoint_url = "http://localhost:8000/add_data"

# Define the data to be inserted in to the database
data_list = [
    {
        "text": "Trouble logging in or accessing the application due to forgotten passwords or account lockouts.",
        "table_name": "issues"
    },
    {
        "text": "Encountering error messages or crashes during usage, leading to frustration and inability to proceed.",
        "table_name": "issues"
    },
    {
        "text": "Billing discrepancies or payment processing issues causing confusion and frustration among users.",
        "table_name": "issues"
    },
    {
        "text": "Difficulty navigating the application or finding specific features, leading to inefficiency and frustration.",
        "table_name": "issues"
    },
    {
        "text": "Seeking assistance with account settings or profile customization, but not finding adequate guidance.",
        "table_name": "issues"
    },
    {
        "text": "Missing or inaccurate information within the application causing confusion or misinformation.",
        "table_name": "issues"
    },
    {
        "text": "Experiencing slow performance or lagging while using the application, leading to frustration and reduced productivity.",
        "table_name": "issues"
    },
    {
        "text": "Facing difficulty integrating the application with other software or platforms, hindering workflow.",
        "table_name": "issues"
    },
    {
        "text": "Encountering compatibility issues with specific devices, browsers, or operating systems, causing inconvenience.",
        "table_name": "issues"
    },
    {
        "text": "Questions about data privacy, security, or compliance, leading to concerns about confidentiality and trust.",
        "table_name": "issues"
    },
    {
        "text": "Seeking clarification on terms of service, privacy policy, or usage agreements to ensure compliance and understanding.",
        "table_name": "issues"
    },
    {
        "text": "Difficulty finding help resources, documentation, or support articles, hindering problem-solving efforts.",
        "table_name": "issues"
    },
    {
        "text": "Encountering language barriers or communication issues while seeking support or assistance.",
        "table_name": "issues"
    },
    {
        "text": "Experiencing unresponsive or slow customer support, leading to frustration and dissatisfaction.",
        "table_name": "issues"
    },
    {
        "text": "Seeking assistance with specific features or functionalities, but not finding adequate guidance or documentation.",
        "table_name": "issues"
    },
    {
        "text": "Frustration due to lack of updates or improvements in the application over time.",
        "table_name": "issues"
    },
    {
        "text": "Difficulty canceling subscriptions or opting out of services, causing inconvenience and frustration.",
        "table_name": "issues"
    },
    {
        "text": "Facing challenges with software updates or installations, hindering usage or access.",
        "table_name": "issues"
    },
    {
        "text": "Encountering unexpected behavior or inconsistencies within the application, causing confusion and frustration.",
        "table_name": "issues"
    },
    {
        "text": "Experiencing performance issues related to network connectivity or internet speed, leading to frustration and reduced productivity.",
        "table_name": "issues"
    },
    {
        "text": "Seeking guidance on best practices or optimal usage of the application, but not finding adequate resources or support.",
        "table_name": "issues"
    },
    {
        "text": "Difficulty recovering lost or deleted data within the application, leading to data loss and frustration.",
        "table_name": "issues"
    },
    {
        "text": "Encountering confusing or unclear user interface elements, hindering navigation and usability.",
        "table_name": "issues"
    },
    {
        "text": "Questions about system requirements or hardware specifications, causing uncertainty about compatibility.",
        "table_name": "issues"
    },
    {
        "text": "Experiencing disruptions or downtime in service availability, causing inconvenience and disruption to workflow.",
        "table_name": "issues"
    },
    {
        "text": "Facing challenges with software performance on specific operating systems or device configurations.",
        "table_name": "issues"
    },
    {
        "text": "Seeking assistance with data migration or transfer between different platforms or applications.",
        "table_name": "issues"
    },
    {
        "text": "Experiencing difficulty in accessing or utilizing premium features or content within the application.",
        "table_name": "issues"
    },
    {
        "text": "Questions about the application's pricing model, subscription plans, or available discounts.",
        "table_name": "issues"
    },
    {
        "text": "Encountering limitations or restrictions in account usage or access, causing frustration and inconvenience.",
        "table_name": "issues"
    }
]



# Function to insert data into the FastAPI endpoint
def insert_data(data):
    try:
        response = requests.post(endpoint_url, json=data)
        if response.status_code == 200:
            print("Data added successfully:", data)
        else:
            print("Error adding data:", response.text)
    except Exception as e:
        print("Exception occurred:", str(e))

# Insert each data entry one by one
for data_entry in data_list:
    insert_data(data_entry)
