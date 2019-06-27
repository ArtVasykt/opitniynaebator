from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
import sys

BIG_CORNER = 400
BIG_VERT = 235
SMALL_CORNER = 397
SMALL_VERT = 274
EMAIL_CORNER = 102
EMAIL_VERT = 109

BIGDIGITS = {}
SMALLDIGITS = {}

MAILS = ['@mail.ru', '@gmail.com', '@yandex.ru']

for i in range(0, 10):
	bigimg = Image.open('fonts/joycasino/joybig/' + str(i) + '.png')
	BIGDIGITS.update({str(i):bigimg})
	smallimg = Image.open('fonts/joycasino/joysmall/' + str(i) + '.png')
	SMALLDIGITS.update({str(i):smallimg})

BIGDIGITS.update({',': Image.open('fonts/joycasino/joybig/,.png')})
SMALLDIGITS.update({',': Image.open('fonts/joycasino/joysmall/,.png')})

def big(amount):
	imgwidth = 0
	imgheight = 21
	spacing = 1
	x = 0
	# Calculate width of image
	for number in amount:
		imgwidth += BIGDIGITS[number].width + spacing
	canvas = Image.new('RGBA', (imgwidth, imgheight))
	# Draw
	for number in amount:
		digit = BIGDIGITS[number]
		if number == ',':
			canvas.paste(digit, box=(x, imgheight - digit.height + 3), mask=digit)
		else:
			canvas.paste(digit, box=(x, imgheight - digit.height), mask=digit)
		x += digit.width + spacing
	return canvas

def small(amount):
	imgwidth = 0
	imgheight = 16
	spacing = 1
	x = 0
	# Calculate width of image
	for number in amount:
		imgwidth += SMALLDIGITS[number].width + spacing
	canvas = Image.new('RGBA', (imgwidth, imgheight))
	# Draw
	for number in amount:
		digit = SMALLDIGITS[number]
		if number == ',':
			canvas.paste(digit, box=(x, imgheight - digit.height + 3), mask=digit)
		else:
			canvas.paste(digit, box=(x, imgheight - digit.height), mask=digit)
		x += digit.width + spacing
	return canvas


def draw(mail, amount, debug=False):
	template = Image.open('joy_template.png')
	draw = ImageDraw.Draw(template)
	amount = '{:,}'.format(int(amount))
	bigd = big(amount)
	smalld = small(amount)
	template.paste(bigd, box=(BIG_CORNER - bigd.width, BIG_VERT), mask=bigd)
	template.paste(smalld, box=(SMALL_CORNER - smalld.width, SMALL_VERT), mask=smalld)

	mail = str(mail) + random.choice(MAILS)
	font = ImageFont.truetype('fonts/joycasino/email.ttf', 30)
	draw.text((EMAIL_CORNER, EMAIL_VERT), mail, font=font)

	if debug:
		template.save('joyexample.png')
	else:
		output = BytesIO()
		template.save(output, format='PNG')
		output.seek(0)
		return ('temp.PNG', output)

if __name__ == "__main__":
	draw('abas', 123000, debug=True)