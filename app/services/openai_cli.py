import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def analyze_lead_with_ai(email_body):
    print("🧠 AI is analyzing...")
    
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = """
        You are a Real Estate Lead Extractor.
        
        INPUT: An email body (Direct or Forwarded).
        TASK:
        1. Ignore "Forwarded message" headers (From, Date, To) at the top.
        2. Find the ORIGINAL Customer Name and Property details.
        3. Rate 'score' (0-100) based on urgency ("Immediate", "Visit tomorrow" = High).
        4. Create a 1-sentence 'summary'.
        
        OUTPUT JSON ONLY:
        {"name": "Name", "property": "Property", "score": 90, "summary": "Summary"}
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
        
        # Import dynamically to avoid circular error
        from app.services.email_cli import save_lead_to_db_and_alert
        save_lead_to_db_and_alert(ai_analysis)

    except Exception as e:
        print(f"❌ AI Error: {e}")