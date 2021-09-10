import telebot
import requests
import json
from PIL import Image
from questions import questions
from random import randint

bot = telebot.TeleBot('1911835877:AAEH9rJDoZrsxS87FocZfoORCoHd4zGEjz0')

@bot.message_handler(commands=['start'])
def start(message):
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	hello = telebot.types.KeyboardButton('Hello!')
	how_are_you = telebot.types.KeyboardButton('How are you?')
	tell = telebot.types.KeyboardButton('Tell me smth')
	keyboard.add(hello, how_are_you, tell)
	bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!', reply_markup=keyboard)


@bot.message_handler(commands=['brand'])
def decode(message):
	keyboard = telebot.types.InlineKeyboardMarkup()
	apple = telebot.types.InlineKeyboardButton('Apple', 'https://apple.com')
	samsung = telebot.types.InlineKeyboardButton('Samsung', 'https://samsung.com')
	keyboard.add(apple, samsung)
	bot.send_message(message.chat.id, "Click button", reply_markup=keyboard)


@bot.message_handler(commands=['test'])
def test(message):
	keyboard = telebot.types.InlineKeyboardMarkup()
	index = randint(0, len(questions) - 1)
	question = questions[index]
	for i in range(len(question["variants"])):
		variant = telebot.types.InlineKeyboardButton(
			text=question['variants'][i]['name'],
			callback_data=question['variants'][i]['true']
		)
		keyboard.add(variant)
	bot.send_message(message.chat.id, question['question'], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "true":
    	bot.send_message(call.message.chat.id, "You're right!")
    else:
    	bot.send_message(call.message.chat.id, "No")



@bot.message_handler(commands=['forecast'])
def forecast(message):
	l = message.text.split()
	message.text = l[-1]
	get_forecast(message)


def get_forecast(message):
	url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

	querystring = {"q": message.text,"days": "2"}

	headers = {
	    'x-rapidapi-host': "weatherapi-com.p.rapidapi.com",
	    'x-rapidapi-key': "c83e7d750dmshcde9415b4bd29b2p1fdd2ajsnc5945f3ce5bb"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	data = json.loads(response.text)
	data = data['forecast']['forecastday'][1]
	bot.send_message(message.chat.id, f"Average temperature is {data['day']['avgtemp_c']}\n" +
		f"Average humidity is {data['day']['avghumidity']}%")

	response = requests.request("GET", "https:" + data['day']['condition']['icon'])

	# file = open("weather_icon.png", "wb")
	# file.write(response.content)
	# file.close()

	with open("weather_icon.png", "wb") as file:
		file.write(response.content)

	with open("weather_icon.png", "rb") as file:
		bot.send_photo(message.chat.id, file)

	get_size_image = Image.open('weather_icon.png')
	size = get_size_image.size


	image_background = Image.new('RGB', (size[0] * 6, size[1] * 4), (255, 255, 255))
	for i in range(24):
		row = i // 6
		column = i % 6

		response = requests.get('https:' + data['hour'][i]['condition']['icon'])
		with open(f"weather_icon_{i}.png", "wb") as file:
			file.write(response.content)

		weather_image = Image.open(f'weather_icon_{i}.png')
		image_background.paste(weather_image, (weather_image.size[0] * column, weather_image.size[1] * row), weather_image.split()[-1])
	image_background.save('weather_background.png')

	with open('weather_background.png', 'rb') as file:
		bot.send_photo(message.chat.id, file)    	


@bot.message_handler(content_types=['text'])
def text(message):
	keyboard = telebot.types.ReplyKeyboardRemove()
	if message.text.lower() == 'cancel keyboard':
		bot.send_message(message.chat.id, "I'm fine", reply_markup=keyboard)



# @bot.message_handler(content_types=['text'])
@bot.message_handler(commands=['definition'])
def definition(message):
	# bot.send_message(message.chat.id, message.text)
	l = message.text.split()
	if len(l) > 1:
		message.text = l[-1]
		get_definition(message)
	else:
		msg = bot.send_message(message.chat.id, "Please enter the word")
		bot.register_next_step_handler(msg, get_definition)


@bot.message_handler(commands=['definition2'])
def definition2(message):
	msg = bot.send_message(message.chat.id, "Please enter the word")
	bot.register_next_step_handler(msg, get_definition)


def get_definition(message):
	word = message.text
	url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/definitions"
	headers = {
	    'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
	    'x-rapidapi-key': "c83e7d750dmshcde9415b4bd29b2p1fdd2ajsnc5945f3ce5bb"
	}
	response = requests.request("GET", url, headers=headers)
	data = json.loads(response.text)
	print(data['definitions'])
	for el in data['definitions']:
		bot.send_message(message.chat.id, el['definition'])


def change_photo():
	image = Image.open('image.png')
	px = image.load()

	image2 = Image.new('RGB', image.size)

	print(px, type(px))
	print(image.size)

	for x in range(image.size[0]):
		for y in range(image.size[1]):
			mean = (px[x, y][0] + px[x, y][1] + px[x, y][2]) // 3
			image2.putpixel((x, y), (mean, mean, mean))

	image2.save('image2.png')


@bot.message_handler(content_types=['photo'])
def black_white_filter(message):
	# print(message)
	fileID = message.photo[-1].file_id
	file = bot.get_file(fileID)
	file_path = file.file_path
	download = bot.download_file(file_path)
	# with open('image.png', 'wb') as new_file:
	# 	new_file.write(download)
	new_file = open('image.png', 'wb')
	new_file.write(download)
	change_photo()
	file = open('image2.png', 'rb')
	bot.send_photo(message.chat.id, file)
	# print(download)





bot.polling(none_stop=True)


# def f(f2, x):
# 	return f2(x)

# def f2(x):
# 	return 2 * x


# print(f(f2, 5))


# def request(request_type, url, headers, params):
# 	return response

# def get(url, headers, params):
# 	return request("GET", url, headers, params)



# @bot.message_handler(commands=['start'])
# def start(message):
# 	keyboard = telebot.types.InlineKeyboardMarkup()
# 	url_button = telebot.types.InlineKeyboardButton(text='Decode School', url='https://decode.kz')
# 	keyboard.add(url_button)
# 	bot.send_message(message.chat.id, "Push me", reply_markup=keyboard)


# @bot.message_handler(commands=['start'])
# def start(message):
# 	keyboard = telebot.types.ReplyKeyboardMarkup()
# 	btna = telebot.types.KeyboardButton('a')
# 	btnb = telebot.types.KeyboardButton('b')
# 	btnc = telebot.types.KeyboardButton('c')
# 	btnd = telebot.types.KeyboardButton('d')
# 	btne = telebot.types.KeyboardButton('e')
# 	keyboard.row(btna, btnb)
# 	keyboard.row(btnc, btnd, btne)
# 	bot.send_message(message.chat.id, "Push me", reply_markup=keyboard)


# @bot.message_handler(content_types=['text'])
# def start(message):
# 	keyboard = telebot.types.ReplyKeyboardRemove(selective=True)
# 	bot.send_message(message.chat.id, "Hide keyboard", reply_markup=keyboard)