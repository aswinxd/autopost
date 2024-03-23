import telegram
import schedule
import time
from config import TOKEN, SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID

# Initialize bot
bot = telegram.Bot(token=TOKEN)

def forward_videos():
    messages = bot.get_chat_history(chat_id=SOURCE_CHANNEL_ID, limit=6)
    for message in messages:
        if message.video:
            bot.forward_message(chat_id=TARGET_CHANNEL_ID, from_chat_id=SOURCE_CHANNEL_ID, message_id=message.message_id)

# Schedule forwarding every 20 minutes
schedule.every(20).minutes.do(forward_videos)

# Main loop
while True:
    schedule.run_pending()
    time.sleep(1)
