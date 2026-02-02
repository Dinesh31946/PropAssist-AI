import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Initialization
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_lead_with_ai(email_body):
    """
    This function sends the raw email to OpenAI and returns structured data.
    """
    try:
        # 2. The AI Request
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # We use 'mini' because it's 10x cheaper and very fast
            messages=[
                {
                    "role": "system", 
                    "content": """
                    You are a professional Real Estate Assistant. 
                    Your job is to read messy emails and extract:
                    - Customer Name (If not found, use 'Interested Client')
                    - Property Name/Location mentioned.
                    - Intent Score (0 to 100): 
                        - 90+ if they want a site visit/call.
                        - 50-80 if they are just asking for price/details.
                        - Below 50 if they seem like a bot or casual browser.
                    
                    Return ONLY a JSON-style string like this:
                    {"name": "Name", "property": "Location", "score": 85, "summary": "One sentence summary"}
                    """
                },
                {"role": "user", "content": email_body}
            ],
            temperature=0.3 # Low temperature makes the AI more consistent and less 'creative'
        )
        
        # 3. Return the result
        return response.choices[0].message.content

    except Exception as e:
        return f"Error connecting to AI: {e}"