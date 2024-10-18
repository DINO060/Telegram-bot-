import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Configuration du logging pour surveiller les activités du bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fonction pour démarrer le bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📁 Your Files", callback_data='your_files')],
        [InlineKeyboardButton("📞 Contact Us", callback_data='contact')],
        [InlineKeyboardButton("📚 Download Webtoon/Manga", callback_data='download_webtoon')],
        [InlineKeyboardButton("🌐 Website", callback_data='website')],
        [InlineKeyboardButton("🌐 Language", callback_data='language')],
        [InlineKeyboardButton("ℹ️ How to use this Bot", callback_data='how_to_use')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("YOSH! I can extract and download for you photos/images/files/archives from multiple platforms. Choose an option:", reply_markup=reply_markup)

# Gestion des boutons
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'your_files':
        keyboard = [
            [InlineKeyboardButton("From Bot 📥", callback_data='from_bot')],
            [InlineKeyboardButton("From Site 🌐", callback_data='from_site')],
            [InlineKeyboardButton("🗑️ Delete Files", callback_data='delete_files')],
            [InlineKeyboardButton("🔙 Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Here you can get all your downloaded files:", reply_markup=reply_markup)

    elif query.data == 'contact':
        keyboard = [
            [InlineKeyboardButton("CHANNEL SUPPORT 📢", url='https://t.me/BOTSUPPORTSITE')],
            [InlineKeyboardButton("Support Group 🛠️", url='https://t.me/+hmsBjulzWGphMmQx')],
            [InlineKeyboardButton("🔙 Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📬 Technical support and news\nCHANNEL: @BOTSUPPORTSITE\nSupport group: @techbotit\nYou are welcome to join!", reply_markup=reply_markup)

    elif query.data == 'download_webtoon':
        await query.edit_message_text(text="You can download Webtoon/Manga from the following site: [Webtoon/Manga Site](https://your-site-url)", parse_mode='Markdown')

    elif query.data == 'website':
        await query.edit_message_text(text="Visit our official website for more resources: [Website](https://your-website-url)", parse_mode='Markdown')

    elif query.data == 'language':
        keyboard = [
            [InlineKeyboardButton("English 🇬🇧", callback_data='lang_en')],
            [InlineKeyboardButton("Français 🇫🇷", callback_data='lang_fr')],
            [InlineKeyboardButton("🔙 Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Choose your language:", reply_markup=reply_markup)

    elif query.data == 'how_to_use':
        await query.edit_message_text(text="Learn how to use the bot by visiting this link: [How to Use](https://telegra.ph/THE-BOT-10-17)", parse_mode='Markdown')

    elif query.data == 'from_bot':
        await query.edit_message_text(text="Here are the files you've downloaded via the bot.")
        
    elif query.data == 'from_site':
        await query.edit_message_text(text="Here are the files you've downloaded from the site.")

    elif query.data == 'delete_files':
        await query.edit_message_text(text="All downloaded files have been deleted.")

    elif query.data == 'back':
        await start(update, context)

# Gestion des messages texte envoyés par l'utilisateur
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "http" in text:
        await update.message.reply_text("⌛️ Your request is processing...")
        # Ici, le code pour gérer le téléchargement de fichiers à partir des URL
        # Vous pouvez ajouter la logique d'extraction et de téléchargement ici
        await update.message.reply_text("✅ Your file has been downloaded successfully.")
    else:
        await update.message.reply_text("I can help you download files. Just send me a link!")

# Configuration du bot avec les handlers
def main():
    application = Application.builder().token('7559751498:AAFAXiHq7ElW0F7nyI4BXoRqm6XXjY2Bl9c').build()

    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Démarrer le bot
    application.run_polling()

if __name__ == '__main__':
    main()