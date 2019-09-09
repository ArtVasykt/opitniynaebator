import sys
import os
from flask import Flask, request
import telepot
from telepot.loop import OrderedWebhook
import result_drawer
import joydrawer
import sberdrawer
import random
import cpanomer1 as cpa
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
WATERMARK_MODE = True
PASSWORD = 'артем крутой'
ADMINS = [474504117, 551475668, 660163008, 866346596, 400885030, 804792225, 408801179]
CPA = [680497281, 671781357]

def adminka(chat_id):
    query[chat_id] = ['logged']
    if chat_id in ADMINS:
    	bot.sendMessage(chat_id, 'Чего хочешь господин)💻', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        	[dict(text='Сбербанк💳', callback_data='sberbank.generate')],
        	[dict(text='JOYCASINO Баланс🤑', callback_data='joycasino.generate')]]))
    elif chat_id in CPA:
    	bot.sendMessage(chat_id, 'Привет CPA#1💻', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        	[dict(text='Сбербанк💳', callback_data='sberbank.generate')],
        	[dict(text='JOYCASINO Баланс🤑', callback_data='joycasino.generate')]]))

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_id not in query:
        query[chat_id] = []
    if content_type == 'text':
        if msg['text'] == '/start':
            if 'logged' not in query[chat_id]:
                if chat_id in ADMINS or chat_id in CPA:
                    adminka(chat_id)
                else:
                    bot.sendMessage(chat_id, '**Пожалуйста введите пароль**🔐', parse_mode='Markdown')
                    query[chat_id].append('logging')
            else:
                adminka(chat_id)

        elif 'logging' in query[chat_id]:
            if msg['text'].lower() == PASSWORD:
                query[chat_id].append('logged')
                bot.sendMessage(chat_id, '**Вход выполнен успешно, брат**🖤', parse_mode='Markdown')
                adminka(chat_id)
            else:
                bot.sendMessage(chat_id, '🚫Неверный пароль сука!')

        elif 'logged' in query[chat_id]:
            try:
                if msg['text'] == '/backnahoi':
                    adminka(chat_id)
                elif 'sberbank' in query[chat_id]:
                    numbers = msg['text'].split('.')
                    bot.sendPhoto(chat_id, sberdrawer.draw(numbers[0], numbers[1]))
                    adminka(chat_id)
                elif 'joycasino_amount' in query[chat_id]:
                    amounts[chat_id] = msg['text']
                    bot.sendMessage(chat_id, 'Напиши мейл📩 (без @gmail.com)')
                    query[chat_id].remove('joycasino_amount')
                    query[chat_id].append('joycasino_mail')
                elif 'joycasino_mail' in query[chat_id]:
                    bot.sendPhoto(chat_id, joydrawer.draw(msg['text'], amounts[chat_id]), caption='На здоровье сука')
                    adminka(chat_id)

            except Exception as e:
                bot.sendMessage(chat_id, '🚫🚫🚫\nОшибка: ' + str(e))

def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
    data = data.split('.')

    if data[0] == 'rosigrishbot':
        print('Участвует {0}'.format(msg['from'].get('first_name')))
        newdata = {'chat_id': from_id,
                'first_name': msg['from'].get('first_name', ''),
                'username': msg['from'].get('username', ''),
                'last_name': msg['from'].get('last_name', ''),
                'giveaway_id': data[1]}
        print(data)
        bot.answerCallbackQuery(query_id, 'Вы учавствуете в розыгрыше!')
        r = requests.post('http://194.67.86.228/api/giveawaypart/', data=newdata)
    elif from_id not in query:
        if from_id in ADMINS:
            query[from_id].append('logged')
        else:
            bot.sendMessage(from_id, '**Пожалуйста введите пароль**🔐', parse_mode='Markdown')
            query[from_id].append('logging')
    elif 'logged' in query[from_id]:
        if data[0] == 'result':
            if data[1] == 'generate':
                bot.answerCallbackQuery(query_id, 'Отправь фото с описанием.📷')
                query[from_id].append('result')
                bot.sendMessage(from_id, 'Отправь фото с описанием.📷', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [dict(text='🤷‍♂️Как?', callback_data='result.tutor')]]))
            elif data[1] == 'tutor':
                bot.answerCallbackQuery(query_id, 'Ща все покажу расскажу')
                bot.sendMessage(from_id, 'Ты должен мне прислать примерно вот такое изображение с подписью!')
                bot.sendPhoto(from_id, 'https://i1.sndcdn.com/avatars-000338809424-572092-t500x500.jpg', caption='Сикснайн.69.1000.100000')
                bot.sendMessage(from_id, 'Тогда ты получишь такую штуку👇')
                bot.sendPhoto(from_id, 'AgADAgADJ60xG2I9AUqlBga1wIXb8EY7hA8ABAEAAwIAA3kAA9_AAwABFgQ')

        elif data[0] == 'sberbank':
            if data[1] == 'generate':
                bot.answerCallbackQuery(query_id, 'OK')
                query[from_id].append('sberbank')
                bot.sendMessage(from_id, 'Кароч напиши сколько ты ему "перевел"💵\n\nP.S. Можно использовать знаки только 1-5 и 0\n\n И его карту (16 цифр)💳\n\nЧЕРЕЗ ТОЧКУ.\n\nПример: 10000.4276656589765432')
        
        elif data[0] == 'joycasino':
            if data[1] == 'generate':
                bot.answerCallbackQuery(query_id, 'OK')
                bot.sendMessage(from_id, 'Напиши сумму🤑')
                query[from_id].append('joycasino_amount')

        elif data[0] == 'cpanomer1':
        	if data[1] == 'balance':
        		balance = cpa.get_balance()
        		bot.answerCallbackQuery(query_id, 'OK')
        		bot.sendMessage(from_id, '*Холд:*\nRUB {0}р.\nUSD {1}$\n*Баланс:*\nRUB {2}р.\nUSD {3}$\n\n_В общем за сегодня депов_ *{4}* _заработано_ *{5} р.*'.format(
        		balance['Холд']['RUB'], balance['Холд']['USD'], balance['Баланс']['RUB'], balance['Баланс']['USD'], balance['За сегодня']['Депов'], balance['За сегодня']['Заработано']), parse_mode='Markdown')
        		adminka(from_id)

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

@app.route('/conversion', methods=['GET'])
def conversion():
	print(request.args)
	ip = request.args.get('ip')
	offer = request.args.get('offer')
	geo = request.args.get('geo')
	city = request.args.get('city')
	summa = request.args.get('sum')
	operationsystem = request.args.get('os')
	if summa != '0':
		for admin in ADMINS:
			bot.sendMessage(admin, "✅*ДЕП!*✅", parse_mode="Markdown")
	return 'OK'


if __name__ == '__main__':
    try:
        bot.setWebhook(URL)
    # Sometimes it would raise this error, but webhook still set successfully.
    except telepot.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)