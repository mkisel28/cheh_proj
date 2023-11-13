import telebot
from datetime import datetime
from telebot import types
import re
bot = telebot.TeleBot('6544599844:AAFn8631B3QGkzM_oTwf0JNdgoZw0DyvcHc')

file_path = 'resources.txt'

def normalize_url(url):
    url = re.sub(r"^(http://|https://)", "", url)   
    url = re.sub(r"^www\.", "", url)   
    return url.rstrip("/")

with open(file_path, 'r', encoding="UTF-8") as file:
    resource_list = [line.strip() for line in file.readlines()]
    
    
resource_list = [normalize_url(link) for link in resource_list]

@bot.message_handler(commands=['start'])
def start(message):
    instruction = (
        "ИНСТРУКЦИЯ:\n"
        "1. Копируем ссылку ресурса.\n"
        "2. Вставляем в строку диалога с ботом.\n"
        "3. Получаем результат."
    )
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item_clear_history = types.KeyboardButton('Проверить ресурс')
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}!\n\n{instruction}\n\nТеперь вы можете использовать команду /check для проверки ресурса и кнопку "Проверить ресурс".',
                     reply_markup=markup)


@bot.message_handler(commands=['check'])
def check(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, 'Введите сюда ссылку на ресурс для проверки.', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def process_message(message):
    if message.text.startswith('/start') or message.text.startswith('/check'):
        return
    current_date = datetime.now().strftime('%d.%m.%Y')

    user_input = message.text.lower()
    normalized_input = normalize_url(user_input)
    if normalized_input in resource_list:
        bot.send_message(message.chat.id, f'🔴 На дату {current_date}, ресурс {user_input} является экстремистским!')
    else:
        bot.send_message(message.chat.id,
                         f'✅ На дату {current_date}, {user_input} отсутствует в списке экстремистских ресурсов.')


if __name__ == '__main__':
    bot.polling(none_stop=True)
