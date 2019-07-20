import sys
import os
from flask import Flask, request
import telepot
from telepot.loop import OrderedWebhook
import result_drawer
import joydrawer
import sberdrawer
import random
from io import BytesIO
from PIL import Image
from telepot.namedtuple import ReplyKeyboardMarkup, InlineKeyboardMarkup

"""
$ python2.7 flask_skeleton.py <token> <listening_port> <webhook_url>
Webhook path is '/webhook', therefore:
<webhook_url>: https://<base>/webhook
"""
query = {}
WATERMARK_MODE = True
PASSWORD = 'артем крутой'
ADMINS = [474504117, 551475668]

def adminka(chat_id):
    query[chat_id] = ['logged']
    bot.sendMessage(chat_id, 'Чего хочешь господин)💻', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [dict(text='Результаты Айсены😍', callback_data='result.generate')],
        [dict(text='Сбербанк💳', callback_data='sberbank.generate')],
        [dict(text='JOYCASINO Баланс🤑', callback_data='joycasino.generate')]]))

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_id not in query:
        query[chat_id] = []
    if content_type == 'text':
        if msg['text'] == '/start':
            if 'logged' not in query[chat_id]:
                if chat_id in ADMINS:
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

    if content_type == 'photo':
        if 'result' in query[chat_id]:
            try:
                char = msg['caption'].split('.')
                file = BytesIO()
                bot.download_file(msg['photo'][-1]['file_id'], file)
                file.seek(0)
                face = Image.open(file)
                result = result_drawer.draw(face, char[0], char[1], char[2], char[3])
                bot.sendPhoto(chat_id, result)
            except KeyError:
                bot.sendMessage(chat_id, "🚫Ты не добавил описания (т.е. подписи к фото)\n**Пример подписи:**\nНиколай Николаев.18.750.26590\n**То есть:**\nИмя.Возраст.Старт.Прибыль\n\n**Все через точку**", parse_mode='Markdown')
            except IndexError:
                bot.sendMessage(chat_id, "🚫Неправильное описание (т.е. подпись к фото)\n**Пример подписи:**\nНиколай Николаев.18.750.26590\n**То есть:**\nИмя.Возраст.Старт.Прибыль\n\n**Все через точку**", parse_mode='Markdown')


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
    data = data.split('.')
    if from_id not in query:
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
                bot.sendPhoto(from_id, 'AgADAgAD1qoxG8zHoUhT7UKEyRdyKoOBCA4ABKbxp6mlejJiP7gBAAEC')

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

@app.route('/conversion', methods=['GET'])
def conversion():
	print(request.args)
	ip = request.args.get('ip')
	offer = request.args.get('offer')
	geo = request.args.get('geo')
	city = request.args.get('city')
	summa = request.args.get('sum')
	operationsystem = request.args.get('os')
	for admin in ADMINS:
		bot.sendMessage(admin, '''✅КОНВЕРСИЯ!✅\n
								  — — — — — — — —\n
							      📡IP:{0}\n
								  🧩Оффер:{1}\n
								  🗾ГЕО:{2}\n
								  🏢Город:{3}\n
								  💵Сумма:{4}\n
								  💽ОС:{5}\n
								  — — — — — — — —'''.format(ip, offer, geo, city, summa, operationsystem))
	return 'OK'


if __name__ == '__main__':
    try:
        bot.setWebhook(URL)
    # Sometimes it would raise this error, but webhook still set successfully.
    except telepot.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)