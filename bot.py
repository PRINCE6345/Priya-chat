from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler,
    CallbackQueryHandler, filters, ContextTypes
)
from config import BOT_TOKEN, CHANNEL_USERNAME, CHANNEL_LINK, GF_NAME
from responses import get_gf_response


async def is_member(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in [
            ChatMember.MEMBER,
            ChatMember.ADMINISTRATOR,
            ChatMember.OWNER,
        ]
    except Exception:
        return False


async def send_join_prompt(update: Update):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Channel Join Karo", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ Join kar liya!", callback_data="check_join")],
    ])
    await update.message.reply_text(
        "🥺 Ruko ek second!\n\n"
        "Mujhse baat karne se pehle humara channel join karna hoga jaan...\n"
        "Join karo phir '✅ Join kar liya!' dabao — main wait kar rahi hoon! 💕",
        reply_markup=keyboard,
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "jaan"
    context.user_data.clear()

    if not await is_member(context.bot, update.effective_user.id):
        await send_join_prompt(update)
        return

    await update.message.reply_text(
        f"Heyy {user_name}! 🥰\n\n"
        f"Main hoon {GF_NAME} — teri virtual girlfriend 💕\n\n"
        "Baat kar mere se, kuch bhi pooch!\n"
        "Hindi, English, Hinglish — jo mann kare likh 😊"
    )


async def check_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_name = query.from_user.first_name or "jaan"

    if await is_member(context.bot, user_id):
        await query.edit_message_text(
            f"Yay! Aa gaye aakhir {user_name}! 🎉\n\n"
            f"Main hoon {GF_NAME} — teri virtual girlfriend 💕\n"
            "Ab baat kar mere se! 🥰"
        )
    else:
        await query.answer(
            "Abhi tak join nahi kiya? Pehle join karo jaan! 🥺",
            show_alert=True
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_member(context.bot, user_id):
        await send_join_prompt(update)
        return

    user_msg = update.message.text
    history = context.user_data.get("history", [])
    history.append(f"User: {user_msg}")
    if len(history) > 20:
        history = history[-20:]

    await context.bot.send_chat_action(update.effective_chat.id, action="typing")

    reply_text = get_gf_response(user_msg, history)

    history.append(f"{GF_NAME}: {reply_text}")
    context.user_data["history"] = history

    await update.message.reply_text(reply_text)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join_callback, pattern="^check_join$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print(f"💕 {GF_NAME} Bot chal rahi hai...")
    app.run_polling()


if __name__ == "__main__":
    main()
