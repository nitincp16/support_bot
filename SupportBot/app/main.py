from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import json
import faiss
import numpy as np
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import logging
import requests

# Load environment variables
os.environ.pop('OPENAI_API_KEY', None)
load_dotenv(override=True)

# Initialize FastAPI app
app = FastAPI()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# OpenAI API key
client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

# Request models for input data (this will be displayed in the execute part of the fastapi endpoint)
class RequestedData(BaseModel):
    text: str
    table_name: str

class DataRequest(BaseModel):
    text: str
    table_name: str
    use_steps: str
    youtube_link: str

class QueryRequest(BaseModel):
    query: str

class IssueRequest(BaseModel):
    issue: str

class RespondedQueryRequest(BaseModel):
    queries_and_responses: List[Dict[str, str]]

class UpdateIssueRequest(BaseModel):
    issue_id: int
    reason: str
    solution: str

# latest embedding format
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

# Helper function to generate response using GPT-4o-mini
def generate_response(query: str, similar_data: list, conversation_history: List[Dict[str, str]]) -> str:
    # Construct prompt with previous queries and responses
    prompt = "previous queries:\n\n"
    for interaction in conversation_history:
        prompt += f"User: {interaction['query']}\nBot: {interaction['response']}\n\n"

    # Add current query and similar data to prompt
    prompt += "current data : \n\n"
    prompt += f"User's query: {query}\nSimilar data:\n"
    for i, data in enumerate(similar_data, 1):
        prompt += f"{i}. {data}\n"
    prompt += "\n\nBased on the above information, provide a response to the user query."

    # Generate response using GPT-3.5 Turbo
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[ 
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

def query_similarity(query1, query2):
    # Implement a function to check similarity between two queries
    # This can be as simple as string matching or as complex as embedding similarity
    # For example, you can use the same embedding technique and a cosine similarity threshold
    try:
        embedding1 = get_embedding(query1)
        embedding2 = get_embedding(query2)
        similarity = cosine_similarity(embedding1, embedding2)
        return similarity > 0.9  # Adjust the threshold as needed
    except Exception as e:
        logger.error(f"Error in query similarity: {str(e)}")
        return False



# Define the root endpoint "/"
@app.get("/")
async def root():
    return {"message": "Welcome to the homepage of SupportBot!!!"}

# Add data endpoint
@app.post("/add_data")
async def add_data(requested_data: RequestedData):
    text = requested_data.text
    table_name = requested_data.table_name
    try:
        # Get the embedding
        embedding = get_embedding(text)
        encoded_data = json.dumps(embedding)

        # Get the current maximum ID in the specified table
        max_id_response = supabase.table(table_name).select('id').order('id', desc=True).limit(1).execute()
        if max_id_response.data:
            max_id = max_id_response.data[0]['id']
            new_id = max_id + 1
        else:
            new_id = 1  # Table is empty, start with ID 1

        # Insert data into Supabase with the new ID
        response = supabase.table(table_name).insert({
            'id': new_id,
            'data': text,
            'encoded_data': encoded_data
        }).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Error inserting data into Supabase")

        return {"message": "Data added successfully", "data_id": response.data[0]['id']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Add modules data endpoint
@app.post("/add_modules_data")
async def add_data(data_request: DataRequest):
    text = "data : " + data_request.text + " steps : " + data_request.use_steps + " youtube_link : " + data_request.youtube_link
    try:
        # Get the embedding
        embedding = get_embedding(text)
        encoded_data = json.dumps(embedding)

        # Get the current maximum ID in the modulesdata table
        max_id_response = supabase.table('modulesdata').select('id').order('id', desc=True).limit(1).execute()
        if max_id_response.data:
            max_id = max_id_response.data[0]['id']
            new_id = max_id + 1
        else:
            new_id = 1  # Table is empty, start with ID 1

        # Insert data into Supabase with the new ID
        response = supabase.table('modulesdata').insert({
            'id': new_id,
            'data': data_request.text,
            'use_steps': data_request.use_steps,
            'youtube_link': data_request.youtube_link,
            'encoded_data': encoded_data
        }).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Error inserting data into Supabase")

        return {"message": "Data added successfully", "data_id": response.data[0]['id']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Query similar data endpoint
@app.post("/query")
async def query(query_request: QueryRequest):
    query = query_request.query
    try:
        # Keywords related to lawyerdesk AI topics
        keywords = ["law", "legal", "agreement", "contract", "court", "plan", "purchasing", "pricing", "link", "case", "terms", "conditions", "pricing", "modules", "module", "platforms", "jobs"]
        if not any(keyword in query.lower() for keyword in keywords):
            return {
                "response": "I'm sorry, I'm here to assist with specific topics related to lawyerdesk AI. Is there something else I can help you with?"
            }

        # Check if the query is similar to previously asked queries
        try:
            responded_queries = supabase.table('respondedqueries').select('*').execute()
        except Exception as e:
            logger.error(f"Error fetching data from respondedqueries table: {str(e)}")
            raise HTTPException(status_code=500, detail="Error fetching data from respondedqueries table")

        for row in responded_queries.data:
            if query_similarity(query, row['query']):  # Implement this function to compare similarity
                return {"response": row['response']}

        # Get the embedding of the query
        try:
            query_embedding = get_embedding(query)
        except Exception as e:
            logger.error(f"Error getting embedding for query: {str(e)}")
            raise HTTPException(status_code=500, detail="Error getting embedding for query")

        # List of tables to consider
        tables = ['modulesdata', 'platforms', 'pricing', 'jobs', 'termsandconditions']
        data = []

        # Fetch data from each table
        for table in tables:
            try:
                response = supabase.table(table).select('*').execute()
            except Exception as e:
                logger.error(f"Error fetching data from {table} table: {str(e)}")
                continue

            if response.data:
                for row in response.data:
                    data.append({
                        'table': table,
                        'data': row['data'],
                        'encoded_data': row['encoded_data']
                    })

        if not data:
            raise HTTPException(status_code=500, detail="Error fetching data from Supabase")

        # Extract embeddings and convert to numpy array
        try:
            embeddings = [json.loads(row['encoded_data']) for row in data]
            embeddings_np = np.array(embeddings).astype('float32')
        except Exception as e:
            logger.error(f"Error processing embeddings: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing embeddings")

        # Initialize FAISS index
        try:
            dimension = len(query_embedding)
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings_np)
        except Exception as e:
            logger.error(f"Error initializing FAISS index: {str(e)}")
            raise HTTPException(status_code=500, detail="Error initializing FAISS index")

        # Perform similarity search
        try:
            k = 6  # Number of nearest neighbors to search
            query_embedding_np = np.array(query_embedding).astype('float32').reshape(1, -1)
            distances, indices = index.search(query_embedding_np, k)
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            raise HTTPException(status_code=500, detail="Error performing similarity search")

        # Collect the similar data
        try:
            similar_data = [data[idx]['data'] for idx in indices[0]]
        except Exception as e:
            logger.error(f"Error collecting similar data: {str(e)}")
            raise HTTPException(status_code=500, detail="Error collecting similar data")

        # Generate response using GPT-3.5 Turbo
        try:
            conversation_history = []  # Initialize or fetch conversation history as required
            response_text = generate_response(query, similar_data, conversation_history)
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise HTTPException(status_code=500, detail="Error generating response")

        return {"response": response_text, "similar_data": similar_data}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

    

    
# adding responded queries endpoint
@app.post("/add_responded_queries")
async def add_responded_queries(request: RespondedQueryRequest):
    queries_and_responses = request.queries_and_responses
    try:
        for item in queries_and_responses:
            query = item['query']
            response = item['response']
            combined_text = f"query : {query} response : {response}"
            encoded_data = json.dumps(get_embedding(combined_text))

            response = supabase.table('respondedqueries').insert({
                'query': query,
                'response': response,
                'encoded_data': encoded_data
            }).execute()

            if not response.data:
                raise HTTPException(status_code=500, detail="Error inserting data into Supabase")

        return {"message": "All queries and responses have been added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint to raise an issue
@app.post("/issues_raising")
async def issues_raising(issue_request: IssueRequest):
    issue = issue_request.issue
    try:
        # Get the current maximum ID in the issues table
        max_id_response = supabase.table('issues').select('id').order('id', desc=True).limit(1).execute()
        if max_id_response.data:
            max_id = max_id_response.data[0]['id']
            new_id = max_id + 1
        else:
            new_id = 1  # Table is empty, start with ID 1

        # Insert issue into Supabase with the new ID
        response = supabase.table('issues').insert({
            'id': new_id,
            'issue': issue,
            'reason': '',  # Placeholder, to be updated by another endpoint
            'solution': '',  # Placeholder, to be updated by another endpoint
            'encoded_data': ''
        }).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Error inserting issue into Supabase")
        
        # send_email(issue)
        # send_whatsapp_and_sms(issue)
        send_slack_message(f"New Issue Raised: {issue}\n\nPlease reply in the following format:\n'reason : enter your reason here', 'solution : enter the solution'")

        return {"message": "Issue added successfully", "issue_id": response.data[0]['id']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Send message to slack using SendGrid
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_message(issue):
    slack_data = {
        'text': f"New Issue Raised: {issue}\n\nPlease reply in the following format:\n'issue : enter the issue', 'reason : enter your reason here', 'solution : enter the solution'"
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=slack_data)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")


@app.post("/update_issue")
async def update_issue(update_request: UpdateIssueRequest):
    try:
        # Retrieve the issue by ID
        issue_response = supabase.table('issues').select('issue').eq('id', update_request.issue_id).single().execute()
        if issue_response.data:
            issue_text = issue_response.data['issue']

            # Update the issue with reason and solution
            update_response = supabase.table('issues').update({
                'reason': update_request.reason,
                'solution': update_request.solution,
                'encoded_data': json.dumps({
                    "issue": issue_text,
                    "reason": update_request.reason,
                    "solution": update_request.solution
                })
            }).eq('id', update_request.issue_id).execute()

            if not update_response.data:
                raise HTTPException(status_code=500, detail="Error updating issue in Supabase")

            return {"message": "Issue updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Issue not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# run this using : 
# uvicorn main:app --reload