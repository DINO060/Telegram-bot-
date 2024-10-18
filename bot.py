import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Configuration du logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Remplacez par votre token bot Telegram ici
BOT_TOKEN = "7559751498:AAFAXiHq7ElW0F7nyI4BXoRqm6XXjY2Bl9c"


# Démarre le bot et envoie un message de bienvenue avec les boutons principaux
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Your Files 📁", callback_data="your_files")],
        [InlineKeyboardButton("Contact Us 📞", callback_data="contact_us")],
        [InlineKeyboardButton("Download Webtoon/Manga 📖", callback_data="download_manga")],
        [InlineKeyboardButton("Website 🌐", callback_data="website")],
        [InlineKeyboardButton("Language 🌐", callback_data="language")],
        [InlineKeyboardButton("How to Use This Bot ❓", callback_data="how_to_use")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome! Choose an option:",
        reply_markup=reply_markup
    )


# Gestion des clics sur les boutons
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "your_files":
        keyboard = [
            [InlineKeyboardButton("From Bot", callback_data="from_bot")],
            [InlineKeyboardButton("From Site", callback_data="from_site")],
            [InlineKeyboardButton("Delete Files 🗑", callback_data="delete_files")],
            [InlineKeyboardButton("Back 🔙", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Here you can get all your downloaded files:", reply_markup=reply_markup)

    elif query.data == "contact_us":
        await query.edit_message_text(
            "📬 Technical support and news\n"
            "CHANNEL: @BOTSUPPORTSITE\n"
            "Support group: @techbotit\n"
            "You are welcome to join!"
        )

    elif query.data == "download_manga":
        await query.edit_message_text("🔗 Click here to download Webtoons and Manga: https://example.com")

    elif query.data == "website":
        await query.edit_message_text("🌐 Visit our website: https://example.com")

    elif query.data == "language":
        await query.edit_message_text("Choose your language: English, Français, etc.")

    elif query.data == "how_to_use":
        await query.edit_message_text("📝 How to use the bot: https://telegra.ph/THE-BOT-10-17")

    elif query.data == "from_bot":
        await query.edit_message_text("Here are your files from the bot.")

    elif query.data == "from_site":
        await query.edit_message_text("Here are your files from the site.")

    elif query.data == "delete_files":
        await query.edit_message_text("🗑 All your files have been deleted.")

    elif query.data == "back":
        # Revenir au menu principal
        await start(update, context)


# Gestion des messages texte envoyés par l'utilisateur (pour les URL)
async def handle_message(update: Update, context):
    user_message = update.message.text

    # Supposons que l'utilisateur envoie une URL de média
    await update.message.reply_text(f"⌛️ Your request is processing...")

    # Simuler un téléchargement ici
    await asyncio.sleep(2)  # Simule un délai pour le traitement

    # Réponse après téléchargement
    await update.message.reply_text(f"✅ Download completed! [Media file] from {user_message}")


# Fonction principale pour démarrer le bot
async def main():
    # Créer l'application bot avec le token
    application = Application.builder().token(BOT_TOKEN).build()

    # Ajouter des gestionnaires de commandes et de messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Démarrer le bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.stop()


if __name__ == "__main__":
    asyncio.run(main())