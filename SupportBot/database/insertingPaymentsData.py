# this program is for inserting bulk data into the database one by one from the datalist

import requests
import json

# Define the FastAPI endpoint URL
endpoint_url = "http://localhost:8000/add_data"

# Define the data to be inserted in to the database
data_list = [
    {
        "text": "1. PLAN-1: Pay-As-You-Go\n₹99..Onwards\n\nAccess to all Tools at your own convenience.\n\nValid per use\nNaver Expires\n20+ Modules\n5 Always Free Modules\nCredit Card Not Required\nNo Frills Attached\nBasic Support",
        "table_name": "pricing"
    },
    {
        "text": "2. PLAN-2: Pro Plan\n₹23,999 /Year\n\nAccess to cutting edge tools for 1 year with flexibility.\n\n5,000 Credits per Month\nValid for 1 Year\n20+ Modules\n5 Always Free Modules\nCredit Card Not Required\nNo Frills Attached\nPriority Support\nDiscounted Top Up Credits",
        "table_name": "pricing"
    },
    {
        "text": "3. PLAN-3: Enterprise\n\nSpecial enterprise pricing with bulk discounts for growth.\n\nVolume Purchase Discounts\nVIP Support for Immediate Assistance\nDedicated Account Manager \nScalability to Grow with Your Business\nTraining and Onboarding Assistance \nFlexible Payment Options",
        "table_name": "pricing"
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
