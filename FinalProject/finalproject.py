import flask
import telebot
import os
from russtress import Accent
import re
import random
from keras import backend as K

TOKEN = os.environ["TOKEN"]


bot = telebot.TeleBot(TOKEN, threaded=False)


bot.remove_webhook()
bot.set_webhook(url="https://app-mayakovsky.herokuapp.com/bot")

app = flask.Flask(__name__)


@bot.message_handler(commands=['start', 'info'])
def send_welcome(message):
	K.clear_session()
	greets = [
	'Здравствуй, мое предсмертное солнце,\nсолнце Аустерлица!',
	'Здравствуй и прощай, седая бабушка.', 'Здрасите!',
	'Здравствуй, Нетте!', 'Здрасьте.', 'Здравствуйте, дети!',
	'Нерон! Здравствуй!', 'Привет, КИМ!',
	'Привет делегатке!']
	bot.send_message(
	message.chat.id, """{}\nЯ бот,
	который обожает стихи В. В. Маяковского и хочет делиться ими с миром!\n
	Я могу ответить на сообщение, написанное на русском языке,
	рифмующейся строкой из Маяковского.\n
	Я был создан в рамках финального проекта
	студенткой 2 курса ФиКЛ Вышки.
	Подробнее о моём создании можно прочесть здесь:https://github.com/ershovamary/python_homework_second/tree/master/FinalProject.
	""".format(random.choice(greets)))


@bot.message_handler(commands=['help'])
def help_command(message):
	K.clear_session()
	bot.send_message(message.chat.id, "Вы пишите любое сообщение на русском языке. \
	А я привожу вам просто цитаты из сердца и из стиха!")


def find_rhyme(stressed_vowels):
	variants = []
	with open("Mayakovsky.csv", "r", encoding="utf-8") as f:
		for line in f.readlines():
			regAccented = re.compile("\w'", re.DOTALL)
			l = regAccented.findall(line)
			if l == stressed_vowels:
				variants.append(line)
	if variants:
		return random.choice(variants)
	return None


def find_source(result):
	with open("Mayakovsky.csv", "r", encoding="utf-8") as f:
		text = f.read()
		regResult = re.compile(result + r'.*?(\[.*?\])', re.DOTALL)
		m = regResult.search(text)
		return m.group(1)


@bot.message_handler(regexp="[а-яёА-ЯЁ]+[.,?!]*")
def get_rhyme(message):
	K.clear_session()
	accent = Accent()
	text = message.text
	accented_text = accent.put_stress(text)
	regAccented = re.compile("\w'", re.DOTALL)
	stressed_vowels = regAccented.findall(accented_text)
	result = find_rhyme(stressed_vowels)
	while result is None:
		stressed_vowels.pop(0)
		result = find_rhyme(stressed_vowels)
	source = find_source(result)
	regStress = re.compile("'", re.DOTALL)
	result = regStress.sub('', result)
	bot.send_message(message.chat.id, result + "\nИсточник:\n" + source)


@bot.message_handler(func=lambda m: True)
def send_len(message):
	K.clear_session()
	bot.send_message(
	message.chat.id, '''Как бы вам бы объяснить\nэто состояние?\n
	В вашем сообщении присутствуют символы,
	которые мне не удаётся обработать...
	Может быть, у вас в горле застревают английского огрызки?
	Может быть вы ошибку допустили в чертежах?
	Надо писать и описывать заново!''')


@app.route("/", methods=['GET', 'HEAD'])
def index():
	return 'ok'


# страница для нашего бота
@app.route("/bot", methods=['POST'])
def webhook():
	if flask.request.headers.get('content-type') == 'application/json':
		json_string = flask.request.get_data().decode('utf-8')
		update = telebot.types.Update.de_json(json_string)
		bot.process_new_updates([update])
		return ''
	else:
		flask.abort(403)

if __name__ == '__main__':
	app.debug = True
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
