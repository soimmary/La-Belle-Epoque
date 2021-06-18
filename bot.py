import csv
import telebot
from telebot import types
from geopy import distance


token = "1678532360:AAG3iNv8KVbAfv61Ss6RQi-O1YdzCdI_AEg"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Привет🤩! Этот бот показывает ближайшие места на карте, "
                                      "связанные с прекрасным Серебряным веком!\n"
                                      "Нажми на кнопку и поделись со мной своим текущим "
                                      "местоположением 🗺📍",
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, print_geo)


def print_geo(message):
    with open('info.csv', 'r') as csvf:
        reader = csv.reader(csvf, delimiter='\t')
        next(reader, None)

        distances = {}
        from_loc = (message.location.latitude, message.location.longitude)

        for elem in reader:
            place = elem[0]
            try:
                fact = elem[3]
            except IndexError:
                fact = ''
            to_loc = (float(elem[1]), float(elem[2]))
            dist = round(distance.distance(from_loc, to_loc).km, 2)
            distances[place] = (dist, fact)

        places = sorted(distances.items(), key=lambda item: item[1][0])[:5]
        for place in places:
            bot.send_message(message.chat.id, f'📍 _{place[0]}_. *~{place[1][0]} км*\n{place[1][1]}, parse_mode = "Markdown"')


if __name__ == '__main__':
    bot.polling(none_stop=True)
