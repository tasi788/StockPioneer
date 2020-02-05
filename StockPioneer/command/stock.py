from html import escape

from telegram.update import Update
from telegram.ext import run_async, CallbackContext
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode

import yfinance as yf


def stock(update: Update, context: CallbackContext):
    """
    response stock info
    """
    query = update.inline_query.query.upper()
    if query == '':
        result = [
            InlineQueryResultArticle(
                id=update.inline_query.id,
                title=f"📃 使用說明",
                thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/237/page-with-curl_1f4c3.png',
                input_message_content=InputTextMessageContent(
                    f"在輸入欄輸入 <code>@StockPioneer_bot AAPL</code> 試試？",
                    parse_mode=ParseMode.HTML))
        ]
        update.inline_query.answer(result)
        return

    try:
        query_stock = yf.Ticker(query).info
    except (KeyError, IndexError):
        # 找不到
        result = [
            InlineQueryResultArticle(
                id=update.inline_query.id,
                title=f"🚫 找不到 {query} 代號 🚫",
                thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/237/no-entry_26d4.png',
                input_message_content=InputTextMessageContent(
                    f"🚫 找不到 <code>{escape(query)}</code> 代號 🚫",
                    parse_mode=ParseMode.HTML))
        ]
        update.inline_query.answer(result, cache_time=0)
        return False
    else:
        # 找到ㄌ
        text = '代號：<code>{query}</code>\n' \
            '買：<code>{ask}</code>\n' \
            '賣：<code>{bid}</code>'.format(
                query=escape(query),
                ask=query_stock['ask'],
                bid=query_stock['bid']
            )
        result = [

            InlineQueryResultArticle(
                id=update.inline_query.id,
                title=f"📝 顯示 {query} 結果",
                thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/237/memo_1f4dd.png',
                input_message_content=InputTextMessageContent(text, parse_mode=ParseMode.HTML))
        ]
        update.inline_query.answer(result, cache_time=120)
