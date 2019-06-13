import sys
import os
from flask import Flask, request
import telepot
from telepot.loop import OrderedWebhook
from result_drawer import draw
from io import BytesIO
from PIL import Image

"""
$ python2.7 flask_skeleton.py <token> <listening_port> <webhook_url>
Webhook path is '/webhook', therefore:
<webhook_url>: https://<base>/webhook
"""

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'photo':
        try:
            char = msg['caption'].split('.')
            file = BytesIO()
            bot.download_file(msg['photo'][-1]['file_id'], file)
            file.seek(0)
            face = Image.open(file)
            result = draw(face, char[0], char[1], char[2], char[3])
            bot.sendPhoto(chat_id, result)
        except KeyError:
            bot.sendMessage(chat_id, "🚫Ты не добавил описания (т.е. подписи к фото)\n**Пример подписи:**\nНиколай Николаев.18.750.26590\n**То есть:**\nИмя.Возраст.Старт.Прибыль\n\n**Все через точку**", parse_mode='Markdown')
        except IndexError:
            bot.sendMessage(chat_id, "🚫Неправильное описание (т.е. подпись к фото)\n**Пример подписи:**\nНиколай Николаев.18.750.26590\n**То есть:**\nИмя.Возраст.Старт.Прибыль\n\n**Все через точку**", parse_mode='Markdown')
        
    print('Chat Message:', content_type, chat_type, chat_id)


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)


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