from fastapi import FastAPI, Request
import uvicorn

# Import your custom modules
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
        
        # 🚨 X-RAY VISION: Print exactly what GreenAPI is sending
        print(f"\n🔍 [DEBUG] WhatsApp Message Type: {msg_type}")
        
        # 🚀 SMART MESSAGE EXTRACTOR
        message_text = ""
        if msg_type == "textMessage":
            message_text = msg_data.get("textMessageData", {}).get("textMessage", "")
        elif msg_type == "extendedTextMessage":
            message_text = msg_data.get("extendedTextMessageData", {}).get("text", "")
        else:
            # If it's a sticker, image, or reaction, we print the RAW JSON to see what it looks like
            print(f"🙈 Ignored non-text message type: {msg_type}")
            print(f"📦 [RAW DATA]: {data}")
            return {"status": "success"}

        sender_phone = data['senderData']['chatId'] 
        
        # 🛑 SHIELD 1: Ignore all Group Messages
        if "@g.us" in sender_phone:
            return {"status": "success"}

        print(f"🔔 CUSTOMER SAYS: {message_text}")

        # 🛑 SHIELD 2: The Database Target Lock
        lead_context = get_lead_by_phone(sender_phone)
        
        if not lead_context:
            print(f"🔒 UNKNOWN NUMBER ({sender_phone}). Ignoring to stay professional.")
            return {"status": "success"}
            
        print(f"✅ VERIFIED LEAD DETECTED: {lead_context['name']} asking about {lead_context['property']}")
        
        # 3. The Brain
        ai_reply = generate_chat_reply(message_text, lead_context)
        print(f"🤖 AI REPLIES: {ai_reply}")
        
        # 4. The Mouth
        send_message_via_greenapi(sender_phone, ai_reply)
            
    except Exception as e:
        print(f"⚠️ Webhook processing error: {e}")
        
    return {"status": "success"}

if __name__ == "__main__":
    print("👂 AI Agent is awake, shielded, and listening on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)