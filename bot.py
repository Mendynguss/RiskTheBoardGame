import asyncio
from telegram import Update, InlineQueryResultGame
from telegram.ext import Application, CommandHandler, InlineQueryHandler, CallbackQueryHandler, ContextTypes
import logging
import uuid

# --- CONFIGURATION ---
BOT_TOKEN = "8071872516:AAFKDXIJepWgl8z1NQuzerhjSeQLmfHW_Uk"  # Replace with your actual token from BotFather
GAME_SHORT_NAME = "risiko" # This MUST match the short name you set in BotFather

# ++ NEW PART: This is where your game is hosted! ++
# Replace this with the URL from GitHub Pages or another host.
GAME_URL = "https://mendynguss.github.io/RiskTheBoardGame/" 

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- BOT HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the command /start is issued."""
    await update.message.reply_text(
        "Hi! To play Risiko, go to any chat, type my username (@RiskBoardGameBot) "
        "and a space, then choose the game to start."
    )

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query to show the game. This part remains the same."""
    query = update.inline_query.query
    logger.info(f"Received inline query: {query}")
    results = [
        InlineQueryResultGame(
            id=str(uuid.uuid4()),
            game_short_name=GAME_SHORT_NAME,
        )
    ]
    await update.inline_query.answer(results)

# ++ NEW PART: This function handles the "Play" button press ++
async def game_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the callback query from the 'Play' button."""
    query = update.callback_query
    # Check if the callback is for our specific game
    if query.game_short_name == GAME_SHORT_NAME:
        # Answer the callback query by providing the URL
        await query.answer(url=GAME_URL)
    else:
        # If the callback is for some other reason, just acknowledge it.
        await query.answer("Sorry, I can't handle this request.", show_alert=True)


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))
    
    # ++ NEW PART: Register the handler for the "Play" button ++
    application.add_handler(CallbackQueryHandler(game_callback))

    # Run the bot
    print("Bot is running... Press Ctrl-C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()