from flask import Flask, render_template, request, jsonify
from main import load_schema, build_prompt, generate_sql
import psycopg2

app = Flask(__name__)

def run_query(sql):
    conn = psycopg2.connect(
        host="localhost",
        database="weather_data",
        user="postgres",
        password="Volume27@",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute(sql)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return columns, rows

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        question = request.json.get("question")
        
        schema_str = load_schema("schema.json")
        prompt = build_prompt(question, schema_str)
        sql = generate_sql(prompt)
        
        # clean up sql in case model adds markdown fences
        sql = sql.strip().replace("```sql", "").replace("```", "").strip()
        
        columns, rows = run_query(sql)
        
        return jsonify({
            "sql": sql,
            "columns": columns,
            "rows": rows
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
