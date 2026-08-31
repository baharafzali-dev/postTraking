import os
import sqlite3
import psycopg2

db_url = os.getenv('DATABASE_URL')

def create_tables():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    cur.execute("PRAGMA foreign_keys = ON")
    #cur.execute("DROP TABLE IF EXISTS shipments")


    cur.execute('''
        CREATE TABLE IF NOT EXISTS shipments (
            id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            tracking_code TEXT NOT NULL UNIQUE,
            shipment_date TEXT NOT NULL DEFAULT '',
            city TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    create_tables()
    print("succesfully!")