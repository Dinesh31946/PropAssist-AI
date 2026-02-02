from app.database.db_handler import init_db
import time
from app.services.email_cli import check_for_leads

def start_app():
    """
    Main loop that keeps the AI bot running.
    It checks for new leads every 60 seconds.
    """
    print("🚀 PropAssist.AI Bot is now running...")
    print("Watching for new leads in your Gmail inbox...")
    
    while True:
        try:
            # Call the function from your email_cli.py
            check_for_leads()
            
            # Pause the script for 1 minute before checking again
            # This prevents Gmail from blocking you for too many requests
            time.sleep(60)
            
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Retrying in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    init_db()  # Create the DB file as soon as the app starts
    start_app()