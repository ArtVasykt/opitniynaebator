from PIL import Image
from sms_drawer import draw as smsdraw
from lightstatusbariosdrawer import draw as stdraw
from io import BytesIO

def draw(smslist, debug=False):
	sms = smsdraw(smslist, debug='Module')
	statusbar = stdraw(debug='Module')
	img = Image.new('RGBA', (750, sms.height + statusbar.height))
	img.paste(sms, box=(0, 40))
	img.paste(statusbar, box=(0, 0))

	if not debug:
		output = BytesIO()
		img.save(output, format='PNG')
		output.seek(0)
		return ('temp.PNG', output) # For Telepot (TELEGRAM BOT)
	elif debug == 'Module':
		return img
	else:
		img.save('output.png', format='PNG')
		return True

if __name__ == "__main__":
	draw(['VISA4734 10:55 Покупка 200000р. MERCEDES-BENZ LLC. Баланс: 156787009р.',
	 'ДД#0#267', 'с#VISA4734 Списание Facebook APL 6500р. Баланс: 15678765р.' ,
	  'б#VISA4734 23:56 Выдача 1678000р. ATM Сбербанк Халтурина Баланс: 156787987р.', 'ДД#1#643'], debug=True)