from PIL import Image, ImageFont, ImageDraw
from emoji import emoji, EMOJIES
import random

FOLDER = 'source/telegram/'

TEXTFONT = ImageFont.truetype(FOLDER + 'SFUIText-RegularG2.otf', 33)
TIMEFONT = ImageFont.truetype(FOLDER + 'SFUIText-LightItalic.ttf', 22)

SENT = {'botl': Image.open(FOLDER + 'sent/botl.png'),
		'botr': Image.open(FOLDER + 'sent/botr.png'),
		'topl': Image.open(FOLDER + 'sent/topl.png'),
		'topr': Image.open(FOLDER + 'sent/topr.png'),
		'tail': Image.open(FOLDER + 'sent/tail.png'),
		'imgtail': Image.open(FOLDER + 'sent/imgtail.png'),
		'topr_glad': Image.open(FOLDER + 'sent/topr_glad.png'),
		'sent': Image.open(FOLDER + 'sent/sent.png'),
		'timerect': Image.open(FOLDER + 'sent/timerect.png')}

RECEIVED = {'botl': Image.open(FOLDER + 'received/botl.png'),
		'botr': Image.open(FOLDER + 'received/botr.png'),
		'topl': Image.open(FOLDER + 'received/topl.png'),
		'topr': Image.open(FOLDER + 'received/topr.png'),
		'tail': Image.open(FOLDER + 'received/tail.png'),
		'imgtail': Image.open(FOLDER + 'sent/imgtail.png'),
		'topl_glad': Image.open(FOLDER + 'received/topl_glad.png')}

BARS = [Image.open(FOLDER + 'statusbar/1bar.png'),
		Image.open(FOLDER + 'statusbar/2bars.png'),
		Image.open(FOLDER + 'statusbar/3bars.png'),
		Image.open(FOLDER + 'statusbar/4bars.png')]

PERCENT = Image.open(FOLDER + 'statusbar/percent.png')
ADDITIONAL = [Image.open(FOLDER + 'statusbar/orientation.png')]
BATTERY = [Image.open(FOLDER + 'statusbar/battery/{0}.png'.format(str(x))) for x in range(0, 10)]

TIME = str(random.randint(0,23) + random.randint(0,60))

def time_draw(time, sender=0, isImage=False):
	time = time[:-2] + ':' + time[-2:]
	if sender == 0: 
		bgcolor = (61, 106, 151)
		textcolor = (140, 176, 203)
	else:
		bgcolor = (33, 48, 64)
		textcolor = (126, 147, 160)
	if not isImage:
		im = Image.new('RGB', TIMEFONT.getsize(time), color=bgcolor)
	else:
		textcolor = (255,255,255)
		im = Image.new('RGBA', TIMEFONT.getsize(time))
	draw = ImageDraw.Draw(im)
	draw.text((0, 0), time, font=TIMEFONT, fill=textcolor)
	return im

def text_draw(text, sender=0):
	# calculate
	limit = 583
	textCoords = {}
	emCoords = {}
	textSplit = text.split(' ')
	spacing = 6
	space = 10
	xlog = []
	ylog = []
	x, y = (0, 0)
	for index, word in enumerate(textSplit):
		curwidth = TEXTFONT.getsize(word)[0]
		emx = 0

		for emi, symbol in enumerate(word):
			print({symbol: word})
			if symbol in EMOJIES:
				word = word.replace(symbol, '', 1)
				emCoords.update({symbol + str(emi): (x + curwidth - 40 + emx, y)})
				emx += 42

				print(emCoords)
				print(emx)

		futureWidth = curwidth + x + space + emx
		if futureWidth >= limit:
			y += TEXTFONT.getsize(word)[1] + spacing
			x = 0
			textCoords.update({word + str(index) : (x, y)})
			x += curwidth + space + emx
		else:
			textCoords.update({word + str(index) : (x, y)})
			x += curwidth + space + emx
			ylog.append(TEXTFONT.getsize(word)[1])
			xlog.append(x)
	print(textCoords)

	if sender == 0:
		im = Image.new('RGBA', (max(xlog), y + max(ylog)), color=(61, 106, 151))
	else:
		im = Image.new('RGBA', (max(xlog), y + max(ylog)), color=(33, 48, 64))
	draw = ImageDraw.Draw(im)
	for index, word in enumerate(textSplit):
		for emi, symbol in enumerate(word):
			if symbol in EMOJIES:
				im.paste(emoji(symbol), box=emCoords[symbol + str(emi)], mask=emoji(symbol))
				word = word.replace(symbol, '', 1)
		draw.text(textCoords[word + str(index)], word, font=TEXTFONT, fill=(255, 255, 255))
	return im, y

