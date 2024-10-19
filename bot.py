import os
import asyncio
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Set your bot token here
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# List of supported domains (you can add more)
SUPPORTED_DOMAINS = ["youtube.com", "vimeo.com", "instagram.com", "tiktok.com"]

# Function to download media from URL
async def download_media(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                return response.content
            else:
                return None
        except Exception as e:
            print(f"Failed to download media: {e}")
            return None

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📂 Your Files", callback_data='your_files'),
            InlineKeyboardButton("🌐 Website", url="https://yourwebsite.com")
        ],
        [
            InlineKeyboardButton("🛠️ Contact Us", callback_data='contact_us'),
            InlineKeyboardButton("📚 How to Use", callback_data='how_to_use')
        ],
        [InlineKeyboardButton("🌍 Language", callback_data='language')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the bot! Choose an option:", reply_markup=reply_markup)

# Handle messages with URLs
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Check if the message contains a URL
    if any(domain in text for domain in SUPPORTED_DOMAINS):
        await update.message.reply_text("Downloading media from the provided URL...")
        
        # Download the media
        media_content = await download_media(text)
        if media_content:
            await update.message.reply_text("Media downloaded successfully!")
            # Send the media back to the user
            await context.bot.send_document(chat_id=update.effective_chat.id, document=media_content)
        else:
            await update.message.reply_text("Failed to download media. Please try again.")
    else:
        await update.message.reply_text("Please provide a valid media URL.")

# Show files handler
async def show_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("From Bot", callback_data='from_bot')],
        [InlineKeyboardButton("From Site", callback_data='from_site')],
        [InlineKeyboardButton("🗑️ Delete Files", callback_data='delete_files')],
        [InlineKeyboardButton("⬅️ Back", callback_data='back_to_main')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Here you can get all your downloaded files:", reply_markup=reply_markup)

# Contact us handler
async def contact_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "📬 Technical support and news\n"
        "CHANNEL: @BOTSUPPORTSITE\n"
        "Support group: @techbotit\n"
        "You are welcome to join!"
    )
    keyboard = [
        [InlineKeyboardButton("⬅️ Back", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

# How to use handler
async def how_to_use(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text="Here is how to use this bot: https://telegra.ph/THE-BOT-10-17")

# Language handler
async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("English", callback_data='lang_en')],
        [InlineKeyboardButton("Français", callback_data='lang_fr')],
        [InlineKeyboardButton("⬅️ Back", callback_data='back_to_main')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Choose your language:", reply_markup=reply_markup)

# Handle button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'your_files':
        await show_files(update, context)
    elif query.data == 'contact_us':
        await contact_us(update, context)
    elif query.data == 'how_to_use':
        await how_to_use(update, context)
    elif query.data == 'language':
        await language(update, context)
    elif query.data == 'back_to_main':
        await start(update, context)

# Main function to start the bot
async def main():
    # Initialize the bot
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Message handler for normal text messages (with URLs)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Callback query handler for inline button presses
    application.add_handler(CallbackQueryHandler(button_handler))

    # Initialize the application
    await application.initialize()

    # Start the application
    await application.start()

    # Run the bot until manually stopped
    await application.idle()

if __name__ == "__main__":
    asyncio.run(main())