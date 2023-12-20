import telebot
from datetime import datetime
from telebot import types
import re
import os
import time

bot = telebot.TeleBot('6544599844:AAFn8631B3QGkzM_oTwf0JNdgoZw0DyvcHc')


data_folder = '/usr/src/app/data'

os.makedirs(data_folder, exist_ok=True)

users_file = os.path.join(data_folder, 'users.txt')
file_path = os.path.join(data_folder, 'resources.txt')

# ID уполномоченного пользователя для рассылки
authorized_user_id = [5446991838, 1689568914]  # Замените на реальный ID

def normalize_url(url):
    url = re.sub(r"^(http://|https://)", "", url)   
    url = re.sub(r"^www\.", "", url)   
    return url.rstrip("/")

def get_resource_list():
    with open(file_path, 'r', encoding='utf-8') as file:
        resource_list = [line.strip().lower() for line in file.readlines()]
    resource_list_2 = [normalize_url(link) for link in resource_list]
    
    return resource_list+resource_list_2

def read_users():
    if not os.path.exists(users_file):
        return []
    with open(users_file, 'r') as file:
        return [line.strip() for line in file.readlines()]


# Сохранение ID пользователя
def save_user(user_id):
    if not os.path.exists(users_file):
        with open(users_file, 'w') as file:
            file.write(f"{user_id}\n")
    else:
        with open(users_file, 'a') as file:
            file.write(f"{user_id}\n")


@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)
    if user_id not in read_users():
        save_user(user_id)
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


@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.chat.id in authorized_user_id:
        bot.send_message(message.chat.id, "Введите сообщение для рассылки:")
        bot.register_next_step_handler(message, send_broadcast)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этой команды.")


def send_broadcast(message):
    users = read_users()
    for user_id in users:
        try:
            bot.send_message(user_id, message.text)
            time.sleep(0.1)
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
    bot.send_message(message.chat.id, "Рассылка проведена успешна")


@bot.message_handler(commands=['addresource'])
def add_resource_command(message):
    if message.chat.id in authorized_user_id:
        bot.send_message(message.chat.id, "Введите ресурс для добавления:")
        bot.register_next_step_handler(message, save_resource)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этой команды.")


def save_resource(message):
    resource = message.text.strip()
    if resource:
        with open(file_path, 'a') as file:
            file.write(f"{resource}\n")
        bot.send_message(message.chat.id, f"Ресурс '{resource}' добавлен.")
    else:
        bot.send_message(message.chat.id, "Некорректный ввод. Попробуйте снова.")


@bot.message_handler(commands=['check'])
def check(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, 'Введите сюда ссылку на ресурс для проверки.', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def process_message(message):
    # Проверяем, что сообщение не является командой /start или /check
    if message.text.startswith('/start') or message.text.startswith('/check'):
        return
    # Получаем текущую дату
    current_date = datetime.now().strftime('%d.%m.%Y')

    # Получаем введенную ссылку
    user_input = message.text.lower()

    # Проверяем наличие ссылки в списке ресурсов
    if user_input in get_resource_list():
        bot.send_message(message.chat.id, f'🔴 На дату {current_date}, ресурс {user_input} является экстремистским!')
    else:
        bot.send_message(message.chat.id,
                         f'✅ На дату {current_date}, {user_input} отсутствует в списке экстремистских ресурсов.')


if __name__ == '__main__':
    bot.polling(none_stop=True)
