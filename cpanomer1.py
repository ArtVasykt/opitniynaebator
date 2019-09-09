import requests
from datetime import datetime
from pytz import timezone
from bs4 import BeautifulSoup

url = 'http://my.cpanomer1.ru/'
login = 'amgeow@gmail.com'
password = 'amantemidze2211'

def connect():
	s = requests.Session()
	# AUTH
	print('Устанавливаем соединение с cpanomer1...')
	auth_page = s.get(url + 'signin')
	soup = BeautifulSoup(auth_page.text, features='html.parser')
	print('Берем CSRF-токен...')
	csrftoken = soup.find('input', id='SignUp__token').get('value')
	print('Токен: {0}'.format(csrftoken))
	s.post(url + 'signin', {
		'SignUp[_token]': csrftoken,
		'SignUp[email]': login,
		'SignUp[password]': password,
		'SignUp[remember]': 1
		})
	return s

def get_balance():
	s = connect()
	r = s.get(url + 'dashboard')
	soup = BeautifulSoup(r.text, features='html.parser')

	moscow = timezone('Europe/Moscow')
	now = moscow.localize(datetime.now()).strftime('%d-%m-%Y')
	today_revenue = s.get(url + 'stats/ajax_get_data?params[mode]=daily&params[date_from]={0}&params[date_to]={1}&params[currency]=RUB&params[timezone]=Europe/Moscow'.format(now, now))
	# EUR 0 0 0 RUB 0 0 0 USD 0 0 0
	balance = [x.text.replace('\xa0', ' ') for x in soup.find_all('table')[1].find_all('td')]
	balance = {
		'Холд': {
			'RUB': balance[6],
			'USD': balance[10],
		},
		'Баланс': {
			'RUB': balance[5],
			'USD': balance[9]
		},
		'За сегодня': {
			'Заработано': today_revenue.json()['total']['actions']['total']['revenue'],
			'Депов': today_revenue.json()['total']['actions']['pending']['count']
		}
	}
	return balance

if __name__ == "__main__":
	print(get_balance())