from PIL import Image, ImageDraw
from io import BytesIO
import random
import sys

SUM_VERT = 494
CARD_VERT = 421

SUMDIGITS = {}
SUMROUBLE = Image.open('fonts/sberbank/sum/Р.png')
CARDDIGITS = {}
CARDSTAR = Image.open('fonts/sberbank/card/star.png')

# SUMIMG
for i in range(0, 10):
	sumimg = Image.open('fonts/sberbank/sum/' + str(i) + '.png')
	SUMDIGITS.update({str(i):sumimg})

# CARDIMG
for i in range(0, 10):
	cardimg = Image.open('fonts/sberbank/card/' + str(i) + '.png')
	CARDDIGITS.update({str(i):cardimg})

def sum(amount):
	amount = int(amount)
	amount = '{:,}'.format(amount).replace(',', ' ')
	imgwidth = 0
	imgheight = 47
	roublespace = 9
	splitspacing = 16
	spacing = 3
	x = 0
	# Calculate width of image
	for number in amount:
		if number == ' ':
			imgwidth += splitspacing
		else:
			imgwidth += SUMDIGITS[number].width + spacing
	imgwidth += SUMROUBLE.width + roublespace
	canvas = Image.new('RGBA', (imgwidth, imgheight))
	# Draw
	for number in amount:
		if number == ' ':
			x += splitspacing
		else:
			digit = SUMDIGITS[number]
			canvas.paste(digit, box=(x, imgheight - digit.height), mask=digit)
			x += digit.width + spacing
	x += roublespace
	canvas.paste(SUMROUBLE, box=(x, imgheight - SUMROUBLE.height - 1), mask=SUMROUBLE)
	return canvas


def card(number):
	if len(str(number)) != 16:
		raise ValueError
	number = list(str(number))
	starnumbers = [6,7,8,9,10,11]
	for starnumber in starnumbers:
		number[starnumber] = '*'
	number = ''.join(number)
	number = ' '.join([number[i:i+4] for i in range(0, len(number), 4)]) # Adding space every 4 chars

	space = 10
	imgwidth = 0
	imgheight = 30 # maximal crazy
	spacing = 2
	x = 0
	# Calculate width of image
	for digit in number:
		if digit == '*':
			imgwidth += CARDSTAR.width + spacing
		elif digit == ' ':
			imgwidth += space
		else:
			imgwidth += CARDDIGITS[digit].width + spacing
	canvas = Image.new('RGBA', (imgwidth, imgheight))
	# Draw
	for digit in number:
		if digit == '*':
			canvas.paste(CARDSTAR, box=(x, 0), mask=CARDSTAR)
			x += CARDSTAR.width + spacing
		elif digit == ' ':
			x += space
		else:
			digit = CARDDIGITS[digit]
			canvas.paste(digit, box=(x, 0), mask=digit)
			x += digit.width + spacing
	return canvas


def draw(amount, cardnum, debug=False):
	template = Image.open('sberbank_template.png')
	sumnumber = sum(amount)
	cardnumber = card(cardnum)
	print(template.width, sumnumber.width)
	template.paste(sumnumber, box=(round((template.width-sumnumber.width)/2), SUM_VERT), mask=sumnumber)
	template.paste(cardnumber, box=(round((template.width-cardnumber.width)/2), CARD_VERT), mask=cardnumber)
	if debug:
		template.save('sberexample.png', format='PNG')
	else:
		output = BytesIO()
		template.save(output, format='PNG')
		output.seek(0)
		return ('temp.PNG', output)

if __name__ == "__main__":
	draw(1234567890, 1234567890123456, debug=True)