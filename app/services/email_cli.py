import imaplib
import email
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.core.parser import extract_basic_info
from app.core.models import Lead
from app.services.openai_cli import analyze_lead_with_ai
import json
from app.database.db_handler import save_lead_to_db

# Load environment variables from .env file
load_dotenv()

def connect_to_email():
    """Connects to Gmail IMAP server securely."""
    user = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASS")
    
    # Connect to Gmail's IMAP server on Port 993 (SSL)
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(user, password)
    return mail

def extract_body(msg):
    """Helper function to handle multi-part emails and get the text content safely."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                # Added 'errors="ignore"' to handle special characters without crashing
                return part.get_payload(decode=True).decode(errors="ignore")
    else:
        # Added 'errors="ignore"' here too
        return msg.get_payload(decode=True).decode(errors="ignore")
    return ""

def check_for_leads():
    """Main function to scan for fresh unread leads."""
    try:
        mail = connect_to_email()
        mail.select("inbox")

        # Create a date string for 'Yesterday' (format: 30-Jan-2026)
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
        
        # 🎯 TARGETED SEARCH: 
        # Only Unseen emails FROM 99acres with "Lead" in the Subject since yesterday
        # You can add more portals like: OR (FROM "magicbricks.com")
        
        portals = ["99acres.com", "magicbricks.com", "facebookmail.com"]
        portal_query = f'FROM "{portals[0]}"'
        
        for portal in portals[1:]:
            portal_query = f'OR (FROM "{portal}") ({portal_query})'
        
        search_criteria = f'(UNSEEN SENTSINCE {yesterday} FROM "gosavidinesh68@gmail.com" SUBJECT "Lead")'
        status, messages = mail.search(None, search_criteria)
        
        if status == 'OK':
            id_list = messages[0].split()
            if not id_list:
                print(f"😴 No new unread leads since {yesterday}.")
                return

            print(f"🎯 Targeted Search: Found {len(id_list)} REAL leads. Processing...")

            for num in id_list:
                res, msg_data = mail.fetch(num, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Extract the text body
                        body = extract_body(msg) 

                        # Extract name and phone using our logic in parser.py
                        name, phone = extract_basic_info(body)
                        
                        if phone != "Unknown":
                            print(f"🔎 Potential Lead Found. Consulting AI...")
    
                            # Send the email body to our new AI function
                            ai_analysis = analyze_lead_with_ai(body)
                            
                            print("-" * 30)
                            print(f"🤖 PROPASSIST AI REPORT:")
                            print(ai_analysis)
                            print("-" * 30)
                            
                            try:
                                # Convert the AI's string response into a Python Dictionary
                                data = json.loads(ai_analysis) 
                                
                                save_lead_to_db(
                                    name=data.get("name"),
                                    phone=phone, # We use the phone number our regex found
                                    property_name=data.get("property"),
                                    score=data.get("score"),
                                    summary=data.get("summary")
                                )
                            except Exception as e:
                                print(f"⚠️ Could not save to DB: {e}")
                            
                        else:
                            # Marking as read so we don't look at it in the next loop
                            mail.store(num, '+FLAGS', '\\Seen')
                            print("⏭️ Marked non-lead email as read.")
                            
        mail.logout()
        
    except Exception as e:
        print(f"⚠️ Error inside check_for_leads: {e}")