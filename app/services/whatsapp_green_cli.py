import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Load keys from .env
INSTANCE_ID = os.getenv("GREEN_API_INSTANCE_ID")
API_TOKEN = os.getenv("GREEN_API_TOKEN")
TARGET_PHONE = os.getenv("GREEN_API_PHONE")

# The URL where we send commands
BASE_URL = f"https://api.green-api.com/waInstance{INSTANCE_ID}"

def send_whatsapp_alert(lead_name, property_name, lead_score, summary):
    """
    Sends a WhatsApp message via GreenAPI (Bypassing Meta).
    """
    # Safety Check: Are keys missing?
    if not INSTANCE_ID or not API_TOKEN:
        print("⚠️ GreenAPI credentials missing. Check .env")
        return

    if not TARGET_PHONE:
         print("⚠️ Target phone missing in .env")
         return

    # 1. Format the phone number (GreenAPI needs '@c.us' at the end)
    chat_id = f"{TARGET_PHONE}@c.us"

    # 2. Create the Message Text
    # We use '*' for bold text, just like normal WhatsApp
    message = (
        f"🔥 *HOT LEAD: PropAssist Alert*\n\n"
        f"👤 *Name:* {lead_name}\n"
        f"🏢 *Property:* {property_name}\n"
        f"💯 *Score:* {lead_score}/100\n\n"
        f"📝 *Insight:* {summary}\n\n"
        f"_Reply to this customer via the app!_"
    )

    # 3. Send it!
    url = f"{BASE_URL}/sendMessage/{API_TOKEN}"
    
    payload = {
        "chatId": chat_id,
        "message": message
    }
    
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            print("✅ WhatsApp Alert Sent (via GreenAPI)!")
        else:
            print(f"⚠️ WhatsApp Fail: {response.text}")
            
    except Exception as e:
        print(f"⚠️ Connection Error: {e}")