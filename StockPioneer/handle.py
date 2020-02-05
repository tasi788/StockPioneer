import logging
import coloredlogs

from telegram.error import *
from telegram.utils.request import Request
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler
from telegram.ext import Filters, messagequeue, InlineQueryHandler

from .plugins import config, mq
from .command import ping, stock

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


class handle:
    def __init__(self):
        pass

    def run(self):
        token = config.get('bot', 'token')
        # for test purposes limit global throughput to 30 messages per 2 sec
        queue = messagequeue.MessageQueue(
            all_burst_limit=3, all_time_limit_ms=3000)
        request = Request(con_pool_size=132)
        bot = mq.MQBot(token, request=request, mqueue=queue)
        updater = Updater(bot=bot, use_context=True)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler('ping', ping))
        dp.add_handler(InlineQueryHandler(stock))

        logger.info(bot.get_me().first_name)
        try:
            updater.start_polling(clean=False, timeout=60)
        except KeyboardInterrupt:
            updater.stop()
            updater.is_idle = False
