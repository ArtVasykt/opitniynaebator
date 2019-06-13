from PIL import Image, ImageDraw
from io import BytesIO
import random
import sys

BIG_CORNER = 204
BIG_VERT = 74
SMALL_CORNER = 202
SMALL_VERT = 94

BIGDIGITS = {}
SMALLDIGITS = {}

for i in range(0, 10):
	bigimg = Image.open('fonts/joybig/' + str(i) + '.png')
	BIGDIGITS.update({str(i):bigimg})
	smallimg = Image.open('fonts/joysmall/' + str(i) + '.png')
	SMALLDIGITS.update({str(i):smallimg})

BIGDIGITS.update({',': Image.open('fonts/joybig/,.png')})
SMALLDIGITS.update({',': Image.open('fonts/joysmall/,.png')})

def big(amount):
	imgwidth = 0
	imgheight = 10
	spacing = 0
	x = 0
	# Calculate width of image
	for number in amount:
		imgwidth += BIGDIGITS[number].width + spacing
	canvas = Image.new('RGBA', (imgwidth, imgheight))
	# Draw
	for number in amount:
		digit = BIGDIGITS[number]
		canvas.paste(digit, box=(x, imgheight - digit.height), mask=digit)
		x += digit.width + spacing
	return canvas

def small(amount):
	imgwidth = 0
	imgheight = 7
	spacing = 0
	x = 0
	# Calculate width of image
	for number in amount:
		imgwidth += SMALLDIGITS[number].width + spacing
	canvas = Image.new('RGBA', (imgwidth, imgheight))
	# Draw
	for number in amount:
		digit = SMALLDIGITS[number]
		canvas.paste(digit, box=(x, imgheight - digit.height), mask=digit)
		x += digit.width + spacing
	return canvas

def draw(minimal, maximal):
	template = Image.open('joy_template.png')
	amount = random.randint(minimal, maximal)
	amount = str(amount)
	amount = ':,'.format(amount)
	bigd = big(amount)
	smalld = small(amount)
	template.paste(bigd, box=(BIG_CORNER - bigd.width, BIG_VERT), mask=bigd)
	template.paste(smalld, box=(SMALL_CORNER - smalld.width, SMALL_VERT), mask=smalld)

	output = BytesIO()
	template.save(output, format='PNG')
	output.seek(0)
	return ('temp.PNG', output)