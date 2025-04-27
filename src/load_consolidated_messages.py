import sqlite3
import logging
import os
import pandas as pd


# Logging Setup
os.makedirs('logs', exist_ok=True)
os.makedirs('output', exist_ok=True)
logging.basicConfig(filename='logs/app.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_PATH = 'database/thrive_test_db.db'

def export_consolidated_messages_to_csv():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM consolidated_messages", conn)
    df.to_csv('output/consolidated_messages.csv', index=False)
    conn.close()


def create_consolidated_messages_table(cursor):
    # Drop table if it exists
    tables_to_drop = ['dim_users', 'dim_conversation_parts', 'consolidated_messages']
    for table in tables_to_drop:
        cursor.execute(f'DROP TABLE IF EXISTS {table};')

    
    with open('scripts/create_consolidated_messages_table.sql', 'r') as file:
        create_table_query = file.read()
    cursor.executescript(create_table_query)
    logging.info("consolidated_messages table created successfully.")

def insert_consolidated_messages(cursor):
    # Read insert query from SQL file
    with open('scripts/load_consolidated_messages.sql', 'r') as file:
        insert_query = file.read()
    cursor.executescript(insert_query)
    logging.info("Data inserted into consolidated_messages successfully.")

def generate_data_quality_report():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open('output/data_quality_report.txt', 'w') as f:
        f.write("Data Quality Report\n")
        f.write("====================\n")

        cursor.execute('SELECT COUNT(*) FROM consolidated_messages')
        total_rows = cursor.fetchone()[0]
        f.write(f"Total Rows: {total_rows}\n")

        cursor.execute('SELECT COUNT(*) FROM consolidated_messages WHERE id IS NULL')
        null_ids = cursor.fetchone()[0]
        f.write(f"Null IDs: {null_ids}\n")

        cursor.execute('SELECT COUNT(DISTINCT conversation_id) FROM consolidated_messages')
        distinct_conversations = cursor.fetchone()[0]
        f.write(f"Distinct Conversations: {distinct_conversations}\n")

        cursor.execute('SELECT message_type, COUNT(*) FROM consolidated_messages GROUP BY message_type ORDER BY COUNT(*) DESC LIMIT 5')
        f.write("\nTop 5 Message Types:\n")
        for row in cursor.fetchall():
            f.write(f"{row[0]}: {row[1]}\n")

    conn.close()


def main():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        logging.info("Database connection established.")

        conn.execute('BEGIN')

        # Create table
        create_consolidated_messages_table(cursor)

        # Insert data
        insert_consolidated_messages(cursor)

        conn.commit()
        logging.info("Transaction committed successfully.")

        export_consolidated_messages_to_csv()
        logging.info("Writing the data into csv file")

        generate_data_quality_report()
        logging.info("Generating Data Quality Reports")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        conn.rollback()
        logging.info("Transaction rolled back due to error.")
    finally:
        conn.close()
        logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
