"""
Telegram News Classification Bot
---------------------------------

This bot receives a text message from the user and predicts
its news category using a trained NLP model (TF-IDF + RandomForest).

Categories:
- Politics
- Rights
- Education
- Sport
"""

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram import Update
from dotenv import load_dotenv
import joblib
import os


# -------------------------------------------------
# Load environment variables (.env file)
# -------------------------------------------------
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables.")


# -------------------------------------------------
# Load trained ML model (Pipeline: TF-IDF + RandomForest)
# -------------------------------------------------
try:
    model = joblib.load("model/nlp_model.pkl")
    print("Model loaded successfully.")
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")


# -------------------------------------------------
# Command: /help
# -------------------------------------------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends instructions to the user.
    """
    await update.message.reply_text(
        "Send me a news message and I will predict its category:\n"
        "• Politics\n"
        "• Rights\n"
        "• Education\n"
        "• Sport"
    )


# -------------------------------------------------
# Message Handler (Main Prediction Logic)
# -------------------------------------------------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles incoming text messages and predicts category.
    """
    user_text = update.message.text

    # Make prediction
    prediction = model.predict([user_text])[0]

    # Send response
    await update.message.reply_text(
        f"📰 Predicted Category: {prediction}"
    )


# -------------------------------------------------
# Main function (Bot setup and execution)
# -------------------------------------------------
def main():
    """
    Initializes and starts the Telegram bot.
    """
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("help", help_command))

    # Register text message handler (ignore commands)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler)
    )

    print("Bot is running...")
    app.run_polling()


# Run the bot
if __name__ == "__main__":
    main()