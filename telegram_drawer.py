from PIL import Image, ImageFont, ImageDraw
import random

FOLDER = 'source/telegram/'

TEXTFONT = ImageFont.truetype(FOLDER + 'SFUIText-RegularG2.otf', 33)
TIMEFONT = ImageFont.truetype(FOLDER + 'SFUIText-Lightitalic.ttf', 22)

SENT = {'botl': Image.open(FOLDER + 'sent/botl.png'),
		'botr': Image.open(FOLDER + 'sent/botr.png'),
		'topl': Image.open(FOLDER + 'sent/topl.png'),
		'topr': Image.open(FOLDER + 'sent/topr.png'),
		'tail': Image.open(FOLDER + 'sent/tail.png'),
		'topr_glad': Image.open(FOLDER + 'sent/topr_glad.png'),
		'sent': Image.open(FOLDER + 'sent/sent.png')}

TIME = str(random.randint(0,23) + random.randint(0,60))

def time_draw(time):
	time = time[:-2] + ':' + time[-2:]
	im = Image.new('RGB', TIMEFONT.getsize(time), color=(61, 106, 151))
	draw = ImageDraw.Draw(im)
	draw.text((0, 0), time, font=TIMEFONT, fill=(140, 176, 203))
	return im

def text_draw(text):
	# calculate
	limit = 583
	textCoords = {}
	textSplit = text.split(' ')
	spacing = 6
	space = 10
	xlog = []
	ylog = []
	x, y = (0, 0)
	for index, word in enumerate(textSplit):
		curwidth = TEXTFONT.getsize(word)[0]
		futureWidth = curwidth + x + space
		if futureWidth >= limit:
			y += TEXTFONT.getsize(word)[1] + spacing
			x = 0
			textCoords.update({word + str(index) : (x, y)})
			x += curwidth + space	
		else:
			textCoords.update({word + str(index) : (x, y)})
			x += curwidth + space
			ylog.append(TEXTFONT.getsize(word)[1])
			xlog.append(x)
	print(textCoords)

	im = Image.new('RGBA', (max(xlog), y + max(ylog)), color=(61, 106, 151))
	draw = ImageDraw.Draw(im)
	for index, word in enumerate(textSplit):
		draw.text(textCoords[word + str(index)], word, font=TEXTFONT, fill=(255, 255, 255))
	return im, y

def sent(textList, time):
	time = time_draw(time)
	imgs = []
	marginTop = 12
	marginBot = 21
	marginRight = 115
	marginLeft = 26
	results = []
	for index, text in enumerate(textList):
		text, y = text_draw(text)
		print(text)
		if y == 0:
			height = 70
			width = marginRight + marginLeft + text.width
		else:
			height = marginTop + marginBot + text.height
			width = marginRight + marginLeft + text.width - 103
		result = Image.new('RGB', (width + 12, height), color=(24,34,45))
		img = Image.new('RGB', (width, height), color=(61, 106, 151))
		img.paste(SENT['topl'], box=(0,0))
		img.paste(SENT['topr'], box=(width - SENT['topr'].width, 0))
		img.paste(SENT['botl'], box=(0, height - SENT['botl'].height))
		img.paste(SENT['botr'], box=(width - SENT['botr'].width, height - SENT['botr'].height))
		if index == 0:
			img.paste(SENT['topr_glad'], box=(width - SENT['topr_glad'].width, 0))
		if text.height == 32:
			pass
		img.paste(text, box=(marginLeft, marginTop))
		result.paste(img, box=(0, 0))
		if index == len(textList) - 1:
			result.paste(SENT['tail'], box=(result.width - SENT['tail'].width, result.height - SENT['tail'].height))
		result.paste(SENT['sent'], box=(result.width - 59, result.height - SENT['sent'].height - 17))
		result.paste(time, box=(result.width - 119, result.height - time.height - 17))
		results.append(result)

	size = [[], 0]
	spacing = 4
	for result in results:
		size[0].append(result.width)
		size[1] += result.height + spacing

	resultImage = Image.new('RGB', (max(size[0]), size[1]), color=(24,34,45))

	y = 0
	for result in results:
		resultImage.paste(result, box=(resultImage.width - result.width, y))
		y += result.height + spacing

	return resultImage

if __name__ == "__main__":
	sent(['Абашкевич','Абас', 'Саайсан ылыан да миигин?😄'], '1822').save('output.png')
	text_draw('Ты пидор')[0].save('print.png')