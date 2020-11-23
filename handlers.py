from tarantool_utils import *
from random import randint, choice
from PIL import Image, ImageDraw, ImageFont
import json
import sys
import os


def scale_image(input_image_path, width=None, height=None):
	original_image = Image.open(input_image_path)
	w, h = original_image.size

 
	if width and height:
		max_size = (width, height)
	elif width:
		max_size = (width, h)
	elif height:
		max_size = (w, height)
	else:
		raise RuntimeError('Width or height required!')
 
	original_image.thumbnail(max_size, Image.ANTIALIAS)
	return original_image


def separation_text(text, count):
	len_str = 0
	text_list = ['']
	for index, c in enumerate(text.split(' ')):
		if len(text_list[-1].split('\n')) >= 2:
			split = text_list[-1].split('\n')
			text_list[-1] = split[0]
			len_str = len(split[1]) + 8
			text_list.append("—" + split[1])
		else:
			len_str += len(c) + 1
		if len_str < count:
			text_list[-1] +=  f" {c}"
		else:
			len_str = len(c) + 1
			text_list.append(c)

	return [c.strip() for c in text_list]


def new_foto(text, fon=True):
	configs_path = os.path.realpath(os.path.dirname(sys.argv[0])) + "/"
	if fon:
		base = scale_image(configs_path + 'fon/' + str(randint(1, 4)) + '.jpg', height=450).convert('RGBA')
	txt = Image.new('RGBA', (600, 600), (0,0,255,0))
	d = ImageDraw.Draw(txt)
	fnt = ImageFont.truetype(configs_path + 'Brush font one.otf', size=16)
	text = text.replace('–', '-')
	text = separation_text(text, 50)
	text[0] = "—" + text[0]
	if len(text) >= 23:
		if fon:
			tetrad = Image.open(configs_path + 'notebook/2.png').convert('RGBA')
			draw = ImageDraw.Draw(tetrad)
			draw.multiline_text((60, 11), '\n'.join(text[:17]), font=fnt, fill=(5, 4, 170, 165), spacing=8)
			draw.multiline_text((335, 12),  '\n'.join(text[17:34]), font=fnt, fill=(5, 4, 170, 165), spacing=8)	
		else:
			tetrad = Image.open(configs_path + 'notebook/4.png').convert('RGBA')
			draw = ImageDraw.Draw(tetrad)
			draw.multiline_text((53, 3), '\n'.join(text[:17]), font=fnt, fill=(5, 4, 170, 165), spacing=8)
			draw.multiline_text((335, 12),  '\n'.join(text[17:34]), font=fnt, fill=(5, 4, 170, 165), spacing=8)	

		rand = randint(1, 3)
		if rand == 1:
			sh21 = scale_image(configs_path + 'foto/21.png', height=265)
			tetrad.paste(sh21, (600, 100),  sh21)
		elif rand == 2:
			sh22 = scale_image(configs_path + 'foto/22.png', height=265)
			tetrad.paste(sh22, (620, 100),  sh22)

		x_base_paste = 70
		y_base_paste = 25
	else:
		fnt = ImageFont.truetype(configs_path + 'Brush font one.otf', size = 29)
		if fon:
			tetrad = Image.open(configs_path + 'notebook/1.png').convert('RGBA')
			draw = ImageDraw.Draw(tetrad)
			draw.multiline_text((33, 61), '\n'.join(text), font=fnt, fill=(5, 4, 170, 165), spacing=8)
		else:
			tetrad = Image.open(configs_path + 'notebook/3.png').convert('RGBA')
			draw = ImageDraw.Draw(tetrad)
			draw.multiline_text((33, 3), '\n'.join(text), font=fnt, fill=(5, 4, 170, 165), spacing=8)
		rand = randint(1, 3)
		if rand == 1:
			sh21 = scale_image(configs_path + 'foto/21.png', height=465)
			tetrad.paste(sh21, (550, 150),  sh21)
		elif rand == 2:
			sh22 = scale_image( configs_path + 'foto/22.png', height=565)
			tetrad.paste(sh22, (570, 100),  sh22)	
		x_base_paste = 0
		y_base_paste = 0
		if fon:
			base = base.resize((500,520))
			tetrad.thumbnail((402,664), Image.ANTIALIAS)

	sh1 = scale_image(configs_path + 'foto/sh1.png', height=200)
	sh2 = scale_image(configs_path + 'foto/sh2.png', height=150)

	i = 0
	while i <= randint(0, 2):
		tetrad.paste(sh1, (randint(0, tetrad.size[0]), randint(0, tetrad.size[1])),  sh1)
		i += 1

	i = 0
	while i <= randint(0, 5):
		sh3 = scale_image(configs_path + 'foto/' + str(randint(1, 5)) + '.png', height=10).convert('RGBA')
		tetrad.paste(sh3, (randint(0, tetrad.size[0] - 50), randint(0, tetrad.size[1] - 20)),  sh3)
		i += 1

	random_name = configs_path + 'img/' + str(randint(0, 9999999)) + '_sfoto.png'
	if fon:
		base.paste(tetrad, (x_base_paste, y_base_paste),  tetrad)
		base.save(random_name)
	else:
		tetrad.save(random_name)
	return random_name


