import logging
import coloredlogs

import telegram.bot
from telegram import user
from telegram.error import *
from telegram.utils.request import Request
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler
from telegram.ext import Filters, messagequeue, CallbackQueryHandler

from . import config


logger = logging.getLogger(__name__)
coloredlogs.install(config.get('logging', 'level'))


class MQBot(telegram.bot.Bot):
    """A subclass of Bot which delegates send method handling to MQ"""

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or messagequeue.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @messagequeue.queuedmessage
    def send_message(self, *args, **kwargs):
        """Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments"""
        try:
            return super(MQBot, self).send_message(*args, **kwargs)
        except (BadRequest, TimedOut, Unauthorized) as e:
            if e.message == 'Reply message not found':
                # logger.warning('msg has deleted.')
                kwargs.pop('reply_to_message_id', None)
                return super(MQBot, self).send_message(*args, **kwargs)
            elif e.message == 'Timed out':
                logger.warning('Timed out.')
            elif e.message == "Forbidden: bot can't initiate conversation with a user":
                logger.warning('cannot reach that guys')
            elif e.message == 'Forbidden: bot is not a member of the supergroup chat':
                logger.warning('new left from group')
                # raise
            else:
                logger.exception(e)
                logger.warning(args)
                logger.warning(kwargs)
            logger.warn(args)
            logger.warn(kwargs)

    @messagequeue.queuedmessage
    def edit_message_text(self, *args, **kwargs):
        return super(MQBot, self).edit_message_text(*args, **kwargs)

    @messagequeue.queuedmessage
    def edit_message_reply_markup(self, *args, **kwargs):
        return super(MQBot, self).edit_message_reply_markup(*args, **kwargs)

    @messagequeue.queuedmessage
    def get_chat_administrators(self, *args, **kwargs):
        return super(MQBot, self).get_chat_administrators(*args, **kwargs)

    @messagequeue.queuedmessage
    def delete_message(self, *args, **kwargs):
        try:
            return super(MQBot, self).delete_message(*args, **kwargs)
        except (BadRequest, TimedOut, Unauthorized) as e:
            if e.message == 'Message to delete not found':
                pass