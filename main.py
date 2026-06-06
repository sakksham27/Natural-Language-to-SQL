import json
import os
from google import genai

def generate_sql(prompt):
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    
    return response.text

def load_schema(filepath="schema.json"):
    with open(filepath, "r") as f:
        schema = json.load(f)
    
    schema_str = ""
    
    for table_name, table_info in schema.items():
        schema_str += f"Table: {table_name}\n"
        
        for column_name, column_info in table_info["columns"].items():
            schema_str += f"  - {column_name} ({column_info['type']}): {column_info['description']}\n"
        
        schema_str += "\n"
    
    return schema_str

def build_prompt(question, schema_str):
    prompt = f"""You are an expert PostgreSQL SQL generator.

Here is the database schema:
{schema_str}

Rules:
- Use only the tables and columns provided above
- Do NOT invent or assume any columns
- Use PostgreSQL syntax only
- Return ONLY the SQL query, no explanation

User Question:
{question}
"""
    return prompt

def main():
    schema_str = load_schema("schema.json")
    
    question = "What is the average temperature in San Diego?"
    
    prompt = build_prompt(question, schema_str)
    
    sql = generate_sql(prompt)
    
    print("Generated SQL:")
    print(sql)

if '__main__' == __name__:
    main()
