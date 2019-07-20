import sys
import os
from flask import Flask, request
import telepot
from telepot.loop import OrderedWebhook
import smswithstatusbar as smsdrawer
from telegram_drawer import chat as chatdraw
import watermarker as wm
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
sms_query = {}
tq = {} # Telegram query
img_query = {}
amounts = {}
WATERMARK_MODE = True
PASSWORD = 'артем крутой'
ADMINS = ['474504117', '551475668']

TELEGRAM_CONTROL = [
    [dict(text='Свап💬', callback_data='telegram.swap')],
    [dict(text='Отменить последнее🔙', callback_data='telegram.undo')],
    [dict(text='Время сообщения🕐', callback_data='telegram.time')]
    ]

def adminka(chat_id):
    query[chat_id] = ['logged']
    bot.sendMessage(chat_id, 'Чего хочешь господин)💻', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [dict(text='Результаты Айсены😍', callback_data='result.generate')],
        [dict(text='Сбербанк💳', callback_data='sberbank.generate')],
        [dict(text='JOYCASINO Баланс🤑', callback_data='joycasino.generate')],
        [dict(text='SMS✉️', callback_data='sms.generate')],
        [dict(text='Telegram[Beta]💠', callback_data='telegram.generate')],
        [dict(text='Watermark✏️', callback_data='watermark.generate')]]))

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
                elif 'sms' in query[chat_id]:
                    print(sms_query)
                    sms_query[chat_id].insert(0, msg['text'])
                    sms = smsdrawer.draw(sms_query[chat_id])
                    bot.sendPhoto(chat_id, sms, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [dict(text="Отменить последнее🔙", callback_data="sms.delete")]]))
                elif 'telegram_name' in query[chat_id]:
                    tg = tq[chat_id]
                    tg['name'] = msg['text']
                    result = chatdraw(tg['textlist'],tg['name'],tg['avatar'],tg['online'])
                    bot.sendPhoto(chat_id, result, caption='✅Отличное имя! Начинайте писать!')
                    query[chat_id].remove('telegram_name')
                    query[chat_id].append('telegram_gen')
                elif 'telegram_time' in query[chat_id]:
                    tg = tq[chat_id]
                    tg['textlist'][tg['count']]['time'] = msg['text']
                    result = chatdraw(tg['textlist'],tg['name'],
                        tg['avatar'],tg['online'])
                    bot.sendPhoto(chat_id, result, reply_markup=InlineKeyboardMarkup(inline_keyboard=TELEGRAM_CONTROL))
                    query[chat_id].remove('telegram_time')
                    query[chat_id].append('telegram_gen')


            except Exception as e:
                bot.sendMessage(chat_id, '🚫🚫🚫\nОшибка: ' + str(e))

            if 'telegram_gen' in query[chat_id]:
                tg = tq[chat_id]
                tg['textlist'][tg['count']].append(msg['text'])
                result = chatdraw(tg['textlist'],tg['name'], tg['avatar'],tg['online'])
                bot.sendPhoto(chat_id, result, reply_markup=InlineKeyboardMarkup(inline_keyboard=TELEGRAM_CONTROL))

            

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
        elif 'telegram_photo' in query[chat_id]:
            tg = tq[chat_id]
            file = BytesIO()
            bot.download_file(msg['photo'][-1]['file_id'], file)
            file.seek(0)
            avatar = Image.open(file)
            tg['avatar'] = avatar
            bot.sendMessage(chat_id, '✅Хорошо, аватар загружен. Теперь введите имя.')
            query[chat_id].remove('telegram_photo')
            query[chat_id].append('telegram_name')
        elif 'telegram_gen' in query[chat_id]:
            tg = tq[chat_id]
            file = BytesIO()
            bot.download_file(msg['photo'][-1]['file_id'], file)
            file.seek(0)
            img = Image.open(file)
            tg['textlist'][tg['count']].append(img)
            result = chatdraw(tg['textlist'], tg['name'], tg['avatar'],tg['online'])
            bot.sendPhoto(chat_id, result, reply_markup=InlineKeyboardMarkup(inline_keyboard=TELEGRAM_CONTROL))
        elif 'watermark_target' in query[chat_id]:
            query[chat_id].remove('watermark_target')
            query[chat_id].append('watermark_mark')
            file = BytesIO()
            bot.download_file(msg['photo'][-1]['file_id'], file)
            file.seek(0)
            img_query.update({chat_id: Image.open(file)})
            bot.sendMessage(chat_id, 'Отправьте собственную вотермарку или выберите нужный.🖌', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [dict(text='Баина Щедрая💘', callback_data='watermark.baina')],
                [dict(text='Albinos Money Team💵', callback_data='watermark.albinos')]]))
        elif 'watermark_mark' in query[chat_id]:
            query[chat_id].remove('watermark_mark')
            file = BytesIO()
            bot.download_file(msg['photo'][-1]['file_id'], file)
            file.seek(0)
            bot.sendPhoto(chat_id, wm.mark(img_query[chat_id], Image.open(file)))


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


        elif data[0] == 'sms':
            if data[1] == 'generate':
                bot.answerCallbackQuery(query_id, 'OK')
                bot.sendMessage(from_id, 'Если впервые ознакомься👇👇', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [dict(text="Туториал✅", callback_data='sms.tutorial')],
                    [dict(text="Начать💻", callback_data="sms.start")]]))
            elif data[1] == 'tutorial':
                bot.answerCallbackQuery(query_id, 'Прочитай внимательно!')
                bot.sendMessage(from_id, '✅Сообщения будут выводится снизу вверх\n✅Ты должен выбрать какие показать с хвостом какие нет')
                bot.sendMessage(from_id, 'Формат сообщений таков (Разделяется через теги):\n✅"с#VISA4734" - с хвостом\n✅"б#VISA4734" - без хвоста\n✅"ДД#01#1230"')
                bot.sendPhoto(from_id, "AgADAgADx6sxG8DQ0UiujtIrhlPFa65IUw8ABIAGKRCbL7ybVCAFAAEC", caption="Наглядно📷", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [dict(text="Начать💻", callback_data="sms.start")]]))
            elif data[1] == 'start':
                query[from_id].append('sms')
                sms_query[from_id] = []
                bot.answerCallbackQuery(query_id, 'OK')
                bot.sendMessage(from_id, '📲Начинай писать:\nСколько написано: {0}🥇'.format(len(sms_query[from_id])))
            elif data[1] == 'delete':
                bot.answerCallbackQuery(query_id, 'OK')
                if len(sms_query[from_id]) != 0:
                    sms_query[from_id].pop()
                    sms = smsdrawer.draw(sms_query[from_id])
                    bot.sendPhoto(from_id, sms, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [dict(text="Отменить последнее🔙", callback_data="sms.delete")]]))
                else:
                    adminka(from_id)


        elif data[0] == 'telegram':
            if data[1] == 'generate':
                bot.answerCallbackQuery(query_id, 'OK')
                bot.sendMessage(from_id, '📲Отправь фото аватарки')
                tq.update({from_id: {'textlist':[], 'online': 0, 'time': '12:00', 'count':0}})
                query[from_id].append('telegram_photo')
            elif data[1] == 'swap':
                tg = tq[chat_id]
                bot.answerCallbackQuery(query_id, 'OK')
                tg['count'] += 1
                tg['textlist'].append({'sender': tg['count'] % 2,'textlist':[], 'time': tg['textlist'][tg['count'] - 1]['time']})
            elif data[1] == 'undo':
                tg = tq[chat_id]
                bot.answerCallbackQuery(query_id, 'OK')
                tg['textlist'][tg['count']].pop()
                result = chatdraw(tg['textlist'],tg['name'],tg['avatar'],tg['online'])
                bot.sendPhoto(from_id, result, reply_markup=InlineKeyboardMarkup(inline_keyboard=TELEGRAM_CONTROL))
            elif data[1] == 'time':
                bot.answerCallbackQuery(query_id, 'OK')
                query[from_id].remove('telegram_gen')
                query[from_id].append('telegram_time')
                bot.sendMessage(from_id, 'Напишите время⏰')


        elif data[0] == 'watermark':
            if data[1] == 'generate':
                bot.answerCallbackQuery(query_id, 'OK')
                query[from_id].append('watermark_target')
                bot.sendMessage(from_id, '📲Отправь сюда фото, которое хочешь завотермарить.✏️')
            elif data[1] == 'baina':
                bot.answerCallbackQuery(query_id, 'OK')
                query[from_id].remove('watermark_mark')
                img = Image.open('source/baina.png')
                bot.sendPhoto(from_id, wm.mark(img_query[from_id], img))
                adminka(from_id)
            elif data[1] == 'albinos':
                bot.answerCallbackQuery(query_id, 'OK')
                query[from_id].remove('watermark_mark')
                img = Image.open('source/albinos.png')
                bot.sendPhoto(from_id, wm.mark(img_query[from_id], img))
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

@app.route('/conversion', methods=['GET'])
def conversion():
	webhook.feed(request.data)
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