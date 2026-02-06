import time
import schedule
from app.database.db_handler import init_db
from app.services.email_cli import check_for_leads

# --- CONFIGURATION ---
CHECK_INTERVAL_SECONDS = 20  # Runs every 20 seconds

def start_bot():
    print("🚀 PropAssist.AI Bot is initializing...")
    
    # 1. Initialize Database
    init_db()
    print("🗄️ Database initialized successfully.")

    # 2. Run the check immediately once (so you don't have to wait 20s for the first run)
    print("⚡ Doing an initial quick scan...")
    check_for_leads()

    # 3. Schedule the loop
    print(f"👀 Watching for new leads every {CHECK_INTERVAL_SECONDS} seconds...")
    schedule.every(CHECK_INTERVAL_SECONDS).seconds.do(check_for_leads)

    print("🟢 Bot is LIVE. Press Ctrl+C to stop.")

    # 4. Infinite Loop (Keeps the script running forever)
    try:
        while True:
            schedule.run_pending()
            time.sleep(1) # Sleep 1s to save CPU
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user.")

if __name__ == "__main__":
    start_bot()