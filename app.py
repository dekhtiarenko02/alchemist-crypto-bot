import asyncio
import time

import telebot
from crypto_price_viewer import CryptoPriceViewer, get_crypto_price
import tkinter as tk
from telebot import types

bot = telebot.TeleBot('6602251345:AAG9YfiUOZ_xgLpwthcZcc8PNFU1vkFLwiY')

root = tk.Tk()
crypto_viewer = CryptoPriceViewer(root)


def get_text_messages(message):
    if message.text == "/help" or message.text == "/start":
        buttons = set_welcome_buttons()
        bot.send_message(message.from_user.id, "Welcome to the Secret Society!", reply_markup=buttons)


def set_welcome_buttons():
    markup = types.InlineKeyboardMarkup()
    buttons_line1 = [
        types.InlineKeyboardButton(text="💸Price", callback_data="price"),
        types.InlineKeyboardButton(text="...", callback_data="cart"),
        types.InlineKeyboardButton(text="...", callback_data="delivery"),
        types.InlineKeyboardButton(text="...", callback_data="history"),
    ]
    buttons_line2 = [
        types.InlineKeyboardButton(text="...", callback_data="about"),
        types.InlineKeyboardButton(text="...", callback_data="support"),
    ]

    for button in buttons_line1:
        markup.add(button)

    markup.add(*buttons_line2)
    return markup


def set_crypto_pairs_buttons():
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("💲BTC/USDT", callback_data='pair_BTC/USDT')
    button2 = types.InlineKeyboardButton("💲ETH/USDT", callback_data='pair_ETH/USDT')
    button3 = types.InlineKeyboardButton("💲SOL/USDT", callback_data='pair_SOL/USDT')
    button4 = types.InlineKeyboardButton("💲ATOM/USDT", callback_data='pair_ATOM/USDT')

    markup.add(button1, button2, button3, button4)

    return markup


@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    get_text_messages(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "price":
            buttons = set_crypto_pairs_buttons()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🚀Top pairs:",
                                  reply_markup=buttons)
        elif call.data.startswith("pair_"):
            asyncio.run(refresh_price(call))
        elif call.data == "/help" or call.data == "/start":
            buttons = set_welcome_buttons()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Welcome to the Secret Society!", reply_markup=buttons)


async def refresh_price(call):
    crypto_pair = call.data[5:]
    price = await get_crypto_price(crypto_pair)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"Current price of {crypto_pair}: {price}")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Exception: {e}")
        time.sleep(15)
