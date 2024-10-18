import os
import requests
import yt_dlp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Function to download a video using yt-dlp
def download_video(url, output_path):
    ydl_opts = {
        'outtmpl': output_path + '/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Function to download a file (images, PDFs, etc.)
def download_file(url, output_path):
    response = requests.get(url, stream=True)
    file_name = url.split("/")[-1]
    full_path = os.path.join(output_path, file_name)

    with open(full_path, 'wb') as f:
        f.write(response.content)
    return full_path

# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎥 Download Video", callback_data='download_video')],
        [InlineKeyboardButton("🖼 Download Image", callback_data='download_image')],
        [InlineKeyboardButton("📂 Your Files", callback_data='your_files')],
        [InlineKeyboardButton("ℹ️ How to Use", callback_data='how_to_use')],
        [InlineKeyboardButton("🌐 Change Language", callback_data='language')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome! Choose an option below:",
        reply_markup=reply_markup
    )

# Handle messages containing URLs
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id

    if "youtube.com" in user_message or "vimeo.com" in user_message:
        output_dir = "downloads/videos"
        os.makedirs(output_dir, exist_ok=True)
        await update.message.reply_text("⌛️ Your request is processing...")
        download_video(user_message, output_dir)
        await update.message.reply_text("✅ Video downloaded successfully!")
    elif user_message.startswith("http"):
        output_dir = "downloads/files"
        os.makedirs(output_dir, exist_ok=True)
        await update.message.reply_text("⌛️ Your request is processing...")
        downloaded_file = download_file(user_message, output_dir)
        await update.message.reply_document(document=downloaded_file, caption="📥 File downloaded successfully!")
    else:
        await update.message.reply_text("❗️ Please send a valid URL to download files.")

# Handle inline button interactions
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "download_video":
        await query.edit_message_text("🎬 Please send the video link.")
    elif query.data == "download_image":
        await query.edit_message_text("🖼 Please send the image link.")
    elif query.data == "your_files":
        # Show downloaded files
        await query.edit_message_text("📂 Here you can get all your downloaded files.")
    elif query.data == "how_to_use":
        await query.edit_message_text("ℹ️ To use this bot, simply send a link to download media files.")
    elif query.data == "language":
        await query.edit_message_text("🌐 Choose your language: English, Français, etc.")

# Main function for the bot
async def main():
    application = Application.builder().token("7559751498:AAFAXiHq7ElW0F7nyI4BXoRqm6XXjY2Bl9c").build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot
    await application.start()
    await application.wait_stop()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())