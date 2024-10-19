import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Function to handle the /start command
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
    await update.message.reply_text(
        "I can extract and download for you photos/images/files/archives from Youtube, Instagram, TikTok, Facebook, Snapchat, X (formerly Twitter), Vimeo, VK, and 1000+ audio/video hostings. Just send me a URL to the post with media or direct link.",
        reply_markup=reply_markup
    )

# Function to handle messages with links
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" in url:
        await update.message.reply_text("Processing your URL... Please wait while I download the media.")
        # Add your download logic here
        await update.message.reply_text(f"Download complete for: {url}")
    else:
        await update.message.reply_text("Please send a valid URL.")

# Function to display the user's files
async def your_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Here are your downloaded files. (This is a placeholder for actual file list)")

# Function to delete files
async def delete_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="All files have been deleted. (This is a placeholder for actual deletion logic)")

# Function to handle the "How to Use" section
async def how_to_use(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="To use this bot, simply send a URL with media or a direct link, and I'll download it for you.")

# Function to handle language selection
async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("English", callback_data='lang_en')],
        [InlineKeyboardButton("Français", callback_data='lang_fr')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Choose your language:", reply_markup=reply_markup)

# Function to go back to the main menu
async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(query, context)

# Handler for button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'your_files':
        await your_files(update, context)
    elif query.data == 'contact_us':
        await query.edit_message_text(text="📬 Technical support and news. CHANNEL: @BOTSUPPORTSITE. Support group: @techbotit. You are welcome to join!")
    elif query.data == 'how_to_use':
        await how_to_use(update, context)
    elif query.data == 'language':
        await language(update, context)
    elif query.data == 'lang_en':
        await query.edit_message_text(text="Language changed to English.")
    elif query.data == 'lang_fr':
        await query.edit_message_text(text="La langue a été changée en Français.")
    elif query.data == 'delete_files':
        await delete_files(update, context)

# Main function to start the bot
async def main():
    # Initialize the bot
    application = Application.builder().token("7559751498:AAFAXiHq7ElW0F7nyI4BXoRqm6XXjY2Bl9c").build()

    # Add command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Add a message handler for normal text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add a callback query handler for button clicks
    application.add_handler(CallbackQueryHandler(button_handler))

    # Initialize the application
    await application.initialize()

    # Start the application
    await application.start()

    # Run the bot until manually stopped
    await application.idle()

if __name__ == "__main__":
    asyncio.run(main())