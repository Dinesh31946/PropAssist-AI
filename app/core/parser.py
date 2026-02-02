import re

def extract_basic_info(raw_email_body):
    """
    Beginner Version: Using Regex to find a phone number.
    Advanced Version: We will later replace this with an LLM call.
    """
    # Look for 10 consecutive digits
    phone_match = re.search(r'\d{10}', raw_email_body)
    phone = phone_match.group(0) if phone_match else "Unknown"
    
    # Simple split to find a name (this is just a placeholder)
    name = "New Lead" 
    
    return name, phone