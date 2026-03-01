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
        # 1. Filter: Only process incoming TEXT messages
        if data.get("typeWebhook") == "incomingMessageReceived" and data.get("messageData", {}).get("typeMessage") == "textMessage":
            
            sender_phone = data['senderData']['chatId'] 
            
            # 🛑 SHIELD 1: Ignore all Group Messages
            if "@g.us" in sender_phone:
                return {"status": "success"}

            message_text = data['messageData']['textMessageData']['textMessage']
            print(f"\n🔔 MESSAGE RECEIVED: {message_text}")

            # 🛑 SHIELD 2: The Database Target Lock
            lead_context = get_lead_by_phone(sender_phone)
            
            if not lead_context:
                print(f"🔒 UNKNOWN NUMBER ({sender_phone}). Ignoring to stay professional.")
                return {"status": "success"}
                
            print(f"✅ VERIFIED LEAD DETECTED: {lead_context['name']} asking about {lead_context['property']}")
            
            # 3. The Brain: Pass message AND database context to OpenAI
            ai_reply = generate_chat_reply(message_text, lead_context)
            print(f"🤖 AI REPLIES: {ai_reply}")
            
            # 4. The Mouth: Send the reply back
            send_message_via_greenapi(sender_phone, ai_reply)
            
    except Exception as e:
        print(f"⚠️ Webhook processing error: {e}")
        
    return {"status": "success"}

if __name__ == "__main__":
    print("👂 AI Agent is awake, shielded, and listening on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)