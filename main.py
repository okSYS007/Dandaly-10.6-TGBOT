
import extensions
import telebot
from tokens import TOKEN_TG

MyBot = extensions.MyBot()

bot = telebot.TeleBot(TOKEN_TG)
 
greet_words = '''Введите <имя валюты цену которой вы хотите узнать> 
<имя валюты в которой надо узнать цену первой валюты> 
<количество первой валюты>
доступные валюты 
/values
/example'''

def curr_exist(curr):
    return False if MyBot.curr_dict.get(curr) == None else True

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, greet_words)
 
@bot.message_handler(commands=['values'])
def all_curr(message):
    curr_str = ''
    for i in MyBot.curr_dict.keys():
        curr_str += ''.join(i + ' ')
    bot.reply_to(message, curr_str)

@bot.message_handler(commands=['example'])
def send_welcome(message):
    bot.reply_to(message, 'for example. try: USD UAH 100')

@bot.message_handler(content_types=['text'])
def answer(message: telebot.types.Message):
    
    user_input = message.html_text.split()
    if len(user_input) > 3:
        try:
            raise extensions.APIException("Много параметров!")
        except Exception as e:
            bot.reply_to(message, e.message)
            return
              
    elif len(user_input) <= 2:
        try:
            raise extensions.APIException("Мало параметров!")
        except Exception as e:
            bot.reply_to(message, e.message)
            return
            
    user_input = list(map(lambda x: str(x).upper(), user_input))

    for curr in user_input[:2]:
        if not curr_exist(curr):
            try:
                raise extensions.APIException(f'Валюта {curr} не найдена')
            except Exception as e:
                bot.reply_to(message, e.message)
                return
    
    base    = user_input[0]
    quote   = user_input[1]
    amount  = int(user_input[2])

    bot.reply_to(message, MyBot.get_price(base, quote, amount))

bot.polling(none_stop=True)