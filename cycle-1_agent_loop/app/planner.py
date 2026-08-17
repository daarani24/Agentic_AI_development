import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def plan_sql(user_request, schema, previous_observation=None):
    prompt=f"""
    You are a SQL planning agent.

    Database schema:
    {schema}

    User request:
    {user_request}  

    Previous attempt observation:
    {previous_observation}

    Important:  
    - If the previous attempt returned an SQL error, correct the SQL using the error message.
    - If the previous attempt executed successfully but returned zero rows, reconsider the query and determine whether the user's request can actually produce results from the available database.
    - Do not repeat the exact same SQL query when the previous attempt returned zero rows.
    - Use only tables and columns that exist in the provided schema.

    Generate one valid SQLite SELECT query that answers the user's request.

    Return only the SQL query.
    Do not include markdown.
    """

    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()