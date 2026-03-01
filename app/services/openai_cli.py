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

def generate_chat_reply(customer_message, lead_context):
    """
    Takes the live WhatsApp message AND the database context, 
    and returns a highly professional real estate reply.
    """
    print("🧠 AI is thinking about the reply...")
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Extract context from our database
        name = lead_context.get("name", "Customer")
        property_name = lead_context.get("property", "a property in Ulwe")

        # 🚀 THE ENTERPRISE SYSTEM PROMPT
        system_prompt = f"""
        You are a highly professional and polite real estate agent working in Navi Mumbai, specifically specializing in the Ulwe area. 
        You are currently talking to a qualified lead named {name} who previously inquired about {property_name}.
        
        YOUR GOAL: Qualify the lead, build trust, and get them to agree to a site visit. 
        
        CRITICAL RULES:
        1. LANGUAGE MIRRORING: You MUST mirror the user's exact language script. If they type in Romanized Hindi (e.g., 'kya price hai'), reply in Romanized Hindi. If English, use English. If Marathi script, use Marathi script.
        2. PRICING (TEASE & PIVOT): If they ask for the exact or all-inclusive price, DO NOT give a single fixed number. Give a realistic range for {property_name} (e.g., ₹65 Lakhs - ₹75 Lakhs depending on floor/area). Mention that registration/stamp duty is extra but there are current builder offers. Immediately ask a counter-question like whether they want 'ready possession' or 'under-construction', or when they can visit.
        3. COMPLEX NEGOTIATION: If they ask about heavy discounts, black/white money, or complex legal terms, gracefully say you need to check with your senior agent/owner and will call them back in 10 minutes. 
        4. KEEP IT SHORT: Conversational WhatsApp length. No long paragraphs.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": customer_message}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"❌ Chat AI Error: {e}")
        return "Sir, I am currently driving. I will call you back shortly!"