import telebot
from telebot import types

token = "1678532360:AAG3iNv8KVbAfv61Ss6RQi-O1YdzCdI_AEg"

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет! Этот бот показывает ближайшие места на карте, связанные с "
                     "прекрасным Серебряным веком!")


@bot.message_handler(commands=["geo"])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)
    bot.register_next_step_handler(message, print_geo())


def print_geo(message):
    bot.send_message(message.chat.id, message.location)
    bot.send_message(message.chat.id,
                     "latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))


@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))


if __name__ == '__main__':
    bot.polling(none_stop=True)
