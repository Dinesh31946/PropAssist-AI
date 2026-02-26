from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def receive_whatsapp_message(request: Request):
    # 1. Get the data from GreenAPI
    data = await request.json()
    
    # 2. Print it to the screen so we can see it!
    print("🔔 DING! NEW MESSAGE RECEIVED:")
    print(data)
    
    # 3. Tell GreenAPI "Thanks, I got it"
    return {"status": "success"}

if __name__ == "__main__":
    print("👂 Webhook is listening on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)