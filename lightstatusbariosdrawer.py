from PIL import Image
import random
from io import BytesIO

FOLDER = 'source/ios_statusbar/iphone6/light/'

# 900 or any SMS or light generator
# coordinates
CONNECTION_POWER = (12, 9)
OPERATOR_CORNER = 54
BATTERY_CORNER = 652
PERCENT = (660, 10)
BICON_COORD = (686, 8)

CONNECTION_POWER_IMAGES = []
TIME = {}
BATTERY = {}
BICON = {}
DIGITHEIGHT = 19
WEAKDIGITS = ['1','2','4','7']

battery = random.randint(1, 100)

for i in range(1, 5):
	CONNECTION_POWER_IMAGES.append(Image.open(FOLDER + 'connection/' + str(i) + '.png'))

for i in range(0, 10):
	TIME.update({str(i): Image.open(FOLDER + 'time/' + str(i) + '.png')})

for i in range(0, 10):
	BATTERY.update({str(i): Image.open(FOLDER + 'battery/' + str(i) + '.png')})

for i in range(1, 11):
	BICON.update({str(i): Image.open(FOLDER + 'battery/b' + str(i) + '.png')})

# :) HARDCODE
if battery < 10:
	bicon = BICON['1']
elif battery < 20 and battery > 10:
	bicon = BICON['2']
elif battery < 30 and battery > 20:
	bicon = BICON['3']
elif battery < 40 and battery > 30:
	bicon = BICON['4']
elif battery < 50 and battery > 40:
	bicon = BICON['5']
elif battery < 60 and battery > 50:
	bicon = BICON['6']
elif battery < 70 and battery > 60:
	bicon = BICON['7']
elif battery < 80 and battery > 70:
	bicon = BICON['8']
elif battery < 90 and battery > 80:
	bicon = BICON['9']
elif battery < 100 and battery > 90:
	bicon = BICON['10']
else:
	bicon = BICON['10']

battery = str(battery)


TIME.update({':': Image.open(FOLDER + 'time/colon.png')})
NETWORK = [Image.open(FOLDER + 'connection/3G.png'), Image.open(FOLDER + 'connection/LTE.png')]
OPERATORS = [Image.open(FOLDER + 'operator/Yota.png'), Image.open(FOLDER + 'operator/Beeline.png')]
PERCENT_IMAGE = Image.open(FOLDER + 'battery/percent.png')

randomtime = '{0}{1}'.format(random.randint(0,23), random.randint(0,59))
# tuple COLOR: (255, 255, 255, 1) RGBA
# string TIME: '1220' HM 
def draw(time=randomtime, debug=False, color=(240,240,242)):
	cover = Image.new('RGBA', (750,40), color)
	connection = random.choice(CONNECTION_POWER_IMAGES)
	cover.paste(connection, box=CONNECTION_POWER, mask=connection)
	operator = random.choice(OPERATORS)
	cover.paste(operator, box=(OPERATOR_CORNER, 29 - operator.height), mask=operator)
	network = random.choice(NETWORK)
	cover.paste(network, box=(operator.width + OPERATOR_CORNER + 20, 28 - network.height), mask=network)

	time = time[:-2] + ':' + time[-2:] # format 12:00
	# calculate width
	spacing = 3
	cwidth = 0
	for digit in time:
		cwidth += TIME[digit].width + spacing
	canvas = Image.new('RGBA', (cwidth, DIGITHEIGHT), (0,0,0,1))
	# draw canvas
	x = 0
	for digit in time:
		height = TIME[digit].height
		if digit in WEAKDIGITS:
			height += 1
		elif digit == ':':
			height += 3
		canvas.paste(TIME[digit], box=(x, DIGITHEIGHT - height))
		x += TIME[digit].width + spacing

	cover.paste(canvas, box=(int(cover.width / 2 - canvas.width / 2), 10), mask=canvas)

	# calculate width
	spacing = 2
	cwidth = 0
	for digit in battery:
		cwidth += BATTERY[digit].width + spacing
	canvas = Image.new('RGBA', (cwidth, DIGITHEIGHT), (0,0,0,1))
	# draw canvas
	x = 0
	for digit in battery:
		height = BATTERY[digit].height
		if digit in WEAKDIGITS:
			height += 1
		canvas.paste(BATTERY[digit], box=(x, DIGITHEIGHT - height))
		x += TIME[digit].width + spacing
	cover.paste(canvas, box=(BATTERY_CORNER - canvas.width + 2, 10), mask=canvas)
	
	cover.paste(bicon, box=BICON_COORD, mask=bicon)
	cover.paste(PERCENT_IMAGE, box=PERCENT, mask=PERCENT_IMAGE)

	if not debug:
		output = BytesIO()
		cover.save(output, format='PNG')
		output.seek(0)
		return ('temp.PNG', output)
	elif debug == 'Module':
		return cover
	else:
		cover.save('output.png', format='PNG')
		return True


if __name__ == "__main__":
	draw(debug=True)