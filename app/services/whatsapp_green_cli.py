import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Load Config
INSTANCE_ID = os.getenv("GREEN_API_INSTANCE_ID")
API_TOKEN = os.getenv("GREEN_API_TOKEN")
# This is YOUR number (The Agent) from the .env file
AGENT_PHONE = os.getenv("GREEN_API_PHONE") 

BASE_URL = f"https://api.green-api.com/waInstance{INSTANCE_ID}"

def send_message_via_greenapi(target_number, message_text):
    """
    Generic function to send ANY message to ANY number.
    """
    if not target_number:
        return

    # 1. Clean the number (Remove +, spaces, dashes)
    clean_phone = re.sub(r'\D', '', str(target_number))
    
    # 2. Format for GreenAPI
    chat_id = f"{clean_phone}@c.us"
    
    url = f"{BASE_URL}/sendMessage/{API_TOKEN}"
    payload = {"chatId": chat_id, "message": message_text}
    headers = {'Content-Type': 'application/json'}
    
    try:
        requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"🚀 Sent WhatsApp to {clean_phone}")
    except Exception as e:
        print(f"⚠️ Error sending to {clean_phone}: {e}")

def handle_new_lead_flow(lead_name, lead_phone, property_name, lead_score, summary):
    """
    The 'Hybrid' Logic:
    1. Send Welcome Message to Customer (Lead).
    2. Send Alert to Agent (You).
    """
    
    # --- STEP 1: TALK TO CUSTOMER (The "Welcome" Message) ---
    if lead_phone:
        print(f"💬 Auto-Replying to Customer: {lead_name}")
        welcome_msg = (
            f"Hi {lead_name}, thank you for inquiring about {property_name}. \n\n"
            f"I have received your details and will call you shortly to discuss. \n"
            f"Are you planning a site visit this week?"
        )
        send_message_via_greenapi(lead_phone, welcome_msg)
    else:
        print("⚠️ No customer phone found in email. Skipping auto-reply.")

    # --- STEP 2: ALERT THE AGENT (You) ---
    print(f"🔔 Notifying Agent...")
    
    # We add a visual checkmark if the Auto-Reply was sent
    status = "✅ *Auto-Reply Sent!*" if lead_phone else "⚠️ *Could not Auto-Reply (No Phone)*"

    alert_msg = (
        f"🔥 *NEW LEAD DETECTED*\n\n"
        f"👤 {lead_name}\n"
        f"📞 {lead_phone}\n"
        f"🏢 {property_name}\n"
        f"💯 Score: {lead_score}/100\n\n"
        f"📝 {summary}\n\n"
        f"{status}\n"
        f"_Check your WhatsApp to continue the chat!_"
    )
    # Send to the number in your .env
    send_message_via_greenapi(AGENT_PHONE, alert_msg)