import requests
import json
import os

API_URL = "http://localhost:8000/query"  # Adjust the URL to match your FastAPI server
issues_adding_url = "http://localhost:8000/issues_raising"
ADD_RESPONDED_QUERIES_URL = "http://localhost:8000/add_responded_queries"

def send_query(query):
    response = requests.post(API_URL, json={"query": query})
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code}"
    
def raise_ticket(issue):
    response = requests.post(issues_adding_url, json={"issue": issue})
    if response.status_code == 200:
        return response.json().get("message", "Ticket raised successfully")
    else:
        return "Error in raising the ticket"

def main():
    prompts_and_responses = []
    iteration_count = 0

    print("Welcome to our support bot, dedicated to resolving your queries efficiently and effectively. How may I assist you today?\n")

    while True:
        query = input("Enter your query: ")
        response = send_query(query)

        prompts_and_responses.append({"query": query, "response": response})
        print(f"Response: {response}")

        iteration_count += 1

        if (iteration_count % 1 == 0 or iteration_count > 1):
            end_session = input("is the issue resolved? : ").strip().lower()
            if end_session == "yes":
                break
            elif end_session == "no":
                ticket_raise = input("Would you like to submit a ticket? : ").strip().lower()
                if ticket_raise == "yes":
                    issue_description = input("Please describe the issue for the ticket: ")
                    ticket_response = raise_ticket(issue_description)
                    print(ticket_response)
                    
                continue_session = input("Would you prefer to extend our conversation? : ").strip().lower()

                if continue_session == "yes":
                    print("Excellent. How may I assist you further?")
                    continue
                else:
                    break


    # Only store valid queries and responses
    valid_prompts_and_responses = [item for item in prompts_and_responses if "I'm sorry, I'm here to assist with specific topics related to lawyerdesk AI" not in item['response']]

    if valid_prompts_and_responses:
        # Send all valid queries and responses to the new endpoint for storage
        response = requests.post(ADD_RESPONDED_QUERIES_URL, json={"queries_and_responses": valid_prompts_and_responses})
        if response.status_code == 200:
            print("All valid queries and responses have been stored successfully.\n")
        else:
            print(f"Failed to store queries and responses: {response.text}")


    # Save to JSON file in a directory named "outputData"
    # Create the "output" folder if it doesn't exist
    output_folder = "outputData"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the file path for the JSON file inside the "output" folder
    file_path = os.path.join(output_folder, "prompts_and_responses.json")

    # Read existing data from the file if it exists
    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            existing_data = json.load(file)

    # Append new data to the existing data
    existing_data.extend(prompts_and_responses)

    # Write the combined data back to the JSON file
    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)


    print("Session ended. Prompts and responses have been saved to prompts_and_responses.json")

if __name__ == "__main__":
    main()
