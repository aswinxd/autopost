import logging
from telegram import Bot, ChatAction
import schedule
import time
from config import TOKEN, SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID

# Configuration parameters
FORWARD_BATCH_SIZE = 6
FORWARD_INTERVAL_MINUTES = 10

# Initialize logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot
bot = Bot(TOKEN)


def forward_videos():
    messages = bot.get_chat_history(chat_id=SOURCE_CHANNEL_ID, limit=FORWARD_BATCH_SIZE)
    for message in messages:
        if message.video:
            bot.forward_message(chat_id=TARGET_CHANNEL_ID, from_chat_id=SOURCE_CHANNEL_ID, message_id=message.message_id)


def fetch_and_forward_messages():
    logger.info("Fetching and forwarding messages...")
    messages = bot.get_chat_history(chat_id=SOURCE_CHANNEL_ID)
    for message in messages:
        if message.video:
            bot.send_chat_action(chat_id=TARGET_CHANNEL_ID, action=ChatAction.TYPING)
            bot.forward_message(chat_id=TARGET_CHANNEL_ID, from_chat_id=SOURCE_CHANNEL_ID, message_id=message.message_id)
            time.sleep(1)  # Delay between forwarding each message to avoid flood


def main():
    # Fetch and forward messages from source channel when bot starts
    fetch_and_forward_messages()

    # Schedule forwarding every 10 minutes
    schedule.every(FORWARD_INTERVAL_MINUTES).minutes.do(fetch_and_forward_messages)

    # Run scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
