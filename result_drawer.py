from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import sys

RES = 1080 # WIDTH AND HEIGHT OF TEMPLATE
EXAMPLEFACE = 'faces/example1.jpg'

#REV AND START FONTS
STARTDIGITS = {}
REVDIGITS = {}
STARTROUBLE = Image.open('fonts/start/rouble.png')
REVROUBLE = Image.open('fonts/revenue/rouble.png')


for i in range(0,10):
	image = Image.open('fonts/start/' + str(i) + '.png')
	STARTDIGITS.update({i:image})

for i in range(0,10):
	image = Image.open('fonts/revenue/' + str(i) + '.png')
	REVDIGITS.update({i:image})


def rev(string):
	if type(string) is not str:
		string = str(string)
	imgwidth = 50 # starts with rouble width
	imgheight = 74 # maximal height of symbols
	spacing = 8
	for symbol in string:
		imgwidth += REVDIGITS[int(symbol)].width
		imgwidth += spacing
	canvas = Image.new('RGBA', (imgwidth, imgheight))
	x = 0
	for symbol in string:
		digit = REVDIGITS[int(symbol)]
		canvas.paste(digit, box=(x,imgheight - digit.height), mask=digit)
		x += digit.width + spacing
	canvas.paste(REVROUBLE, box=(x, imgheight - 69), mask=REVROUBLE)
	return canvas

def startd(string):
	if type(string) is not str:
		string = str(string)
	imgwidth = 62 # starts with rouble width
	imgheight = 91 # maximal height of symbols
	spacing = 8
	for symbol in string:
		imgwidth += STARTDIGITS[int(symbol)].width
		imgwidth += spacing
	canvas = Image.new('RGBA', (imgwidth, imgheight))
	x = 0
	for symbol in string:
		digit = STARTDIGITS[int(symbol)]
		canvas.paste(digit, box=(x,imgheight - digit.height), mask=digit)
		x += digit.width + spacing
	canvas.paste(STARTROUBLE, box=(x, imgheight - 85), mask=STARTROUBLE)
	return canvas


def draw(face, name, age, start, revenue, debug=False):
	template = Image.open('result_template.png')
	# Ширина 380п Высота 380п
	# x: 68 y: 197
	if debug:
		face = Image.open(EXAMPLEFACE)
	face.resize((380,380))
	mask = Image.open('facemask.png') # Круглость
	print(mask.size, mask.mode)
	print(face.size, face.mode)
	template.paste(face, box=(68, 197), mask=mask)

	draw = ImageDraw.Draw(template)
	# NAME
	helb = ImageFont.truetype('HelveticaNeueCyr-Bold.ttf', 36)
	w, h = helb.getsize(name.upper())
	draw.text((((RES/2)-w)/2, 628.7), name.upper(), font=helb) # NAME
	# AGE
	age += ' лет'
	hell = ImageFont.truetype('HelveticaNeueCyr-Light.ttf', 28)
	w, h = hell.getsize(age)
	draw.text((((RES/2)-w)/2,665), age, font=hell)
	# START
	start = startd(start)
	template.paste(start, box=(RES-start.width, 450), mask=start)
	# REVENUE
	revenue = rev(revenue)
	template.paste(revenue, box=(RES-revenue.width, 796), mask=revenue)


	if not debug:
		output = BytesIO()
		template.save(output, format='PNG')
		output.seek(0)
		return ('temp.PNG', output)
	else:
		template.save('output.png', format='PNG')
		return True

if __name__ == "__main__":
	a = sys.argv
	draw(a[1], a[2], a[3], a[4], a[5], debug=True)