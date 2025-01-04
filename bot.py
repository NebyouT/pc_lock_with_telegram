import requests
import time
import os
import ctypes

# Telegram Bot Token
BOT_TOKEN = "7599478700:AAGcJoNa9_BRPP3_SVuakF0nH9pn3TqjWPw"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
LAST_UPDATE_ID = None

def get_updates():
    """Fetch updates from the Telegram bot."""
    global LAST_UPDATE_ID
    params = {"offset": LAST_UPDATE_ID + 1} if LAST_UPDATE_ID else {}
    response = requests.get(API_URL, params=params)
    if response.ok:
        return response.json()
    else:
        print("Failed to fetch updates")
        return None

def perform_task():
    """Task to perform when the text is 'locked'."""
    print("Locking the PC...")
    # Lock the PC
    if os.name == "nt":  # Windows
        ctypes.windll.user32.LockWorkStation()
    else:
        print("Locking is only supported on Windows systems.")

def listen_and_respond():
    """Continuously listen for updates and respond if text is 'locked'."""
    global LAST_UPDATE_ID
    while True:
        updates = get_updates()
        if updates and updates.get("result"):
            for update in updates["result"]:
                LAST_UPDATE_ID = update["update_id"]
                # Check if the update contains a message with text
                if "message" in update and "text" in update["message"]:
                    text = update["message"]["text"]
                    print(f"Received message: {text}")
                    # Perform task if text matches 'locked'
                    if text.lower() == "locked":
                        perform_task()
        time.sleep(2)  # Polling delay to avoid excessive API calls

if __name__ == "__main__":
    listen_and_respond()
