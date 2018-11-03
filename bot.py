#!/usr/bin/env python
import os

import telebot

TOKEN = '656772247:AAHWY4qsBhTHsT8jnH6ss63JErwS4a-Dmrc'

bot = telebot.TeleBot(TOKEN)

print(bot.get_me())


def log(message, answer):
    print('\n')
    from datetime import datetime
    print(datetime.now())
    print('Сообщение от {0} {1} , (id = {2}) \n Текст - {3}'.format(message.from_user.first_name,
                                                                    message.from_user.last_name,
                                                                    str(message.from_user.id),
                                                                    message.text))
    print(answer)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Наши контакты')
    user_markup.row('Оставить заявку на поставку продукции')
    answer = 'Добро пожаловать дорогой пользователь моего бота !'
    log(message, answer)
    bot.send_message(message.from_user.id, answer, reply_markup=user_markup)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    answer = 'Бот создан новичком в этой сфере, не судите строго'
    log(message, answer)
    bot.reply_to(message, answer)


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    if message.text == 'Наши контакты':
        bot.send_message(message.from_user.id, 'Наши контакты'
                                               '\nНомер телефона : +998 903211309'
                                               '\nНаш канал : @mqtextile')
    elif message.text == 'Оставить заявку на поставку продукции':
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = telebot.types.KeyboardButton(text='Отправить номер телефона', request_contact=True)
        button_hub = telebot.types.KeyboardButton(text='Назад')
        keyboard.add(button_phone, button_hub)
        bot.send_message(message.from_user.id, 'Для того чтобы оставить заявку на поставку продукции ,'
                                               '\nвы должны отправить нам ваш номер телефона,'
                                               '\nпо нажатию кнопки на клавиатуре'
                                               '\nдля того чтобы мы могли вам перезвонить'
                                               '\nЗатем вы должны написать вашу заявку'
                                               '\nв Microsoft Word и отправить нам .'
                                               '\nСнизу я вам отправил пример заявки .', reply_markup=keyboard)
        doc = open('Пример заявки.docx', 'rb')
        bot.send_document(message.from_user.id, doc)

    elif message.text == 'Назад':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Наши контакты')
        user_markup.row('Оставить заявку на поставку продукции')
        answer = 'Добро пожаловать дорогой пользователь моего бота !'
        log(message, answer)
        bot.send_message(message.from_user.id, answer, reply_markup=user_markup)
    else:
        bot.send_message(message.from_user.id, 'MqTextile:'
                                               '\nЯ вас не понимаю .')


@bot.message_handler(content_types=['contact'])
def user_contact(message):
    answer = 'Заявка от :{0} ,\nНомер телефона : {1}'.format(message.from_user.first_name,
                                                             message.contact.phone_number)
    bot.send_message(35633610, answer)


@bot.message_handler(content_types=['photo'])
def echo_msg(message):
    if message.content_type == 'photo':
        raw = message.photo[2].file_id
        name = raw + ".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(name, 'wb') as new_file:
            new_file.write(downloaded_file)
        img = open(name, 'rb')
        bot.send_message(35633610,
                         "Запрос от\n*{name} , отправил фотографию *".format(name=message.chat.first_name),
                         parse_mode="Markdown")
        bot.send_photo(35633610, img)
        bot.send_message(message.chat.id,
                         "*{name}!*\nСпасибо за инфу".format(name=message.chat.first_name,
                                                             text=message.text),
                         parse_mode="Markdown")
        img.close()
        os.remove(str(img.name))


@bot.message_handler(content_types=['document'])
def handle_text_doc(message):
    if message.content_type == 'document':
        raw = message.document.file_id
        name = raw + ".docx"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(name, 'wb') as new_file:
            new_file.write(downloaded_file)
        doc = open(name, 'rb')
        bot.send_message(35633610,
                         "Запрос от\n*{name} , отправил файл заявку *".format(name=message.chat.first_name),
                         parse_mode="Markdown")
        bot.send_document(35633610, doc)
        bot.send_message(message.chat.id,
                         "*{name}!*\nСпасибо за инфу".format(name=message.chat.first_name,
                                                             text=message.text),
                         parse_mode="Markdown")
        doc.close()
        os.remove(str(doc.name))


bot.polling(none_stop=True)