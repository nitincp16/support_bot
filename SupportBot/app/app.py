import requests
import json
import os
import streamlit as st

# API endpoints (adjust to match your FastAPI server)
API_URL = "http://localhost:8000/query"
issues_adding_url = "http://localhost:8000/issues_raising"
ADD_RESPONDED_QUERIES_URL = "http://localhost:8000/add_responded_queries"

# Function to send a query
def send_query(query):
    response = requests.post(API_URL, json={"query": query})
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code}"

# Function to raise a ticket
def raise_ticket(issue):
    response = requests.post(issues_adding_url, json={"issue": issue})
    if response.status_code == 200:
        return response.json().get("message", "Ticket raised successfully")
    else:
        return "Error in raising the ticket"
    
# Save valid queries and responses to JSON
def save_data(prompts_and_responses):
    valid_prompts_and_responses = [
        item for item in prompts_and_responses 
        if "I'm sorry" not in item['response']
    ]

    if valid_prompts_and_responses:
        response = requests.post(ADD_RESPONDED_QUERIES_URL, json={"queries_and_responses": valid_prompts_and_responses})
        if response.status_code == 200:
            st.write("All valid queries and responses have been stored successfully.")
        else:
            st.write(f"Failed to store queries and responses: {response.text}")
    
    # Save to JSON in 'outputData' directory
    output_folder = "outputData"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_path = os.path.join(output_folder, "prompts_and_responses.json")

    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            existing_data = json.load(file)

    existing_data.extend(prompts_and_responses)
    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)

    st.write("Session saved to prompts_and_responses.json")

# Main Streamlit UI
st.title("Support Bot 🤖")
st.write("Welcome to our support bot. How may I assist you today?")

# CSS styling for chat output and input boxes, with new background animation
st.markdown(""" 
<style>
    /* Apply a darker background with smooth gradient animations */
    body, html, .stApp {
        height: 100%;
        background: radial-gradient(circle at top left, #304a17, #000000, #633a01);
        background-size: 200% 200%;
        animation: gradientShift 8s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Ensure Streamlit containers are transparent */
    .stApp {
        background-color: transparent;
    }

    .output-box {
        background-color: rgba(128, 128, 128, 0.2);  /* Translucent gray */
        padding: 10px;
        border-radius: 8px;
        margin-top: 10px;
        max-width: 700px;
        word-wrap: break-word;
        color: white;
    }

    .user-query {
        color: #ffbb00;  /* Highlighted color for user queries */
        font-weight: bold;
    }
</style>

""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'prompts_and_responses' not in st.session_state:
    st.session_state['prompts_and_responses'] = []
if 'iteration_count' not in st.session_state:
    st.session_state['iteration_count'] = 0

# Input box for new query
query = st.text_input("Enter your query")

# Add loading spinner while processing the query
if query:
    with st.spinner("Bot is thinking..."):
        response = send_query(query)
        st.session_state['prompts_and_responses'].append({"query": query, "response": response})
        st.session_state['iteration_count'] += 1

        for chat in st.session_state['prompts_and_responses']:
            st.markdown(f'<div class="output-box"><span class="user-query">You:</span> {chat["query"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box"><span>Bot:</span> {chat["response"]}</div>', unsafe_allow_html=True)

# Ask if the issue is resolved after the first query
if st.session_state['iteration_count'] > 2:
    resolved = st.radio("Is the issue resolved?", ("No", "Yes"))
    
    if resolved == "No":
        ticket_raise = st.radio("Would you like to submit a ticket?", ("No", "Yes"))
        
        if ticket_raise == "Yes":
            issue_description = st.text_input("Describe the issue for the ticket")
            if st.button("Raise Ticket"):
                ticket_response = raise_ticket(issue_description)
                st.write(ticket_response)
                st.stop()

extend_session = ""

if st.session_state['iteration_count'] > 1:    
    # Set default to "Yes" for extending conversation, and close conversation if switched to "No"
    extend_session = st.radio("Would you prefer to extend our conversation?", ("Yes", "No"), index=0)
    
if extend_session == "No":
    st.write("Thank you for using the support bot! Have a great day! 😊")
    save_data(st.session_state['prompts_and_responses'])
    st.stop()
