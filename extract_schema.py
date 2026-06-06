# ===================
# Import Libraries: 
# ===================
import pandas as pd 
import psycopg2
import json

# =========================
# Database Connection: 
# =========================
def connet_to_database():
    try: 
        conn = psycopg2.connect(
            host = "localhost",
            database =  "weather_data",
            user = "postgres",
            password = "Volume27@",
            port = "5432"
        )

        cursor = conn.cursor()

    except Exception as error:
        print(f"Database connection failed: {error}")
        return None, None

    return conn, cursor



def main():
    print("Entered main function.")

    # Connect to database
    conn, cur = connet_to_database()

    query = """
    SELECT
        table_name,
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """

    df = pd.read_sql(query, conn)

    schema = {}

    for table, group in df.groupby("table_name"):
        schema[table] = {
            "columns": {}
        }

        for _, row in group.iterrows():
            column = row["column_name"]
            dtype = row["data_type"]

            schema[table]["columns"][column] = {
                "type": dtype,
                "description": None  # placeholder for future enrichment
            }

    print(schema)

    with open("schema.json", "w") as f:
        json.dump(schema, f, indent=4)



if '__main__' == __name__:
    main()
