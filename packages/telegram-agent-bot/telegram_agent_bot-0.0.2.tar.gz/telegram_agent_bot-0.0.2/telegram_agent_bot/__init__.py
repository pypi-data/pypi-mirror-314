from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Bot
from telegram_agent_bot.client import send_message


chat_ids = None
token = None
_generate_agent_fn = None


CLIENTS = {
}


def generate_client_function(chat_id):
    def send_msg_to_user(msg: str):
        """Send a message to the user. Use this function to send messages to the user, not just return text string. Text string that you generate(that is not passed to this function) can be random. User will not see it."""
        send_message(chat_id, msg, token)
    return send_msg_to_user


async def drop_client(update, context):
    if str(update.message.chat_id) not in chat_ids:
        return
    CLIENTS.pop(update.message.chat_id, None)
    await update.message.reply_text("Client dropped.")


async def message(update, context):
    global _generate_agent_fn
    if chat_ids and update and update.message and str(update.message.chat_id) not in chat_ids:
        return
    clt = CLIENTS.get(update.message.chat_id, None)
    if not clt:
        clt = _generate_agent_fn(on_message=generate_client_function(str(update.message.chat_id)))
        CLIENTS[update.message.chat_id] = clt
    clt.send_message(update.message.text, )


async def get_chat_id(update, context):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Your chat ID is: {chat_id}")


def start_agent_bot(*, telegram_token, telegram_chat_ids=None, generate_agent_fn):
    global _generate_agent_fn
    global chat_ids
    global token
    _generate_agent_fn = generate_agent_fn
    token = telegram_token
    chat_ids = telegram_chat_ids
    bot = Bot(token=telegram_token)
    application = Application.builder().bot(bot).build()
    drop_client_handler = CommandHandler('drop_client', drop_client)
    application.add_handler(drop_client_handler)
    get_chat_id_handler = CommandHandler('get_chat_id', get_chat_id)
    application.add_handler(get_chat_id_handler)    

    main_handler = MessageHandler(filters.TEXT, message)
    application.add_handler(main_handler)

    application.run_polling()