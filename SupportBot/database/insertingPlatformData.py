# this program is for inserting bulk data into the database one by one from the datalist

import requests
import json

# Define the FastAPI endpoint URL
endpoint_url = "http://localhost:8000/add_data"

# Define the data to be inserted in to the database
data_list = [
    {
        "text": "ADVOCASE:\nFOR ALL LEGAL PROFESSIONALS \nTransforming legal practice with its revolutionary AI, delivering unprecedented insights and analytics, along with advanced document drafting capabilities.",
        "table_name": "platforms"
    },
    {
        "text": "LAWBOOK:\nFOR STUDENTS\nTailored for law students, offering real-time case analysis and study aids to bridge the gap between theory and practice.",
        "table_name": "platforms"
    },
    {
        "text": "PRAJALOK:\nFOR EVERYONE\nTransforming how citizens can navigate the legal system with an Ai app that offers easy access to legal information, guidance, and resources.",
        "table_name": "platforms"
    },
    {
        "text": "CASEWORK:\nFOR LEGAL FIRMS\nAssists lawyers from case inception to completion, with cutting-edge AI to streamline tasks, and enhance productivity.",
        "table_name": "platforms"
    },
    {
        "text": "MOOTCOURT:\nFOR EVERYONE\nAn engaging AI court simulation game app where lawyers can sharpen their skills through realistic case simulations and challenges.",
        "table_name": "platforms"
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
