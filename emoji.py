from PIL import Image

EMOJIES = {'💔':'broken-heart_1f494.png',
		   '😵':'dizzy-face_1f635.png',
		   '😘':'face-throwing-a-kiss_1f618.png',
		   '😂':'face-with-tears-of-joy_1f602.png',
		   '😳':'flushed-face_1f633.png',
		   '😀':'grinning-face_1f600.png',
		   '😄':'grinning-face-with-smiling-eyes_1f601.png',
		   '😁':'grinning-face-with-star-eyes_1f929.png'}

def emoji(symbol):
	if symbol not in EMOJIES:
		return ''
	else:
		return Image.open('source/telegram/emoji/' + EMOJIES[symbol]).resize((38, 38))