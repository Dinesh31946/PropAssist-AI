import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp_alert(lead_name, property_name, lead_score, summary):
    """
    Sends a WhatsApp message to the Agent (You).
    Includes a 'Mock Mode' for testing without API keys.
    """
    token = os.getenv("WHATSAPP_TOKEN")
    phone_id = os.getenv("WHATSAPP_PHONE_ID")
    agent_phone = os.getenv("WHATSAPP_MY_NUMBER") 
    
    # --- 1. Construct the Message ---
    if lead_score >= 90:
        emoji = "🔥 HOT LEAD"
    elif lead_score >= 70:
        emoji = "⚠️ WARM LEAD"
    else:
        emoji = "ℹ️ NEW LEAD"
    
    message_body = f"""
{emoji} *PropAssist Alert*

*👤 Name:* {lead_name}
*🏢 Property:* {property_name}
*💯 Score:* {lead_score}/100

*📝 Insight:* {summary}

_Reply to this customer immediately via the 99acres app!_
    """

    # --- 2. MOCK MODE CHECK (Since you are blocked) ---
    if not token or not phone_id:
        print("\n" + "="*40)
        print("🛑 MOCK MODE (No API Keys Found)")
        print("📱 This message WOULD be sent to WhatsApp:")
        print("-" * 20)
        print(message_body)
        print("="*40 + "\n")
        return "✅ Mock Alert Simulated"

    # --- 3. Real Sending Logic (Runs when you get keys) ---
    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    
    payload = {
        "messaging_product": "whatsapp",
        "to": agent_phone,
        "type": "text",
        "text": {"body": message_body}
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return "✅ WhatsApp Alert Sent!"
        else:
            return f"❌ Meta API Error: {response.text}"
    except Exception as e:
        return f"❌ Connection Error: {e}"