from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import random

# Our folder
FOLDER = "source/sms/"
#Prepare Bubble Files
template = Image.open(FOLDER + 'template.png')
RECT_COLOR = (229, 229, 234) # Material Grey
topl = Image.open(FOLDER + 'rectangle/topl.png')
topr = Image.open(FOLDER + 'rectangle/topr.png')
botl = Image.open(FOLDER + 'rectangle/botl.png')
botr = Image.open(FOLDER + 'rectangle/botr.png')
triangle = Image.open(FOLDER + 'rectangle/triangle.png')
HEADER900 = Image.open(FOLDER + '900header.png')
DATES = ['Сегодня', 'Вчера', 'Позавчера']


def datetime(date, time):
	# int date : 0 - today, 1 - yesterday, 2 - before yesterday
	# str time : '1220' will turn 12:20
	fontcolor = (142, 142, 147)
	time = time[:-2] + ':' + time[-2:]
	datefont = ImageFont.truetype(FOLDER + 'SFUIText-Medium.ttf', size=22)
	timefont = ImageFont.truetype(FOLDER + 'SFUIText-Light.ttf', size=22)
	datesize = datefont.getsize(DATES[date])
	timesize = timefont.getsize(time)
	canvas = Image.new('RGBA', (datesize[0] + timesize[0] + 9, max(datesize[1], timesize[1])))
	draw = ImageDraw.Draw(canvas)
	draw.text((0, 0),DATES[date], font=datefont, fill=fontcolor)
	draw.text((datesize[0] + 9, 0), time, font=timefont, fill=fontcolor)
	img = Image.new('RGBA', (750, 80))
	img.paste(canvas, box=(round(img.width/2 - canvas.width/2), 40), mask=canvas)
	return img

def text_draw(text):
	textfont = ImageFont.truetype(FOLDER + 'SFUIText-Medium.ttf', size=31)
	MAXTEXTWIDTH = 490
	MAXTEXTVERT = textfont.getsize(text)[1]
	text = text.split(' ')
	textwidths = []
	textcoords = {}
	textvert = MAXTEXTVERT
	x = 0
	y = 0
	space = 10
	spacing = 0
	for index, word in enumerate(text):
		cursize = textfont.getsize(word)[0]
		futurewidth = x + cursize + space
		textwidths.append(x)
		if futurewidth >= MAXTEXTWIDTH:
			textvert += MAXTEXTVERT + spacing
			x = 0
			y += MAXTEXTVERT
			textcoords.update({word + str(index): (x, y)})
			x += cursize + space
		else:
			textcoords.update({word + str(index): (x, y)})
			x += cursize + space

	img = Image.new('RGBA', (max(textwidths), textvert))
	draw = ImageDraw.Draw(img)
	for index, word in enumerate(text):
		coords = textcoords[word + str(index)]
		if word.isdigit() and len(word) > 4:
			draw.text(textcoords[word + str(index)], word, font=textfont, fill=(0, 122, 255))
			draw.line(((coords[0], coords[1] + 31), (coords[0] + textfont.getsize(word)[0], coords[1] + 31)), width=2, fill=(0, 122, 255))
		else:
			draw.text(textcoords[word + str(index)], word, font=textfont, fill=(0, 0, 0))
	return img


def bubble(text, new=True):
	padding = 25
	paddingvert = 23
	text = text_draw(text)
	width = text.width + padding * 2
	height = text.height + paddingvert * 2 # 50 - padding

	content = Image.new('RGB', (width, height), RECT_COLOR)
	# Corners of the bubble
	content.paste(topl, box=(0,0), mask=topl)
	content.paste(topr, box=(content.width - topr.width,0), mask=topr)
	content.paste(botl, box=(0,content.height - botl.height), mask=botl)
	content.paste(botr, box=(content.width - topr.width, content.height - botl.height), mask=botr)
	content.paste(text, box=(padding, paddingvert), mask=text)
	img = Image.new('RGBA', (content.width + triangle.width - 10, content.height))
	img.paste(content, box=(10, 0))

	if new:
		img.paste(triangle, box=(0, img.height - triangle.height), mask=triangle)

	return img


def draw(smslist, debug=False):
	img = Image.new('RGBA', (750, 1150))
	spacing = 18
	oneminutespacing = 2
	y = 1150
	for sms in smslist:
		sms = sms.split('#')
		# Date
		if sms[0] == 'ДД':
			item = datetime(int(sms[1]), sms[2])
			y -= item.height
			img.paste(item, box=(0, y))
		elif sms[0].lower() == 'б':
			item = bubble(sms[1], new=False)
			y -= item.height + oneminutespacing
			img.paste(item, box=(21, y))
		elif sms[0].lower() == 'с':
			item = bubble(sms[1])
			y -= item.height + spacing
			img.paste(item, box=(21, y))
		else:
			item = bubble(sms[0])
			y -= item.height + spacing
			img.paste(item, box=(21, y))
		

	template.paste(img, box=(0, 913 - img.height), mask=img)

	headerfont = ImageFont.truetype(FOLDER + 'SFUIText-Medium.ttf', size=23)
	draw = ImageDraw.Draw(HEADER900)
	amountofsms = str(random.randint(1, 999))
	headersize = headerfont.getsize(amountofsms)
	draw.text((83 - headersize[0]/2, 38 - headersize[1]/2), amountofsms, font=headerfont, fill=(255,255,255))

	outputimage = Image.new('RGBA', (750, 1297))
	outputimage.paste(template, box=(0, 147))
	outputimage.paste(HEADER900, box=(0,0))

	if not debug:
		output = BytesIO()
		outputimage.save(output, format='PNG')
		output.seek(0)
		return ('temp.PNG', output) # For Telepot (TELEGRAM BOT)
	elif debug == 'Module':
		return outputimage
	else:
		outputimage.save('output.png', format='PNG')
		return True


if __name__ == "__main__":
	#bubble('VISA4734 28.06.19 Зачисление 14500 руб. от отправителя Артём В. Сообщение: "на ком. расходы', new=True).save('hui.png')
	draw(['с#Абастар сука', 'б#Ааспыкка миигин кырбаабыттара уонна 10000 солкуобайга ыйаабыттара', 'с#Пиздалар блэ', 'ДД#0#1245','с#Бля утуй сука заебал дииллэр','б#пиздец нахуй бля', '8989898989', 'с#Бу суоьулэри кытта корустум','Ол сука'], debug=True)
