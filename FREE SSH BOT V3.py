import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token (updated)
BOT_TOKEN = "7986414215:AAFluxh_98kCd7wQxDTCnir1a-z16kIxRrM"

# States for the conversation
USERNAME_SSL, PASSWORD_SSL = range(2)
USERNAME_CF, PASSWORD_CF = range(2, 4)
NAME_NETMOD = range(4, 5)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Start message
        start_message = (
            "🌐 **Welcome to the Premium Account Creation Bot!** 🌐\n\n"
            "🔐 Instantly create **Cloudflare**, **SSL**, or **NetMod files** by selecting the options below. "
            "This bot is designed for ease of use and quick creation. Choose your preferred option and follow the steps!"
        )

        # Inline buttons
        keyboard = [
            [
                InlineKeyboardButton("Create Cloudflare", callback_data="create_cloudflare"),
                InlineKeyboardButton("Create SSL", callback_data="create_ssl"),
            ],
            [
                InlineKeyboardButton("Create NetMod File", callback_data="create_netmod"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the start message
        await update.message.reply_text(
            text=start_message, reply_markup=reply_markup, parse_mode="Markdown", 
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Error in /start: {e}")

# Inline button callback handler
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    try:
        if query.data == "create_cloudflare":
            await query.edit_message_text("Please send your Cloudflare Username.")
            return USERNAME_CF

        elif query.data == "create_ssl":
            await query.edit_message_text("Please send your SSL Username.")
            return USERNAME_SSL
        
        elif query.data == "create_netmod":
            await query.edit_message_text("Please send a name for your NetMod file.")
            return NAME_NETMOD
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")

# Handle name input for NetMod file
async def get_netmod_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file_name = update.message.text  # User's input
        context.user_data["netmod_name"] = file_name  # Store name

        # Generate the NetMod file link
        netmod_message = (
            f"trojan://SB20pgBBh5@cdn.rawgit.com:443?type=splithttp&host=aloneop.b-cdn.net&headerType=none&path=%252Falone&security=tls&sni=aloneop.b-cdn.net#{file_name}\n\n"
            "Copy and Paste This In NetMod\n\n"
            "This file is For Jio 4G"
        )
        await update.message.reply_text(netmod_message, parse_mode="Markdown")
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in get_netmod_name: {e}")

# Handle username input for Cloudflare
async def get_cf_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        username = update.message.text  # User's input
        context.user_data["username_cf"] = username  # Store username

        # Ask for password after receiving username
        await update.message.reply_text("Please send your Cloudflare Password.")
        return PASSWORD_CF
    except Exception as e:
        logger.error(f"Error in get_cf_username: {e}")

# Handle password input for Cloudflare
async def get_cf_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        password = update.message.text  # User's input
        username = context.user_data.get("username_cf")  # Retrieve stored username

        # Generate account creation details
        cloudflare_message = (
            "☁️ **Cloudflare Account Created!**\n\n"
            "• **Cloudflare Domain**: `cf-example.site`\n"
            f"• **Cloudflare User**: `{username}`\n"
            f"• **Cloudflare Pass**: `{password}`\n"
            "• **Logins**: `1`\n"
            "• **Expiration**: `60 Minutes`\n\n"
            f"• **To Use on HTTP Custom**: `cf-example.site:80@{username}:{password}`"
        )
        await update.message.reply_text(cloudflare_message, parse_mode="Markdown")
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in get_cf_password: {e}")

# Handle username input for SSL
async def get_ssl_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        username = update.message.text  # User's input
        context.user_data["username_ssl"] = username  # Store username

        # Ask for password after receiving username
        await update.message.reply_text("Please send your SSL Password.")
        return PASSWORD_SSL
    except Exception as e:
        logger.error(f"Error in get_ssl_username: {e}")

# Handle password input for SSL
async def get_ssl_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        password = update.message.text  # User's input
        username = context.user_data.get("username_ssl")  # Retrieve stored username

        # Generate account creation details
        ssl_message = (
            "𝗦𝗦𝗟 𝗗𝗶𝗿𝗲𝗰𝘁 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗖𝗿𝗲𝗮𝘁𝗲𝗱 ;)\n\n"
            "• 𝙎𝙎𝙇 𝙄𝙋 : `46.101.229.158`\n"
            "• 𝙎𝙎𝙇 𝘿𝙊𝙈𝘼𝙄𝙉 : `ws-freevps.amineba.site`\n"
            f"• 𝙎𝙎𝙇 𝙐𝙨𝙚𝙧: `{username}`\n"
            f"• 𝙎𝙎𝙇 𝙋𝙖𝙨𝙨: `{password}`\n"
            "• 𝙀𝙭𝙥𝙞𝙧𝙖𝙩𝙞𝙤𝙣 : `60 Minutes`\n\n"
            f"•  𝙎𝙎𝙃 𝙎𝙎𝙇 / 𝙏𝙇𝙎 : `46.101.229.158:443@{username}:{password}`"
        )
        await update.message.reply_text(ssl_message, parse_mode="Markdown")
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in get_ssl_password: {e}")

# Cancel the conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Process canceled.")
    return ConversationHandler.END

# Main function
def main():
    # Create the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Set up conversation handlers
    conversation_handler_netmod = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="create_netmod")],
        states={
            NAME_NETMOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_netmod_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    conversation_handler_cf = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="create_cloudflare")],
        states={
            USERNAME_CF: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_cf_username)],
            PASSWORD_CF: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_cf_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    conversation_handler_ssl = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="create_ssl")],
        states={
            USERNAME_SSL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ssl_username)],
            PASSWORD_SSL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ssl_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conversation_handler_netmod)
    application.add_handler(conversation_handler_cf)
    application.add_handler(conversation_handler_ssl)

    # Start the bot
    logger.info("🤖 Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()