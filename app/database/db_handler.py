import sqlite3
from datetime import datetime
import re

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
    Saves a new lead into our database OR updates an existing one 
    if they inquire about the same property again (Deduplication).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Check if this exact Phone + Property combination already exists
    cursor.execute('''
        SELECT id FROM leads 
        WHERE phone = ? AND property = ?
    ''', (phone, property_name))
    
    existing_lead = cursor.fetchone()
    
    if existing_lead:
        # 2. If they exist, just update their timestamp and score (Do not duplicate!)
        cursor.execute('''
            UPDATE leads 
            SET timestamp = ?, score = ?, summary = ?
            WHERE id = ?
        ''', (datetime.now(), score, summary, existing_lead[0]))
        print(f"🔄 Lead {name} already exists for {property_name}. Timestamp updated.")
    else:
        # 3. If they are new, insert a fresh row
        cursor.execute('''
            INSERT INTO leads (name, phone, property, score, summary, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, phone, property_name, score, summary, datetime.now()))
        print(f"💾 New Lead for {name} saved to database.")
    
    conn.commit()
    conn.close()
    
def get_lead_by_phone(phone_number):
    """
    SECURITY SHIELD: Checks if the phone number exists in our database.
    Returns the lead's Name and Property if found, otherwise returns None.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Clean the incoming GreenAPI number (extract just the digits)
    clean_phone = re.sub(r'\D', '', str(phone_number))
    
    # We check the last 10 digits to avoid +91 country code mismatch issues
    search_number = f'%{clean_phone[-10:]}%'
    
    cursor.execute('''
        SELECT name, property FROM leads 
        WHERE phone LIKE ? 
        ORDER BY timestamp DESC LIMIT 1
    ''', (search_number,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"name": result[0], "property": result[1]}
    
    return None