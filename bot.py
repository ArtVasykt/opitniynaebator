import sys
import os
from flask import Flask, request
import telepot
from telepot.loop import OrderedWebhook
from result_drawer import draw
import joydrawer
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
PASSWORD = 'pasha_lox'

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        if msg['text'] == '/start':
            if chat_id not in logged_users:
                bot.sendMessage(chat_id, '**Пожалуйста введите пароль**🔐', parse_mode='Markdown')
                logging_in.append(chat_id)
        elif chat_id in logging_in:
            if msg['text'].lower() == PASSWORD:
                logged_users.append(chat_id)
                logging_in.remove(chat_id)
                bot.sendMessage(chat_id, '**Вход выполнен успешно, брат**🖤', parse_mode='Markdown')

    if content_type == 'photo' and chat_id in logged_users:
        try:
            char = msg['caption'].split('.')
            file = BytesIO()
            bot.download_file(msg['photo'][-1]['file_id'], file)
            file.seek(0)
            face = Image.open(file)
            result = draw(face, char[0], char[1], char[2], char[3])
            bot.sendPhoto(chat_id, result, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [dict(text='Сгенерировать баланс 🎻', callback_data='generate_balance.{0}'.format(char[3]))]]))
        except KeyError:
            bot.sendMessage(chat_id, "🚫Ты не добавил описания (т.е. подписи к фото)\n**Пример подписи:**\nНиколай Николаев.18.750.26590\n**То есть:**\nИмя.Возраст.Старт.Прибыль\n\n**Все через точку**", parse_mode='Markdown')
        except IndexError:
            bot.sendMessage(chat_id, "🚫Неправильное описание (т.е. подпись к фото)\n**Пример подписи:**\nНиколай Николаев.18.750.26590\n**То есть:**\nИмя.Возраст.Старт.Прибыль\n\n**Все через точку**", parse_mode='Markdown')
        
    print('Chat Message:', content_type, chat_type, chat_id)


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
    data = data.split('.')
    if data[0] == 'generate_balance':
        balance = joydrawer.draw(int(data[1])- 100, int(data[1]))
        bot.sendPhoto(from_id, balance)
        bot.answerCallbackQuery(query_id, 'Ща все будет')


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