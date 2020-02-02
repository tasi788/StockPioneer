from telegram.ext import run_async, CallbackContext
from telegram.update import Update

@run_async
def ping(update:Update, context: CallbackContext):
    """
    Ping Pong
    """
    update.message.reply_text('pong')
