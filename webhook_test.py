from fastapi import FastAPI, Request
import uvicorn

# 🧩 Importing your existing modules!
from app.services.openai_cli import generate_chat_reply
from app.services.whatsapp_green_cli import send_message_via_greenapi

app = FastAPI()

@app.post("/webhook")
async def receive_whatsapp_message(request: Request):
    data = await request.json()
    
    try:
        # 1. Filter: Only process incoming TEXT messages (ignore status updates)
        if data.get("typeWebhook") == "incomingMessageReceived" and data.get("messageData", {}).get("typeMessage") == "textMessage":
            
            # 2. Extract the message and the sender's phone number
            message_text = data['messageData']['textMessageData']['textMessage']
            sender_phone = data['senderData']['chatId'] 
            
            print(f"\n🔔 CUSTOMER SAYS: {message_text}")
            
            # 3. The Brain: Send text to OpenAI and get a reply
            ai_reply = generate_chat_reply(message_text)
            print(f"🤖 AI REPLIES: {ai_reply}")
            
            # 4. The Mouth: Send the reply back via your existing GreenAPI function
            send_message_via_greenapi(sender_phone, ai_reply)
            
    except Exception as e:
        print(f"⚠️ Webhook processing error: {e}")
        
    return {"status": "success"}

if __name__ == "__main__":
    print("👂 AI Agent is awake and listening on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)