import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def analyze_lead_with_ai(email_body):
    print("🧠 AI is analyzing...")
    
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # --- CHANGE 1: THE UPDATED PROMPT ---
        prompt = """
        You are a Real Estate Lead Extractor.
        
        INPUT: An email body (Direct or Forwarded).
        TASK:
        1. Ignore "Forwarded message" headers.
        2. Extract:
           - Customer Name (If unknown, use "Guest")
           - Customer Phone (Look for 10-12 digit numbers. If +91 is missing, add it. If none, return null).
           - Property Name
        3. Rate 'score' (0-100) based on urgency.
        4. Create a 'summary'.
        
        OUTPUT JSON ONLY:
        {"name": "Name", "phone": "919876543210", "property": "Property", "score": 90, "summary": "Summary"}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": email_body}
            ],
            response_format={"type": "json_object"}
        )

        ai_analysis = response.choices[0].message.content
        
        # Pass the data to the next step
        from app.services.email_cli import save_lead_to_db_and_alert
        save_lead_to_db_and_alert(ai_analysis)

    except Exception as e:
        print(f"❌ AI Error: {e}")

def generate_chat_reply(customer_message):
    """
    Takes the live WhatsApp message, runs it through the Persona, 
    and returns a Hinglish reply.
    """
    print("🧠 AI is thinking about the reply...")
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # The Persona (Your Competitive Moat)
        system_prompt = """
        You are a highly professional and polite real estate agent working in Navi Mumbai, specifically specializing in the Ulwe area. 
        Your goal is to qualify leads and get them to agree to a site visit. 
        Speak in natural 'Hinglish' (a mix of Hindi and English) just like a real Indian broker. 
        Keep your answers short, crisp, and conversational. Do not sound like a robot.
        If they ask for property prices, give a realistic estimate for Ulwe but tell them exact prices depend on the property, and ask when they can come for a site visit.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini", # Keeping it fast and cheap!
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": customer_message}
            ]
        )

        ai_reply = response.choices[0].message.content
        return ai_reply

    except Exception as e:
        print(f"❌ Chat AI Error: {e}")
        return "Sorry, I am currently driving. I will call you back shortly!"