import asyncio
from telegram import Update, InlineQueryResultGame
from telegram.ext import Application, CommandHandler, InlineQueryHandler, ContextTypes
import logging
import uuid

# --- CONFIGURATION ---
BOT_TOKEN = "8071872516:AAFKDXIJepWgl8z1NQuzerhjSeQLmfHW_Uk"  # Replace with your actual token from BotFather
GAME_SHORT_NAME = "risiko"  # This MUST match the short name you set in BotFather

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- BOT HANDLERS ---

# This function handles the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the command /start is issued."""
    await update.message.reply_text(
        "Hi! To play Risiko, go to any chat, type my username (@RiskBoardGameBot) "
        "and a space, then choose the game to start."
    )

# This function handles inline queries. This is how players will start your game.
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query to show the game."""
    query = update.inline_query.query
    logger.info(f"Received inline query: {query}")

    # The result of the inline query will be a single Game object
    results = [
        InlineQueryResultGame(
            id=str(uuid.uuid4()),  # Unique ID for this result
            game_short_name=GAME_SHORT_NAME,
        )
    ]

    await update.inline_query.answer(results)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non-command i.e message - echo the message on Telegram
    application.add_handler(InlineQueryHandler(inline_query))

    # Run the bot until the user presses Ctrl-C
    print("Bot is running... Press Ctrl-C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()