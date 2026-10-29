import os
import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Welcome to Music Bot!\n\n"
        "Song name লিখে পাঠাও। আমি গান খুঁজে দেব।"
    )


async def search_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    try:
        response = requests.get(
            "https://api.jamendo.com/v3.0/tracks/",
            params={
                "client_id": "f6f3b7a7",
                "format": "json",
                "limit": 5,
                "search": query,
                "audioformat": "mp32",
            },
            timeout=20,
        )
        response.raise_for_status()
        tracks = response.json().get("results", [])

        if not tracks:
            await update.message.reply_text("😕 গান পাওয়া যায়নি। অন্য নাম দিয়ে চেষ্টা করো।")
            return

        for track in tracks:
            title = track.get("name", "Unknown")
            artist = track.get("artist_name", "Unknown")
            audio = track.get("audio")

            if audio:
                await update.message.reply_audio(
                    audio=audio,
                    title=title,
                    performer=artist,
                )
            else:
                await update.message.reply_text(
                    f"🎵 {title} — {artist}\n{track.get('shareurl', '')}"
                )

    except Exception:
        await update.message.reply_text(
            "গান খুঁজতে সমস্যা হয়েছে। পরে আবার চেষ্টা করো।"
        )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_music))
    app.run_polling()


if __name__ == "__main__":
    main()
