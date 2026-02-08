import os
import time
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
from app.services.openai_cli import analyze_lead_with_ai
import datetime

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
IMAP_SERVER = "imap.gmail.com"
EMAIL_USER = os.getenv("GMAIL_USER")
EMAIL_PASS = os.getenv("GMAIL_PASS")

def connect_to_email():
    """Connects to Gmail IMAP"""
    # --- SAFETY CHECK 1: Are credentials loaded? ---
    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ CRITICAL ERROR: Email credentials are missing!")
        print(f"   - GMAIL_USER detected: {'Yes' if EMAIL_USER else 'NO'}")
        print(f"   - GMAIL_APP_PASSWORD detected: {'Yes' if EMAIL_PASS else 'NO'}")
        print("   -> Check your .env file is in the same folder and has these exact keys.")
        return None

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        return mail
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return None

def extract_body(msg):
    """Safe extraction of plain text body from email"""
    try:
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode(errors="ignore")
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                return payload.decode(errors="ignore")
    except Exception as e:
        print(f"⚠️ Error extracting body: {e}")
    
    return ""

def check_for_leads():
    """
    Scans for NEW leads (Direct from Portal OR Forwarded from Agent).
    STRICTER MODE: Only accepts recognized Portals or Explicit Keywords.
    PERFORMANCE FIX: Uses Gmail's 'newer_than:1h' to scan only the last 60 mins.
    """
    try:
        print("⏳ Connecting to Gmail...")
        mail = connect_to_email()
        if not mail:
            return

        mail.select("inbox")
        
        # --- FIX: "LAST HOUR" FILTER (Gmail Specific) ---
        # "is:unread" -> Only unread messages
        # "newer_than:1h" -> Only received in the last 1 hour (Google Magic)
        print(f"📅 Searching for unread emails from the last 1 hour...")
        
        # This syntax is specific to Gmail and is VERY fast
        status, messages = mail.search(None, 'X-GM-RAW "is:unread newer_than:1h"')
        
        if status != 'OK':
            print("❌ Failed to search emails.")
            return

        id_list = messages[0].split()
        if not id_list:
            print("😴 No new unread emails in the last hour.")
            return

        print(f"📨 Scanning {len(id_list)} new emails...")

        for num in id_list:
            res, msg_data = mail.fetch(num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # 1. Get Subject & Sender
                    subject = msg["Subject"] if msg["Subject"] else "No Subject"
                    sender = msg["From"] if msg["From"] else "Unknown"
                    
                    subj_lower = subject.lower()
                    sender_lower = sender.lower()

                    # --- STRICT FILTERING LOGIC ---

                    # 1. TRUSTED PORTALS (Always Accept)
                    trusted_portals = ["99acres", "magicbricks", "housing.com", "commonfloor", "squareyards", "nobroker"]
                    is_portal = any(p in sender_lower for p in trusted_portals)

                    # 2. STRICT KEYWORDS (Subject must contain these)
                    lead_keywords = ["lead", "enquiry", "inquiry", "requirement", "interested in", "i am interested"]
                    has_lead_keyword = any(k in subj_lower for k in lead_keywords)

                    if is_portal or has_lead_keyword:
                        print(f"✅ FOUND LEAD: '{subject}' | From: {sender}")
                        
                        body = extract_body(msg)
                        
                        if body and len(body.strip()) > 0:
                            clean_body = " ".join(body.split())
                            analyze_lead_with_ai(clean_body)
                        else:
                            print("⚠️ Warning: Email body was empty. Skipping.")
                    
                    else:
                        print(f"❌ SKIPPED: '{subject}' (No portal or keyword match)")

        mail.logout()
        
    except Exception as e:
        print(f"⚠️ Error in check_for_leads: {e}")

# Helper to prevent circular imports
def save_lead_to_db_and_alert(ai_json_string):
    import json
    from app.services.whatsapp_green_cli import send_whatsapp_alert
    from app.database.db_handler import save_lead_to_db

    try:
        data = json.loads(ai_json_string)
        
        save_lead_to_db(
            name=data.get("name"),
            phone="Unknown",
            property_name=data.get("property"),
            score=data.get("score"),
            summary=data.get("summary")
        )

        send_whatsapp_alert(
            lead_name=data.get("name"),
            property_name=data.get("property"),
            lead_score=data.get("score"),
            summary=data.get("summary")
        )

    except Exception as e:
        print(f"⚠️ Saving Error: {e}")