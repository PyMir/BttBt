import telebot
from telebot import types
from bittrex import Bittrex
import time

def get_pair(message):    
    my_bittrex = Bittrex(None,None)
    return(my_bittrex.get_ticker('BTC-'+ str(message)))

def get_summary(message):
    my_bittrex = Bittrex(None,None)
    return(my_bittrex.get_marketsummary('BTC-'+ str(message)))    

def get_kurs():
    my_bittrex = Bittrex(None,None)
    coins =['TRIG','NEO','ADX']
    sumbuy  = [0.00008899,0.00346663,0.00012222]
    col = [50,0.33,15,7,200]
    #col = [0.01,0.01,0.01,0.01,0.01]
    val = []
    resp = ""
    for item in coins:
        tmp = my_bittrex.get_ticker('BTC-'+ item)
        try:
            val.append(tmp['result']['Last'])
        except:
            val.append(0)
    resp = ""
    for i in range(len(coins)):
        resp = resp + coins[i]+' Tek: %.8f : %.8f (%.3f)\n' %(val[i],sumbuy[i],(val[i]-sumbuy[i])*col[i]*58*13500)
    return resp

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup.row('Курс')
    bot.send_message(message.chat.id, "Выбирай", reply_markup = markup)


@bot.message_handler(content_types=["text"])
def answer_on_messages(message):
    resp = ""
    if message.text == 'Курс':
        resp = get_kurs()
        keyboard = types.InlineKeyboardMarkup()
        btns = []
        btns.append(types.InlineKeyboardButton(text='Обновить', callback_data='Refresh'))
        keyboard.add(*btns)
    else:        
        res = get_pair(message.text)
        #try:
        resp = "Курс по паре BTC-"+ message.text+"\n" +"Покупка: " + str(res['result']['Ask']) + '\n' + "Продажа: " + str(res['result']['Bid']) + '\n' + "Последняя цена: " + str(res['result']['Last'])
        c='''resp = """Курс по паре BTC-%s
    Покупка: %.8f
    Продажа: %.8f
    Последняя цена: %.8f
    Минимум за день: %.8f
    Максимум за день: %.8f
    Вчера в это время: %.8f
                     """ % (message.text.upper(),res['result'][0]['Bid'],res['result'][0]['Ask'],res['result'][0]['Last'],res['result'][0]['Low'],res['result'][0]['High'],res['result'][0]['PrevDay'])'''
        #except:
        #resp = "Нет такой пары"
    bot.send_message(message.chat.id,resp,reply_markup = keyboard)

@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    if c.data =='Refresh':
        print("a")
        resp = get_kurs()
        keyboard = types.InlineKeyboardMarkup()
        btns = []
        btns.append(types.InlineKeyboardButton(text='Обновить', callback_data='Refresh'))
        keyboard.add(*btns)
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text=resp,reply_markup = keyboard)

if __name__ == '__main__':
    #try:
        bot.polling(none_stop = True)
    #except:
    #    print('Нет соединения с Интернетом!')
