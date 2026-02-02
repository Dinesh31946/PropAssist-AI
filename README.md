# 🏢 PropAssist.AI: The 24/7 Real Estate Lead Concierge

![Status](https://img.shields.io/badge/Status-Active_Development-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![AI](https://img.shields.io/badge/Intelligence-OpenAI_GPT4o-orange)
![Database](https://img.shields.io/badge/Storage-SQLite-lightgrey)

> **"Speed to Lead is everything."** > PropAssist.AI reduces lead response time from **4 hours to 4 seconds**.

## 📖 Overview
In the Indian real estate market, 70% of portal leads (99acres, MagicBricks) go cold because agents are busy driving or sleeping. **PropAssist.AI** is a Micro-SaaS tool that acts as an "Infinite Assistant." 

It listens to your inbox, uses Large Language Models (LLMs) to understand if a lead is "Hot" or "Junk," and eventually triggers an instant WhatsApp alert to ensure no deal is ever lost.

## ⚡ Key Features (Phase 1 MVP)
* **🕵️ Targeted Lead Capture:** Uses advanced IMAP filtering to capture *only* fresh leads from portals (ignores personal spam).
* **🧠 AI Intent Scoring:** Uses OpenAI (`gpt-4o-mini`) to analyze the customer's message and assign a "Hot/Cold" score (0-100).
* **🧹 Robust Parsing:** Handles messy HTML emails and extracts clean data (Name, Phone, Property, Budget).
* **🗄️ Persistent Memory:** Automatically saves every lead into a local SQLite database for future reporting.
* **🛡️ Multi-Portal Ready:** Architecture designed to handle 99acres, MagicBricks, and Facebook Ads simultaneously.

## 🏗️ Architecture
```mermaid
graph LR
    A[Portal Email] -->|IMAP SSL| B(Email Listener)
    B -->|Raw Text| C{AI Brain}
    C -->|Analyze Intent| D[Structured Data]
    D -->|Save| E[(SQLite Database)]
    D -->|Trigger| F[WhatsApp Alert (Coming Soon)]

    🛠️ Installation & Setup
1. Clone the Repository
Bash
git clone [https://github.com/YourUsername/propassist-ai.git](https://github.com/YourUsername/propassist-ai.git)
cd propassist-ai
2. Set up Virtual Environment
Bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory and add your secrets:

Ini, TOML
# Email Configuration (App Password Required)
GMAIL_USER=your-email@gmail.com
GMAIL_PASS=your-16-char-app-password

# AI Configuration
OPENAI_API_KEY=sk-proj-your-openai-key

# Database Config (Optional)
DB_NAME=propassist.db
🚀 Usage
Run the main application entry point:

Bash
python main.py
Expected Output:

Plaintext
🚀 PropAssist.AI Bot is now running...
Watching for new leads in your Gmail inbox...
🎯 Targeted Search: Found 1 REAL leads. Processing...
🤖 PROPASSIST AI REPORT:
{"name": "Rajesh", "score": 95, "summary": "Urgent site visit request for Ulwe 2BHK"}
💾 Lead saved to database.
🗺️ Roadmap
[x] Phase 1: Foundation (Email Parsing & AI Scoring)

[ ] Phase 2: The Hook (WhatsApp Integration via Meta API)

[ ] Phase 3: Speed (Upgrade to IMAP IDLE for Instant Push)

[ ] Phase 4: Scale (Multi-Tenant SaaS Architecture)

🤝 Contributing
This project is currently in Private Beta. If you are a developer interested in the Real Estate AI space, feel free to open an Issue or submit a Pull Request.