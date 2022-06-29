import telebot
from functions import *

bot = telebot.TeleBot("2007140752:AAEOtKRl47tG2ZTKC6L7PCvH93oNNwG1mDM")
admin = [1696805458]
respawn = ""

#команды админа и пользователя
@bot.message_handler(commands=['admin'])
def handle_admin_menu(message):
    if message.from_user.id in admin:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

        user_markup.row('/add_restaurant', '/edit_restaurant', '/remove_restaurant')
        user_markup.row('/add_food_type', '/add_food')

        bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=user_markup)
    else:
        bot.send_message(message.from_user.id, 'Ты чужой')

@bot.message_handler(commands=['start'])
def handle_admin_menu(message):
    global respawn

    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "...", reply_markup=hide_markup)

    text = ""
    text = text + "#########################\n"
    text = text + "Добро пожаловать в сервис заказа еды\n"
    text = text + "#########################\n"
    text = text + "Выберите опцию поиска: \n"
    text = text + "1 - Поиск по типу еды\n"
    text = text + "2 - Поиск по ресторану\n"

    respawn = "user menu"
    bot.send_message(message.chat.id, text)



#функции кнопок в меню админа
@bot.message_handler(commands=['add_restaurant'])
def handle_admin_menu(message):
    global respawn
    bot.send_message(message.from_user.id, 'Имя / Адрес')
    respawn = "add_restaurant"

@bot.message_handler(commands=['edit_restaurant'])
def handle_admin_menu(message):
    global respawn

    text = ""
    restaurants = get_all_restaurants()
    for r in restaurants:
        text += str(r[0]) + ") " + r[1] + " " + r[2]
        text += '\n'

    bot.send_message(message.from_user.id, text)
    bot.send_message(message.from_user.id, 'ID / Имя / Аддресс')
    respawn = "edit_restaurant"

@bot.message_handler(commands=['remove_restaurant'])
def handle_admin_menu(message):
    global respawn

    text = ""
    restaurants = get_all_restaurants()
    for r in restaurants:
        text += str(r[0]) + ") " + r[1] + " " + r[2]
        text += '\n'

    bot.send_message(message.from_user.id, text)
    bot.send_message(message.from_user.id, 'Выберите ID')
    respawn = "remove_restaurant"

@bot.message_handler(commands=['add_food_type'])
def handle_admin_menu(message):
    global respawn
    bot.send_message(message.from_user.id, 'Имя')
    respawn = "add_food_type"

@bot.message_handler(commands=['add_food'])
def handle_admin_menu(message):
    global respawn

    text = ""
    food_types = get_all_food_types()
    for f in food_types:
        text += str(f[0]) + ") " + f[1]
        text += '\n'
    bot.send_message(message.from_user.id, "Типы Блюда:")
    bot.send_message(message.from_user.id, text)

    text = ""
    restaurants = get_all_restaurants()
    for r in restaurants:
        text += str(r[0]) + ") " + r[1] + " " + r[2]
        text += '\n'
    bot.send_message(message.from_user.id, "Рестораны:")
    bot.send_message(message.from_user.id, text)

    bot.send_message(message.from_user.id, 'Имя / Цена / Описание / food_type_id / restaurant_id')
    respawn = "add_food"


@bot.message_handler(content_types=['text'])
def handle_text(message):
    global respawn

    if message.text == "my chat id":
        bot.send_message(message.from_user.id, str(message.from_user.id))

    if respawn == "user menu":
        if message.text.lower() == "1":
            food_types = get_all_food_types()
            text = "#####################\n"
            for food in food_types:
                text = text + str(food[0]) + ") " + food[1] + "\n"
            respawn = "choose_by_food_type"
            bot.send_message(message.chat.id, text)
            bot.send_message(message.chat.id, "Выберите тип блюда")

        elif message.text.lower() == "2":
            restaurants = get_all_restaurants()
            text = "#####################\n"
            for rest in restaurants:
                text = text + str(rest[0]) + ") " + rest[1] + " " + rest[2] + "\n"
            respawn = "choose_by_restaurant"
            bot.send_message(message.chat.id, text)
            bot.send_message(message.chat.id, "Выберите ресторан")

    elif respawn == "choose_by_food_type":
        respawn = "choose_food"
        id = message.text.lower()
        foods = get_foods_by_food_type(id)
        text = "#####################\n"
        for food in foods:
            text = text + str(food[0]) + ") " + food[1] + " " + str(food[2]) + " KZT - " + str(food[4]) + "\n"

        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "Выберите номер блюда")

    elif respawn == "choose_by_restaurant":
        respawn = "choose_food"
        id = message.text.lower()
        foods = get_foods_by_restaurant_id(id)
        text = "#####################\n"
        for food in foods:
            text = text + str(food[0]) + ") " + food[1] + " " + str(food[2]) + " KZT - " + food[5] + "\n"

        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "Выберите номер блюда")

    elif respawn == "choose_food":
        id = message.text.lower()
        food = get_food(id)

        text = "Вы заказали " + food[1] + " за " + str(food[2]) + " KZT\n"
        text = text + "Состав: [" + food[3] + "] \n"
        text = text + "К оплате: " + str(food[2]) + " KZT\n"
        text = text + "Спасибо за покупку\n"
        bot.send_message(message.chat.id, text)

    if respawn == "add_restaurant":
        values = message.text
        values = values.split('/')
        values = [v.strip() for v in values]

        if len(values) == 2:
            insert_restaurant(values[0], values[1])
            bot.send_message(message.from_user.id, 'Успешно')
        else:
            bot.send_message(message.from_user.id, 'Введите в правильном формате')

    elif respawn == "edit_restaurant":
        values = message.text
        values = values.split('/')
        values = [v.strip() for v in values]

        if len(values) == 3:
            edit_restaurant(int(values[0]), values[1], values[2])
            bot.send_message(message.from_user.id, 'Успешно')
        else:
            bot.send_message(message.from_user.id, 'Введите в правильном формате')

    elif respawn == "remove_restaurant":
        value = message.text

        if value.isdigit():
            delete_restaurant(value)
            bot.send_message(message.from_user.id, 'Успешно')
        else:
            bot.send_message(message.from_user.id, 'Введите в правильном формате')

    if respawn == "add_food_type":
        insert_food_type(message.text)
        bot.send_message(message.from_user.id, 'Успешно')

    if respawn == "add_food":
        values = message.text
        values = values.split('/')
        values = [v.strip() for v in values]

        if len(values) == 5:
            insert_food(values[0], values[1], values[2], values[3], values[4])
            bot.send_message(message.from_user.id, 'Успешно')
        else:
            bot.send_message(message.from_user.id, 'Введите в правильном формате')

bot.polling(none_stop=True, interval=0)

