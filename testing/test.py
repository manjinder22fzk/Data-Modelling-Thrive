# Test python file to check if tables exist or not

import sqlite3

DB_PATH = 'database/thrive_test_db.db'

def list_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tables inside thrive_test_db.db:")
    for table in tables:
        print(table[0])
    
    conn.close()

if __name__ == "__main__":
    list_tables()
