
import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

# Simple in-memory UNO lobby
players = {}
game_open = True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎴 UNO Bot ready!\n\n"
        "/join - Join the UNO lobby\n"
        "/leave - Leave the lobby\n"
        "/close - Close the lobby (admin only)"
    )


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_open

    if not game_open:
        await update.message.reply_text("Lobby closed aanu.")
        return

    user = update.effective_user
    chat_id = update.effective_chat.id

    room = players.setdefault(chat_id, {})

    if user.id in room:
        await update.message.reply_text("Nee already lobby-il und!")
        return

    room[user.id] = user.full_name
    await update.message.reply_text(
        f"✅ {user.full_name} joined UNO!\n"
        f"Players: {len(room)}"
    )


async def leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    room = players.setdefault(chat_id, {})

    if user.id not in room:
        await update.message.reply_text("Nee lobby-il illa.")
        return

    del room[user.id]
    await update.message.reply_text(
        f"👋 {user.full_name} left the lobby.\n"
        f"Players: {len(room)}"
    )


async def close_lobby(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_open

    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id,
    )

    if member.status not in ("administrator", "creator"):
        await update.message.reply_text(
            "❌ Group admins mathrame /close use cheyyan pattuu."
        )
        return

    game_open = False
    await update.message.reply_text("🔒 UNO lobby closed!")


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable missing!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("leave", leave))
    app.add_handler(CommandHandler("close", close_lobby))

    print("UNO bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
