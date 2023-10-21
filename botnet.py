import telebot
import requests
import json
import os


class CurrencyBot:
    API_URL = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR'

    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def run(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def start(message):
            instructions = '''
            Привет! Я бот, который может вернуть цену на определенное количество валюты.
            Чтобы узнать цену, отправьте мне сообщение в формате:
            <имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>
            Например: USD RUB 10
            '''
            self.bot.reply_to(message, instructions)

        @self.bot.message_handler(commands=['values'])
        def values(message):
            response = requests.get(self.API_URL)
            data = json.loads(response.text)
            rates = data['rates']
            currencies = '\n'.join([currency for currency in rates.keys()])
            self.bot.reply_to(message, currencies)

        @self.bot.message_handler(func=lambda message: True)
        def get_price(message):
            try:
                base_currency, quote_currency, amount = message.text.split()
                price = self._get_currency_price(base_currency.upper(), quote_currency.upper(), float(amount))
                self.bot.reply_to(message, f'{amount} {base_currency} = {price} {quote_currency}')
            except Exception as e:
                self.bot.reply_to(message, str(e))

        self.bot.polling()

    @staticmethod
    def _get_currency_price(base, quote, amount):
        response = requests.get(f'{CurrencyBot.API_URL}?base={base}&symbols={quote}')
        data = json.loads(response.text)
        if 'error' in data:
            raise Exception(data['error'])
        rate = data['rates'][quote]
        return rate * amount


print("kiber_bot - telegram")
bot = CurrencyBot('5434270396:AAF6sEenUDcjc8Nf9mMRGUBzwI58bMth9Is')
bot.run()
