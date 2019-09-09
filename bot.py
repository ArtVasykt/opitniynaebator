import sys
import os
from flask import Flask, request
import telepot
from telepot.loop import OrderedWebhook
import joydrawer
import sberdrawer
import random
import requests
from io import BytesIO
from PIL import Image
from telepot.namedtuple import ReplyKeyboardMarkup, InlineKeyboardMarkup

"""
$ python2.7 flask_skeleton.py <token> <listening_port> <webhook_url>
Webhook path is '/webhook', therefore:
<webhook_url>: https://<base>/webhook
"""
amounts = {}
query = {}
ADMINS = [474504117, 551475668, 680497281, 671781357, 660163008, 866346596, 400885030, 804792225, 408801179]

def adminka(chat_id):
    bot.sendMessage(chat_id, 'Если есть какая-нибудь идея *обязательно* напиши @ghjkluiopp (серьезно) 💻',
    	parse_mode='Markdown',
    	reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [dict(text='Сбербанк💳', callback_data='sberbank.generate')],
        [dict(text='JOYCASINO Баланс🤑', callback_data='joycasino.generate')]]))

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_id not in query:
        query[chat_id] = []

    if content_type == 'text':
        if msg['text'] == '/start':
            if chat_id in ADMINS:
                adminka(chat_id)
            else:
                bot.sendMessage(chat_id, '*Вам нужно получить доступ от разработчика бота, напиши @ghjkluiopp*🔐',
                parse_mode='Markdown')
        elif msg['text'] == '1111':
        	adminka(chat_id)
        else:
            try:
                if 'sberbank' in query[chat_id]:
                    numbers = msg['text'].split('.')
                    bot.sendPhoto(chat_id, sberdrawer.draw(numbers[0], numbers[1]))
                    adminka(chat_id)
                elif 'joycasino_amount' in query[chat_id]:
                    amounts[chat_id] = msg['text']
                    bot.sendMessage(chat_id, 'Напиши мейл📩 (без @gmail.com)')
                    query[chat_id].remove('joycasino_amount')
                    query[chat_id].append('joycasino_mail')
                elif 'joycasino_mail' in query[chat_id]:
                    bot.sendPhoto(chat_id, joydrawer.draw(msg['text'], amounts[chat_id]))
                    adminka(chat_id)

            except Exception as e:
                bot.sendMessage(chat_id, '🚫🚫🚫\nОшибка: ' + str(e))

def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
    data = data.split('.')

    if from_id not in query:
        query[from_id] = []

    if data[0] == 'sberbank':
        if data[1] == 'generate':
            bot.answerCallbackQuery(query_id, 'OK')
            query[from_id].append('sberbank')
            bot.sendMessage(from_id, '''Кароч напиши *сколько* ты ему "перевел"💵\n\n
            И его(её) *карту* (16 цифр)💳\n\n*ЧЕРЕЗ ТОЧКУ*.\n\nПример: 10000.4276656589765432''', parse_mode='Markdown')
        
    elif data[0] == 'joycasino':
        if data[1] == 'generate':
            bot.answerCallbackQuery(query_id, 'OK')
            bot.sendMessage(from_id, 'Напиши сумму🤑')
            query[from_id].append('joycasino_amount')


TOKEN = '860594921:AAG1GHkdaJU0JFlExy-6CNJUSeeIYcyTo4c'
URL = 'https://opitniynaebator.herokuapp.com/'

app = Flask(__name__)
bot = telepot.Bot(TOKEN)
webhook = OrderedWebhook(bot, {'chat': on_chat_message,
                               'callback_query': on_callback_query})

@app.route('/', methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'

@app.route('/message', methods=['GET'])
def pass_message():
	for admin in ADMINS:
		bot.sendMessage(admin, request.args.get('message'))
	return 'OK'

#@app.route('/conversion', methods=['GET'])
#def conversion():
#	print(request.args)
#	ip = request.args.get('ip')
#	offer = request.args.get('offer')
#	geo = request.args.get('geo')
#	city = request.args.get('city')
#	summa = request.args.get('sum')
#	operationsystem = request.args.get('os')
#	if summa != '0':
#		for admin in ADMINS:
#			bot.sendMessage(admin, "✅*ДЕП!*✅", parse_mode="Markdown")
#	return 'OK'


if __name__ == '__main__':
    try:
        bot.setWebhook(URL)
    # Sometimes it would raise this error, but webhook still set successfully.
    except telepot.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)