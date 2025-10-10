import sqlite3
import os
import pandas as pd
import re
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

# ---------------- ENVIRONMENT SETUP ----------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")

# Configure Gemini globally
genai.configure(api_key=api_key)

# Create the model instance
client_sql = genai.GenerativeModel(model_name=GOOGLE_MODEL)

# ---------------- DATABASE PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "web-scraping", "db.sqlite")

# ---------------- PROMPTS ----------------
prompt = """
You are an expert in understanding the database schema and generating SQL queries for a natural language question asked
pertaining to the data you have. The schema is provided in the schema tags. 

<schema> 
table: product 

fields: 
product_link - string (hyperlink to product)
title - string (name of the product)
brand - string (brand of the product)
price - integer (price of the product in Indian Rupees)
discount - float (discount on the product. 10 percent discount is represented as 0.1, 20 percent as 0.2, and such.)
avg_rating - float (average rating of the product. Range 0–5, 5 is the highest.)
total_ratings - integer (total number of ratings for the product)
</schema>

Make sure whenever you try to search for the brand name, the name can be in any case. 
So, make sure to use %LIKE% to find the brand in condition. Never use ILIKE.
Create a single SQL query for the question provided. 
The query should have all the fields in SELECT clause (i.e. SELECT *).

Just the SQL query is needed, nothing more. Always provide the SQL in between the <SQL> </SQL> tags,
for example: <SQL> SELECT * FROM product WHERE brand LIKE '%nike%' </SQL>.
Do not write anything else apart from the SQL query in between the <SQL> </SQL> tags.
"""

comprehension_prompt = """
You are an expert in understanding the context of the question and replying based on the data provided. 
You will be given Question: and Data: fields. The Data will be in the form of an array, dataframe, or dict.

Reply only based on the provided data — no external assumptions.

When asked about products, always reply in this format:
1. Product title: Rs. price (X percent off), Rating: Y <link>

Example:
1. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.7 <link>
2. Puma Men Running Shoes: Rs. 1222 (57 percent off), Rating: 4.4 <link>
3. Reebok Men Running Shoes: Rs. 1500 (45 percent off), Rating: 4.1 <link>
"""

# ---------------- GEMINI HELPERS ----------------
def generate_sql_query(question: str) -> str:
    """
    Generates an SQL query from a natural language question using Gemini.
    """
    response = client_sql.generate_content(
        contents=[
            {"role": "system", "parts": prompt},
            {"role": "user", "parts": question}
        ],
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 1024
        }
    )
    return response.text.strip() if response.text else ""

def run_query(query: str) -> pd.DataFrame:
    """
    Executes a SQL SELECT query and returns the results as a pandas DataFrame.
    """
    if query.strip().upper().startswith("SELECT"):
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query(query, conn)
    else:
        raise ValueError("Invalid query: Only SELECT statements are allowed.")

def data_comprehension(question: str, data) -> str:
    """
    Uses Gemini to generate a natural language summary of the SQL query result.
    """
    response = client_sql.generate_content(
        contents=[
            {"role": "system", "parts": comprehension_prompt},
            {"role": "user", "parts": f"Question: {question}\nData: {data}"}
        ],
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 1024
        }
    )
    return response.text.strip() if response.text else "No response generated."

def sql_chain(question: str) -> str:
    """
    Complete pipeline:
    1. Convert question → SQL
    2. Execute SQL
    3. Interpret result in natural language
    """
    sql_query = generate_sql_query(question)
    matches = re.findall(r"<SQL>(.*?)</SQL>", sql_query, re.DOTALL)

    if not matches:
        return "Sorry, I could not generate a valid SQL query."

    query = matches[0].strip()
    try:
        response_df = run_query(query)
    except Exception as e:
        return f"Error executing SQL: {str(e)}"

    if response_df.empty:
        return "No matching records found in the database."

    context = response_df.to_dict(orient='records')
    answer = data_comprehension(question, context)
    return answer

# ---------------- MAIN ----------------
if __name__ == "__main__":
    question = "all nike shoes in price range 1000 to 5000"
    answer = sql_chain(question)
    print(answer)
