from pyrogram import Client
from pyrogram.errors import FloodWait
from config import API_ID, API_HASH, SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID
import time

# Configuration parameters
FORWARD_BATCH_SIZE = 6
FORWARD_INTERVAL_MINUTES = 10

# Initialize Pyrogram client
app = Client("my_account", api_id=API_ID, api_hash=API_HASH)


@app.on_message()
def forward_videos(client, message):
    # Ensure the message is from the source channel and is a video
    if message.chat.id == SOURCE_CHANNEL_ID and message.video:
        try:
            # Forward the message to the target channel
            client.forward_messages(chat_id=TARGET_CHANNEL_ID, from_chat_id=SOURCE_CHANNEL_ID, message_ids=message.message_id)
            print("Video forwarded successfully.")
        except FloodWait as e:
            print(f"Sleeping for {e.x} seconds.")
            time.sleep(e.x)
        except Exception as e:
            print(f"Error: {e}")


def main():
    with app:
        # Fetch and forward messages from source channel when bot starts
        messages = app.get_chat_history(chat_id=SOURCE_CHANNEL_ID, limit=FORWARD_BATCH_SIZE)
        for message in messages:
            if message.video:
                app.send_message(chat_id=TARGET_CHANNEL_ID, text="Forwarding video...")
                app.forward_messages(chat_id=TARGET_CHANNEL_ID, from_chat_id=SOURCE_CHANNEL_ID, message_ids=message.message_id)
                time.sleep(1)  # Delay between forwarding each message to avoid flood

        # Schedule forwarding every 10 minutes
        while True:
            messages = app.get_chat_history(chat_id=SOURCE_CHANNEL_ID, limit=FORWARD_BATCH_SIZE)
            for message in messages:
                if message.video:
                    app.send_message(chat_id=TARGET_CHANNEL_ID, text="Forwarding video...")
                    app.forward_messages(chat_id=TARGET_CHANNEL_ID, from_chat_id=SOURCE_CHANNEL_ID, message_ids=message.message_id)
                    time.sleep(1)  # Delay between forwarding each message to avoid flood
            time.sleep(FORWARD_INTERVAL_MINUTES * 60)


if __name__ == '__main__':
    main()
