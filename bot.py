import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import httpx

BOT_TOKEN = "7897628824:AAGL-WQl8PAUQ1TJBeMd2EOMI1No6fDbNgY"

# Démarrage du bot
async def start(update: Update, context):
    keyboard = [
        [
            InlineKeyboardButton("📂 Your File", callback_data='files'),
            InlineKeyboardButton("ℹ️ Contact Us", callback_data='contact')
        ],
        [
            InlineKeyboardButton("📚 Download Webtoon/Manga", callback_data='download_webtoon'),
            InlineKeyboardButton("🌐 Website", callback_data='website')
        ],
        [
            InlineKeyboardButton("🌍 Language", callback_data='language'),
            InlineKeyboardButton("📖 How to use this Bot", url='https://telegra.ph/THE-BOT-10-17')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome to the bot! Choose an option:", reply_markup=reply_markup)

# Gérer les boutons du clavier inline
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'files':
        keyboard = [
            [
                InlineKeyboardButton("📥 From Bot", callback_data='from_bot'),
                InlineKeyboardButton("🌐 From Site", callback_data='from_site')
            ],
            [
                InlineKeyboardButton("🗑️ Delete Files", callback_data='delete_files'),
                InlineKeyboardButton("🔙 Back", callback_data='back')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Here you can get all your downloaded files:", reply_markup=reply_markup)

    elif query.data == 'contact':
        keyboard = [
            [
                InlineKeyboardButton("📬 CHANNEL SUPPORT", url='https://t.me/BOTSUPPORTSITE'),
                InlineKeyboardButton("🛠 Groupe Support", url='https://t.me/techbotit')
            ],
            [InlineKeyboardButton("🔙 Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📬 Technical support and news. CHANNEL: @BOTSUPPORTSITE. Support group: @techbotit. You are welcome to join!", reply_markup=reply_markup)

    elif query.data == 'download_webtoon':
        await query.edit_message_text("🌐 Please visit our website to download Webtoon/Manga: [Website](https://example.com)")

    elif query.data == 'website':
        await query.edit_message_text("🌐 Please visit our website: [Website](https://example.com)")

    elif query.data == 'language':
        keyboard = [
            [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'), InlineKeyboardButton("🇫🇷 Français", callback_data='lang_fr')],
            [InlineKeyboardButton("🔙 Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Choose your language: English, Français", reply_markup=reply_markup)

    elif query.data == 'back':
        await start(query, context)

# Gérer le téléchargement des fichiers
async def download_file(update: Update, context):
    url = update.message.text
    if "http" in url:
        await update.message.reply_text("⌛️ Your request is processing...")

        # Exemple de gestion du téléchargement avec HTTPX
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                filename = "downloaded_file"
                with open(filename, 'wb') as f:
                    f.write(response.content)

                await update.message.reply_document(document=open(filename, 'rb'), caption=f"📁 {filename} has been downloaded.")
                os.remove(filename)

            except Exception as e:
                await update.message.reply_text(f"❌ Failed to download file. Error: {e}")
    else:
        await update.message.reply_text("❌ Please provide a valid URL.")

# Initialisation de l'application
async def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Initialiser l'application
    await application.initialize()

    # Gestion des commandes
    application.add_handler(CommandHandler("start", start))

    # Gestion des interactions avec les boutons
    application.add_handler(CallbackQueryHandler(button))

    # Gestion des messages contenant des liens
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_file))

    # Démarrer le bot
    await application.start()
    await application.idle()

if __name__ == "__main__":
    asyncio.run(main())