from PIL import Image
from io import BytesIO

def mark(target, waterimage):
	waterimage = waterimage.convert('RGBA')
	waterimage.putalpha(128)
	x = 0
	y = 0
	while True:
		print(x, y)
		if x < target.width:
			target.paste(waterimage, (x,y), mask=waterimage)
			x+= waterimage.width
		else:
			y+= waterimage.width
			x = 0
		if y >= target.height:
			break
	output = BytesIO()
	target.save(output, format='PNG')
	output.seek(0)
	return ('temp.PNG', output)

