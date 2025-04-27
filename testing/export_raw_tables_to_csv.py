import sqlite3
import pandas as pd
import os

DB_PATH = 'database/thrive_test_db.db'

def export_table_to_csv(conn, table_name, output_folder='output_raw_tables'):
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

    try:
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, conn)
        csv_path = os.path.join(output_folder, f"{table_name}.csv")
        df.to_csv(csv_path, index=False)
        print(f"✅ Exported {table_name} to {csv_path}")
    except Exception as e:
        print(f"❌ Failed to export {table_name}: {e}")

def main():
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"✅ Connected to {DB_PATH}")

        # Export all three raw tables
        export_table_to_csv(conn, 'users')
        export_table_to_csv(conn, 'conversation_start')
        export_table_to_csv(conn, 'conversation_parts')

        conn.close()
        print("✅ Connection closed.")
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")

if __name__ == "__main__":
    main()
