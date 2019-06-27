import sys
import os
from flask import Flask, request
import telepot
from telepot.loop import OrderedWebhook
from result_drawer import draw
import joydrawer
import sberdrawer
from io import BytesIO
from PIL import Image
from telepot.namedtuple import ReplyKeyboardMarkup, InlineKeyboardMarkup

"""
$ python2.7 flask_skeleton.py <token> <listening_port> <webhook_url>
Webhook path is '/webhook', therefore:
<webhook_url>: https://<base>/webhook
"""
logged_users = []
logging_in = []
result_query = []
sberbank_query = []
joycasino_query = []
PASSWORD = 'артем крутой'
admins = ['474504117', 474504117]

def adminka(chat_id):
    if chat_id in result_query:
        result_query.remove(chat_id)
    if chat_id in sberbank_query:
        sberbank_query.remove(chat_id)
    if chat_id in joycasino_query:
        joycasino_query.remove(chat_id)
    bot.sendMessage(chat_id, 'Чего хочешь господин)💻', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [dict(text='Результаты Айсены😍', callback_data='result.generate')],
        [dict(text='Сбербанк💳', callback_data='sberbank.generate')],
        [dict(text='JOYCASINO Баланс🤑', callback_data='joycasino.generate_prepare')]]))

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        if msg['text'] == '/start':
            if chat_id not in logged_users:
                if chat_id in admins:
                    logged_users.append(chat_id)
                    adminka(chat_id)
                else:
                    bot.sendMessage(chat_id, '**Пожалуйста введите пароль**🔐', parse_mode='Markdown')
                    logging_in.append(chat_id)
        elif chat_id in logging_in:
            if msg['text'].lower() == PASSWORD:
                logged_users.append(chat_id)
                logging_in.remove(chat_id)
                bot.sendMessage(chat_id, '**Вход выполнен успешно, брат**🖤', parse_mode='Markdown')
        elif chat_id in logged_users:
            if msg['text'] == '/backnahoi':
                adminka(chat_id)
            elif chat_id in sberbank_query:
                try:
                    numbers = msg['text'].split('.')
                    bot.sendPhoto(chat_id, sberdrawer.draw(numbers[0], numbers[1]))
                except Exception as e:
                    bot.sendMessage(chat_id, '🚫🚫🚫\nОшибка: ' + str(e))
                adminka(chat_id)
            elif chat_id in joycasino_query:
                try:
                    amount = int(msg['text'])
                    bot.sendPhoto(joydrawer.draw(amount, amount))
                except Exception as e:
                    bot.sendMessage(chat_id, '🚫🚫🚫\nОшибка: ' + str(e))
                adminka(chat_id)
            

    if content_type == 'photo' and chat_id in logged_users and chat_id in result_query:
        try:
            char = msg['caption'].split('.')
            file = BytesIO()
            bot.download_file(msg['photo'][-1]['file_id'], file)
            file.seek(0)
            face = Image.open(file)
            result = draw(face, char[0], char[1], char[2], char[3])
            bot.sendPhoto(chat_id, result, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [dict(text='Сгенерировать баланс 🎻', callback_data='result.generate_balance.{0}'.format(char[3]))],
                [dict(text='Назад🔙', callback_data='result.back')]]))
        except KeyError:
            bot.sendMessage(chat_id, "🚫Ты не добавил описания (т.е. подписи к фото)\n**Пример подписи:**\nНиколай Николаев.18.750.26590\n**То есть:**\nИмя.Возраст.Старт.Прибыль\n\n**Все через точку**", parse_mode='Markdown')
        except IndexError:
            bot.sendMessage(chat_id, "🚫Неправильное описание (т.е. подпись к фото)\n**Пример подписи:**\nНиколай Николаев.18.750.26590\n**То есть:**\nИмя.Возраст.Старт.Прибыль\n\n**Все через точку**", parse_mode='Markdown')
        
    print('Chat Message:', content_type, chat_type, chat_id)


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
    data = data.split('.')
    if data[0] == 'result':
        if data[1] == 'generate_balance':
            bot.answerCallbackQuery(query_id, 'Ща все будет')
            balance = joydrawer.draw(int(data[2])- 100, int(data[2]))
            bot.sendPhoto(from_id, balance)
        elif data[1] == 'generate':
            bot.answerCallbackQuery(query_id, 'Отправь фото с описанием.📷')
            result_query.append(from_id)
            bot.sendMessage(from_id, 'Отправь фото с описанием.📷')
        elif data[1] == 'back':
            bot.answerCallbackQuery(query_id, 'OK')
            result_query.remove(from_id)
            adminka(from_id)
    elif data[0] == 'sberbank':
        if data[1] == 'generate':
            bot.answerCallbackQuery(query_id, 'OK')
            sberbank_query.append(from_id)
            bot.sendMessage(from_id, 'Кароч напиши сколько ты ему "перевел"💵\n\nP.S. Можно использовать знаки только 1-5 и 0\n\n И его карту (16 цифр)💳\n\nЧЕРЕЗ ТОЧКУ.\n\nПример: 10000.4276656589765432')
    elif data[0] == 'joycasino':
        if data[1] == 'generate_prepare':
            bot.answerCallbackQuery(query_id, 'OK')
            bot.sendMessage(from_id, 'Напиши сумму🤑')
            joycasino_query.append(from_id)

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

if __name__ == '__main__':
    try:
        bot.setWebhook(URL)
    # Sometimes it would raise this error, but webhook still set successfully.
    except telepot.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)