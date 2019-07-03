import telegram_chat_drawer as tcdrawer
from PIL import Image
from io import BytesIO

CORNER = 1074

def chat(chatlist, name, avatar, online, debug=False):
	# chatlist {}
	# sender int - 0 - you 1 - other
	# textlist [] - list of strings
	# time string - format '1020'
	template = Image.open('source/telegram/template.png')
	image = Image.new('RGBA', (750, 3000), color=(24,34,45))
	timeList = []
	chatlist.reverse()
	y = 0
	if len(chatlist) == 0:
		timeList.append('0000')
	for chatMessage in chatlist:
		timeList.append(chatMessage['time'])
		messages = tcdrawer.bubble(chatMessage['textlist'], chatMessage['time'], int(chatMessage['sender']))
		if chatMessage['sender'] == 0:
			image.paste(messages, (image.width - messages.width - 8, image.height - messages.height - y))
		else:
			image.paste(messages, (8, image.height - messages.height - y))
		y += messages.height

	header = tcdrawer.header_draw(name, avatar, online)
	statusbar = tcdrawer.statusbar_draw(max(timeList))
	result = Image.new('RGB', (750, header.height + template.height + statusbar.height))
	template.paste(image, (0, CORNER - image.height))
	result.paste(template, (0, header.height))
	result.paste(header, (0, 40))
	result.paste(statusbar, (0, 0))
	

	if not debug:
		output = BytesIO()
		result.save(output, format='PNG')
		output.seek(0)
		return ('temp.PNG', output)
	else:
		result.save('output.png', format='PNG')
		return True


if __name__ == "__main__":
	chat([],'Норка Шубачаан', Image.open('ebalo.jpg'), online=4,  debug=True)