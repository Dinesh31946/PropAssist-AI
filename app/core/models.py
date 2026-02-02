from dataclasses import dataclass
from datetime import datetime

@dataclass
class Lead:
    source: str          # e.g., '99acres'
    customer_name: str
    customer_phone: str
    property_id: str
    inquiry_text: str    # The raw message
    timestamp: datetime = datetime.now()
    score: int = 0       # To be filled by Scorer
    status: str = "new"  # new, qualified, hot, junk