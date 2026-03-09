from fastapi import FastAPI, Request
import uvicorn

from app.services.openai_cli import generate_chat_reply
from app.services.whatsapp_green_cli import send_message_via_greenapi
from app.database.db_handler import get_lead_by_phone

app = FastAPI()

@app.post("/webhook")
async def receive_whatsapp_message(request: Request):
    data = await request.json()
    
    try:
        webhook_type = data.get("typeWebhook")
        
        # 1. Ignore delivery receipts and outgoing messages
        if webhook_type != "incomingMessageReceived":
            return {"status": "success"}

        msg_data = data.get("messageData", {})
        msg_type = msg_data.get("typeMessage")
        
        print(f"\n🔍 [DEBUG] WhatsApp Message Type: {msg_type}")
        
        # 🚀 SMART MESSAGE EXTRACTOR
        message_text = ""
        if msg_type == "textMessage":
            message_text = msg_data.get("textMessageData", {}).get("textMessage", "")
        elif msg_type == "extendedTextMessage":
            message_text = msg_data.get("extendedTextMessageData", {}).get("text", "")
        elif msg_type == "quotedMessage":
            message_text = msg_data.get("extendedTextMessageData", {}).get("text", "")
        else:
            print(f"🙈 Ignored non-text type: {msg_type}")
            return {"status": "success"}

        sender_phone = data['senderData']['chatId'] 
        
        # 🚨 THE NEW CALLER ID 
        print(f"📱 [CALLER ID] Message from: {sender_phone}")
        
        # 🛑 SHIELD 1: Ignore Group Messages
        if "@g.us" in sender_phone:
            print("🛡️ Shield blocked a group message.")
            return {"status": "success"}

        print(f"🔔 CUSTOMER SAYS: {message_text}")

        # 🛑 SHIELD 2: Database Check
        lead_context = get_lead_by_phone(sender_phone)
        
        if not lead_context:
            print(f"🔒 UNKNOWN NUMBER ({sender_phone}). Ignoring to stay professional.")
            return {"status": "success"}
            
        print(f"✅ VERIFIED LEAD DETECTED: {lead_context['name']}")
        
        ai_reply = generate_chat_reply(message_text, lead_context)
        print(f"🤖 AI REPLIES: {ai_reply}")
        
        send_message_via_greenapi(sender_phone, ai_reply)
            
    except Exception as e:
        print(f"⚠️ Webhook processing error: {e}")
        
    return {"status": "success"}

if __name__ == "__main__":
    print("👂 AI Agent is listening with CALLER ID on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)