def bubble(textList, timer, sender=0):
	# sender 0 - sender 1 - receiver
	imgs = []
	marginTop = 12
	marginBot = 21
	if sender == 0:
		marginRight = 115
	else:
		marginRight = 85
	marginLeft = 26
	results = []
	for index, text in enumerate(textList):
		if type(text) == str:
			time = time_draw(timer, sender=sender)
			print('SUKA' + text)
			isImage = False
			text, y = text_draw(text, sender=sender)
			print(time)
			if y == 0:
				height = 70
				width = marginRight + marginLeft + text.width
			else:
				height = marginTop + marginBot + text.height
				width = marginRight + marginLeft + text.width 
			result = Image.new('RGB', (width + 12, height), color=(24,34,45))
		else:
			time = time_draw(timer, sender=sender, isImage=True)
			print('YEah')
			isImage = True
			text = text.resize((text.width // 2, text.height // 2), resample=Image.LANCZOS)
			width = text.width - 12
			height = text.height - 17
			result = Image.new('RGB', (width + 12, height + 17), color=(24,34,45))

		if sender == 0:
			img = Image.new('RGBA', (width, height), color=(61, 106, 151))
			img.paste(SENT['topl'], box=(0,0))
			img.paste(SENT['topr'], box=(width - SENT['topr'].width, 0))
			img.paste(SENT['botl'], box=(0, height - SENT['botl'].height))
			img.paste(SENT['botr'], box=(width - SENT['botr'].width, height - SENT['botr'].height))
			if index == 0:
				img.paste(SENT['topr_glad'], box=(width - SENT['topr_glad'].width, 0))
			if isImage:
				if index == len(textList) - 1:
					im = Image.new('RGBA', (result.width, result.height))
					im.paste(img, (0,0), mask=img)
					im.paste(SENT['imgtail'], box=(text.width - 23, im.height - SENT['imgtail'].height - 18), mask=SENT['imgtail'])
				result.paste(text, box=(0,0), mask=im)
				result.paste(SENT['timerect'], box=(img.width - SENT['timerect'].width - 12, img.height - SENT['timerect'].height - 12), mask=SENT['timerect'])
				result.paste(SENT['sent'], box=(img.width - 49, img.height - 38), mask=SENT['sent'])
				result.paste(time, box=(round(img.width - 84 - time.width/2), img.height - 43), mask=time)
			else:
				img.paste(text, box=(marginLeft, marginTop))
				result.paste(img, box=(0, 0), mask=img)
				if index == len(textList) - 1:
					result.paste(SENT['tail'], box=(result.width - SENT['tail'].width, result.height - SENT['tail'].height))
				result.paste(SENT['sent'], box=(result.width - 59, result.height - SENT['sent'].height - 17), mask=SENT['sent'])
				result.paste(time, box=(result.width - 119, result.height - time.height - 17))
			results.append(result)
		else:
			img = Image.new('RGB', (width, height), color=(33, 48, 64))
			img.paste(RECEIVED['topl'], box=(0,0))
			img.paste(RECEIVED['topr'], box=(width - RECEIVED['topr'].width, 0))
			img.paste(RECEIVED['botl'], box=(0, height - RECEIVED['botl'].height))
			img.paste(RECEIVED['botr'], box=(width - RECEIVED['botr'].width, height - RECEIVED['botr'].height))
			if index == 0:
				img.paste(RECEIVED['topl_glad'], box=(0, 0))
			img.paste(text, box=(marginLeft, marginTop))
			result.paste(img, box=(result.width - img.width, 0))
			if index == len(textList) - 1:
				result.paste(RECEIVED['tail'], box=(0, result.height - RECEIVED['tail'].height))
			result.paste(time, box=(result.width - time.width - 26, result.height - time.height - 17))
			results.append(result)

	size = [[], 0]
	spacing = 4
	for result in results:
		size[0].append(result.width)
		size[1] += result.height + spacing

	resultImage = Image.new('RGB', (max(size[0]), size[1]), color=(24,34,45))

	y = 0
	for result in results:
		if sender == 0:
			resultImage.paste(result, box=(resultImage.width - result.width, y))
		else:
			resultImage.paste(result, box=(0, y))
		y += result.height + spacing

	return resultImage

def header_draw(name, avatar, online=1):
	nameFont = ImageFont.truetype(FOLDER + 'SFUIText-Medium.ttf', 33)
	mesFont = ImageFont.truetype(FOLDER + 'SFUIText-RegularG2.otf', 25)
	statusFont = ImageFont.truetype(FOLDER + 'SFUIText-Regular.ttf', 26)
	header = Image.open(FOLDER + 'header.png')

	draw = ImageDraw.Draw(header)
	# NAME
	textSize = nameFont.getsize(name)
	draw.text((header.width/2 - textSize[0]/2, 30 - textSize[1]/2), name, font=nameFont, fill=(255, 255, 255))
	# MESSAGE COUNT
	mesCount = str(random.randint(1, 99))
	textSize = mesFont.getsize(mesCount)
	draw.text((56 - textSize[0]/2, 18 - textSize[1]/2), mesCount, font=mesFont, fill=(255,255,255))
	# status
	if online == 0:
		status = 'в сети'
		color = (45, 163, 251)
	elif online == 1:
		status = 'был(а) только что'
		color = (139, 145, 151)
	else:
		status = 'был(а) {0} минут назад'.format(online)
		color = (139, 145, 151)
	textSize = statusFont.getsize(status)
	draw.text((header.width / 2 - textSize[0] / 2, 65 - textSize[1] / 2), status, font=statusFont, fill=color)
	mask = Image.open(FOLDER + 'mask.png')
	avatar = avatar.resize((74, 74))
	header.paste(avatar, box=(664, 8), mask=mask)

	return header

def statusbar_draw(time):
	time = time[:-2] + ':' + time[-2:]
	heightline = 29
	battery = random.randint(1,99)
	batimage = BATTERY[round((battery / 10) - 1)]
	textFont = ImageFont.truetype(FOLDER + 'SFUIText-Regular.ttf', 24)
	bar = random.choice(BARS)
	rect = Image.new('RGB', (750, 40), color=(33, 48, 64))
	rect.paste(bar, (12, 10))
	draw = ImageDraw.Draw(rect)
	text1Size = textFont.getsize('Билайн')
	draw.text((54, heightline - text1Size[1]), 'Билайн', font=textFont, fill=(255,255,255))
	connection = random.choice(['LTE', '3G'])
	text2Size = textFont.getsize(connection)
	draw.text((54 + text1Size[0] + 20, heightline - text2Size[1]), connection, font=textFont, fill=(255,255,255))
	text3Size = textFont.getsize(time)
	draw.text((rect.width/2 - text3Size[0] / 2, heightline - text3Size[1]), time, font=textFont, fill=(255,255,255))
	text4Size = textFont.getsize(str(battery))
	draw.text((638 - text4Size[0] / 2, heightline - text4Size[1]), str(battery), font=textFont, fill=(255,255,255))
	rect.paste(batimage, box=(686, 8), mask=batimage)
	rect.paste(PERCENT, box=(660, 11))

	return rect

if __name__ == "__main__":
	bubble(['Абашкевич','Абас', 'Саайсан ылыан да миигин?💔 Cуох бо сука😀'], '1822', sender=1).save('output.png')
	text_draw('Ты пидор')[0].save('print.png')
	header_draw('Абас Григорьев', Image.open('ebalo.jpg'), online=1).save('ebalnik.png')