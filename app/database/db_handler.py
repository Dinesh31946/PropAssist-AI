import sqlite3
from datetime import datetime

# This is the name of your database file
DB_NAME = "propassist.db"

def init_db():
    """
    Creates the database and the 'leads' table if they don't exist.
    Think of this as creating an Excel sheet with specific columns.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create Table: We define Name, Phone, Property, and Score as columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            property TEXT,
            score INTEGER,
            summary TEXT,
            timestamp DATETIME
        )
    ''')
    
    conn.commit()
    conn.close()
    print("🗄️ Database initialized successfully.")

def save_lead_to_db(name, phone, property_name, score, summary):
    """
    Saves a new lead into our 'Excel-like' database.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO leads (name, phone, property, score, summary, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, phone, property_name, score, summary, datetime.now()))
    
    conn.commit()
    conn.close()
    print(f"💾 Lead for {name} saved to database.")