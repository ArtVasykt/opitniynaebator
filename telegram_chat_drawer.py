from PIL import Image, ImageFont, ImageDraw
from emoji import emoji, EMOJIES
import textwrap
import random

FOLDER = 'source/telegram/'

SENT = {'botl': Image.open(FOLDER + 'sent/botl.png'),
		'botr': Image.open(FOLDER + 'sent/botr.png'),
		'topl': Image.open(FOLDER + 'sent/topl.png'),
		'topr': Image.open(FOLDER + 'sent/topr.png'),
		'tail': Image.open(FOLDER + 'sent/tail.png'),
		'imgtail': Image.open(FOLDER + 'sent/imgtail.png'),
		'topr_glad': Image.open(FOLDER + 'sent/topr_glad.png'),
		'sent': Image.open(FOLDER + 'sent/sent.png'),
		'timelist[index]ect': Image.open(FOLDER + 'sent/timerect.png')}

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

def bubble()

if __name__ == "__main__":