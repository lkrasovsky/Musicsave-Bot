# _*_ coding: utf-8 _*
import telebot

import constants
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import pyautogui

bot = telebot.TeleBot(constants.token) # "constants" - a bot token existing file(doesn't exist in this repository). Token can not be shown to anyone for security reasons.

directory = "C:/Users/Семья/Downloads/"


def log(message):
    print("====================")
    from datetime import datetime
    print(datetime.now())
    print("Message from {0} {1}. (id = {2}) \nText: {3}".format(message.from_user.first_name,
                                                                message.from_user.last_name,
                                                                str(message.from_user.id),
                                                                message.text))


def get_music(message):
    name = message.text

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get("https://music.xn--41a.ws/page/4/")
    time.sleep(1)
    pyautogui.click(x=355, y=162)
    driver.find_element_by_name("q").send_keys(name + Keys.RETURN)
    time.sleep(1)

    download = driver.find_element_by_class_name('playlist-btn-down')
    download.click()

    time.sleep(5)

    driver.quit()

    filename = os.listdir(directory)[0]

    old_file = os.path.join(directory, str(filename))
    new_file = os.path.join(directory, str(message.text) + ".mp3")
    os.rename(old_file, new_file)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.from_user.id,
                     'Здравствуйте. Меня зовут Musicsave Bot и я умею скачивать музыку из ВКонтакте.\n\nВот список доступных команд:\n/sign_in - войти в ВК.\n/sign_out - выйти из ВК\n/about - как пользоваться сервисом.\n/developer - разработчик.')


@bot.message_handler(commands=['sign_in'])
def handle_sign_in(message):
    bot.send_message(message.from_user.id,
                     "Введите через пробел ваши логин(телефон или email) и пароль для входа в систему.")


@bot.message_handler(commands=['sign_out'])
def handle_sign_out(message):
    bot.send_message(message.from_user.id, "Вы вышли из системы.")


@bot.message_handler(commands=['about'])
def handle_about(message):
    bot.send_message(message.from_user.id,
                     "И так, в первую очередь вам необходимо войти в ВК для того, чтобы я получил доступ к поиску. Для этого служит команда /sign_in. Просто введите ваш логин(телефон или email) и пароль для входа. Вводить можно в любом формате(через пробел, перенос строки и т.п.).\nПосле входа вам нужно всего лишь отправить название песни, которую вы хотите скачать и подождать около 30 секунд.\nОчень важно, чтобы введённый запрос был корректным.\n\nПримечание: для работы необходимо войти всего один раз. Далее просто вводите названия песен и скачивайте.\n\nЕсли вы желаете выйти из системы, используйте команду /sign_out.\n\nПолучить контакт разработчика можно при помощи команды /developer.")


@bot.message_handler(commands=['developer'])
def handle_developer(message):
    bot.send_message(message.from_user.id, "@lkrasovsky\nМинск, Беларусь\nОтвечаю с 10.00 до 22.00(МСК).")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if "+" in message.text or "@" in message.text:
        log(message)
        time.sleep(3)
        bot.send_message(message.from_user.id, "Вы успешно вощли в систему!\nТеперь введите называние песни, которую хотите скачать.")

    else:
        log(message)

        time.sleep(4)

        get_music(message)

        time.sleep(2)

        filename = os.listdir(directory)[0]

        audio = open(directory + str(filename), 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_audio')
        bot.send_audio(message.from_user.id, audio)
        audio.close()

        for the_file in os.listdir(directory):
            file_path = os.path.join(directory, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)


bot.polling(none_stop=True, interval=0)