from telegram import ChatAction
from telegram.ext import Updater
import logging
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
updater = Updater(TOKEN, use_context=True)
bot = updater.bot


def forward_files(context):
    logger.info("Fetching and forwarding files...")
    files = context.bot.get_chat(SOURCE_CHANNEL_ID).get_files(limit=FORWARD_BATCH_SIZE)
    for file in files:
        context.bot.send_chat_action(chat_id=TARGET_CHANNEL_ID, action=ChatAction.TYPING)
        context.bot.forward_document(chat_id=TARGET_CHANNEL_ID, from_chat_id=SOURCE_CHANNEL_ID, message_id=file.message_id)
        time.sleep(1)  # Delay between forwarding each file to avoid flood


def main():
    # Forward files from source channel when bot starts
    forward_files(updater)

    # Schedule forwarding every 10 minutes
    schedule.every(FORWARD_INTERVAL_MINUTES).minutes.do(forward_files, updater)

    # Run scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
