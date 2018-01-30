# -*- coding: utf-8 -*-

"""
Created on 28.01.18

:author: Dmitry Bulyga

Ядро бота


"""

import vk_api
import random
import time
import threading


class BotCore:

    def __init__(self, bot):
        self.parent = bot # связь с другими модулями программы
        self.running = False
        self.admin = 0 # id пользователя, который управляет ботом
        self.dictionary = [] # словарный запас бота
        self.ignore = [] # пользователи, забаненные ботом
        self.answers = dict() # ответы бота на определенные сообщения
        self.api = None  # API для ВКонтакте
        self.timeout = 0.1  # время задержки отправки сообщений
        self.name = 'bot' # имя бота
        self.__load_dictionary__()
        self.__load_settings__()

    def auth(self, login, password, admin):
        """ Авторизация во ВКонтакте

        :param login: имя пользователя
        :param password: пароль
        :param admin: id пользователя, который управляет ботом
        :param botname: имя бота

        """

        self.api = vk_api.VkApi(login=login, password=password)
        self.api.auth()
        if admin.isnumeric():
            self.admin = admin
        else:
            self.admin = 0
        lstthread = threading.Thread(target=self.__listen__, name=self.name)
        self.running = True
        lstthread.start() # запуск прослушивания сообщений

    def send(self, user, message):
        """ Отправка сообщения ВКонтакте

        :param user: пользователь, которому отправляется сообщение
        :param message: текст сообщения

        """
        self.api.method('messages.send', {'user_id': user, 'message': message})



    def __listen__(self):
        """ Получение сообщений ВКонтакте
            и вызов функций-обработчиков

        """
        while self.running:
            values = {'out': 0, 'count': 100, 'time_offset': 60}
            response = self.api.method('messages.get', values)
            for item in response['items']:
                if item['read_state'] == 0 and item.get('chat_id') is None:

                    """ Сообщения в групповых чатах
                            не обрабатываются ботом (пока что)
                    """
                    self.api.method('messages.markAsRead', {'peer_id': item['user_id']})
                    if str(item['user_id']) == self.admin:
                        self.parent.dialog_interpreter.handle(item['body'])
                    else:
                        self.handle(item['user_id'], item['body'])
            time.sleep(self.timeout)

    def handle(self, user, message):
        """ Обработка сообщений от обычных пользователей
            По умолчанию бот отправляет произвольную фразу
            из своего словаря (BotCore.dictionary)

        :param user: id пользователя, от которого получено сообщение
        :param message: текст полученного сообщения
        """
        if user in self.ignore:
            return
        answer = '[' + self.name + '] '
        if self.answers.get(message) is not None:
            answer += self.answers[message]
        else:
            n_answer = int(random.uniform(0, len(self.dictionary)))
            answer += self.dictionary[n_answer]
        self.send(user, answer)

    def __load_dictionary__(self):
        """ Загрузка словаря из файла dictionary.dat

        """
        file_dict = open('dictionary.dat', 'r')
        data = file_dict.read()
        self.dictionary.extend(data.split('\n'))
        file_dict.close()
        if '' in self.dictionary:
            self.dictionary.remove('')
        if '\n' in self.dictionary:
            self.dictionary.remove('\n')
        file_dict.close()

    def __save_dictionary__(self):
        file_dict = open("dictionary.dat", "w")
        if len(self.dictionary) != 0:
            file_dict.write('\n'.join(self.dictionary))
        file_dict.close()

    def __load_settings__(self):
        file_settings = open('settings.dat', 'r')
        data = file_settings.read().split('\n')
        for _data in data:
            spl_data = _data.split('|')
            if spl_data[0] == 'ignore':
                self.ignore.extend(map(int, spl_data[1:]))
            if spl_data[0] == 'answers':
                for pair in spl_data[1:]:
                    word, answer = pair.split(':')
                    self.answers.update({word: answer})
        file_settings.close()

    def __save_settings__(self):
        file_settings = open('settings.dat', 'w')
        file_settings.write('ignore|' + '|'.join(map(str, self.ignore)) + '\n')
        ans_str = 'answers'
        for item in list(self.answers.items()):
            ans_str += '|'
            ans_str += item[0]
            ans_str += ':'
            ans_str += item[1]
        file_settings.write(ans_str)
        file_settings.close()

    def add_ignore(self, id):
        self.ignore.append(id)
        self.__save_settings__()

    def add_phrase_in_dict(self, phrase):
        self.dictionary.append(phrase)
        self.__save_dictionary__()

    def add_answer(self, message, answer):
        self.answers.update({message: answer})
        self.__save_settings__()