async def button_1(bot, event):
	await bot.answer_callback_query(query_id=event.data['queryId'])
	user = User(user_id=event.data['from']['userId']).get()
	if user.old_mes['text']:
		# ищем слово конспект, и проверяем то что оно стоит в конце	
		name = new_foto(user.old_mes['text'], fon=True)
		with open(name, 'rb') as file:
			await bot.send_file(
				chat_id=event.data['message']['chat']['chatId'],
				file=file
			)
			await bot.send_text(
				chat_id=event.data['message']['chat']['chatId'],
				text="Если нужно еще – присылай новый текст :)"
			)			
		user.old_mes['text'] = None
		os.remove(name)
		user.save()
	else:
		await bot.send_text(
			chat_id=event.data['message']['chat']['chatId'],
			text="Пришли текст, который нужно написать от руки - я пришлю тебе скан"
		)	


async def button_2(bot, event):
	await bot.answer_callback_query(query_id=event.data['queryId'])
	user = User(user_id=event.data['from']['userId']).get()
	if user.old_mes['text']:	
		name = new_foto(user.old_mes['text'], fon=False)
		with open(name, 'rb') as file:
			await bot.send_file(
				chat_id=event.data['message']['chat']['chatId'],
				file=file
				)
			await bot.send_text(
				chat_id=event.data['message']['chat']['chatId'],
				text=get_t.get_text('Готово!')
			)			
		user.old_mes['text'] = None
		os.remove(name)
		user.save()	
	else:
		await bot.send_text(
			chat_id=event.data['message']['chat']['chatId'],
			text=get_t.get_text('Пришли текст')
		)	


async def write_text(bot, event):
	user = User(user_id=event.data['from']['userId']).get()
	if user.old_mes['text'] is None:
		
		user.old_mes['text'] = event.data['text'].replace('ё', 'е')
	else:
		user.old_mes['text'] += " " + event.data['text'].replace('ё', 'е')
	await bot.send_text(
		chat_id=event.from_chat,
		text="Нужен фон стола?",
		inline_keyboard_markup="{}".format(json.dumps([
		[
			{"text": "Да", "callbackData": "call_back_id_1"}
		],

		[
			{"text": "Нет", "callbackData": "call_back_id_2"}
		]
		])))
	user.save()
	

async def start(bot, event):
	await bot.send_text(
			chat_id=event.from_chat,
			text="""https://files.icq.net/get/0cU7g000BJdXGIQY3Kz9sE5f9807a41ae
Привет! 🙂

Я могу написать за тебя конспект. Отправь текст, который нужно написать от руки, а я пришлю тебе фото листочка бумаги."""
		)	


async def media(bot, event):
	await bot.send_text(
			chat_id=event.from_chat,
			text="Пришли, пожалуйста, текстовое сообщение"
		)	