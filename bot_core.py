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
        self.admin_mode = True
        self.admin = 0 # id пользователя, который управляет ботом
        self.dictionary = [] # словарный запас бота
        self.ignore = [] # пользователи, забаненные ботом
        self.answers = dict() # ответы бота на определенные сообщения
        self.api = None  # API для ВКонтакте
        self.timeout = 0.1  # время задержки отправки сообщений
        self.name = 'bot' # имя бота
        self.__load_dictionary__()
        self.__load_settings__()

    def auth(self, login, password):
        """ Авторизация во ВКонтакте

        :param login: имя пользователя
        :param password: пароль
        :param admin: id пользователя, который управляет ботом
        :param botname: имя бота

        """
        try:
            self.api = vk_api.VkApi(login=login, password=password)
            self.api.auth()
        except Exception as e:
            return 1
        return 0


    def start(self):
        if self.api is None:
            return 2
        try:
            lstthread = threading.Thread(target=self.__listen__, name=self.name)
            self.running = True
            lstthread.start()  # запуск прослушивания сообщений
        except Exception as e:
            return 1
        return 0

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
                    if int(item['user_id']) == int(self.admin):
                        self.handle_admin(item['body'])
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

    def handle_admin(self, message):
        if 'auth' in message or 'exit' in message:
            return
        if not self.admin_mode and 'adminmode' not in message:
            self.handle(self.admin, message)
            return
        answer = self.parent.interpreter.interpret(message)
        if 'setadmin' not in message:
            self.send(self.admin, answer)

    def __load_dictionary__(self):
        """ Загрузка словаря из файла dictionary.dat

        """
        with open('dictionary.dat', 'r') as file_dict:
            data = file_dict.read()
            self.dictionary.extend(data.split('\n'))
            file_dict.close()
            if '' in self.dictionary:
                self.dictionary.remove('')
            if '\n' in self.dictionary:
                self.dictionary.remove('\n')


    def __save_dictionary__(self):
        with open("dictionary.dat", "w") as file_dict:
            if len(self.dictionary) != 0:
                file_dict.write('\n'.join(self.dictionary))

    def __load_settings__(self):
        with open('settings.dat', 'r') as file_settings:
            data = file_settings.read().splitlines()
            for d in data:
                spl_data = d.split('|')
                if spl_data[0] == 'ignore':
                    self.ignore.extend(map(int, spl_data[1:]))
                elif spl_data[0] == 'answers':
                    for pair in spl_data[1:]:
                        word, answer = pair.split(':')
                        self.answers.update({word: answer})
                elif spl_data[0] == 'admin':
                    if spl_data[1].isnumeric():
                        self.admin = int(spl_data[1])
                elif spl_data[0] == 'name':
                    self.name = spl_data[1]
                elif spl_data[0] == 'timeout':
                    self.timeout = float(spl_data[1])

    def __save_settings__(self):
        with open('settings.dat', 'w') as file_settings:
            file_settings.write('ignore|' + '|'.join(map(str, self.ignore)) + '\n')
            ans_str = 'answers'
            for item in list(self.answers.items()):
                ans_str += '|'
                ans_str += item[0]
                ans_str += ':'
                ans_str += item[1]
            file_settings.write(ans_str + '\n')
            file_settings.write('admin|' + str(self.admin) + '\n')
            file_settings.write('name|' + self.name + '\n')
            file_settings.write('timeout|' + str(self.timeout) + '\n')

    def add_ignore(self, id):
        try:
            self.ignore.append(id)
            self.__save_settings__()
        except Exception as e:
            return 1
        return 0

    def remove_ignore(self, index):
        if index >= len(self.ignore):
            return 2
        try:
            self.parent.core.ignore.pop(index)
            self.__save_settings__()
        except Exception as e:
            return 1
        return 0

    def get_ignore(self):
        if len(self.ignore) == 0:
            return 'No ignored users'
        counter = 0
        answer = ''
        for user in self.ignore:
            answer += str(counter) + '. https://vk.com/id' + str(user) + '\n'
            counter += 1
        return answer

    def add_phrase_in_dict(self, phrase):
        try:
            self.dictionary.append(phrase)
            self.__save_dictionary__()
        except Exception as e:
            return 1
        return 0

    def remove_phrase_from_dict(self, index):
        if index >= len(self.dictionary):
            return 2
        try:
            self.dictionary.pop(index)
            self.__save_dictionary__()
        except Exception as e:
            return 1
        return 0

    def get_dict(self):
        if len(self.dictionary) == 0:
            return 'The dictionary is empty!'
        counter = 0
        answer = ''
        for phrase in self.dictionary:
            answer += str(counter) + '. ' + phrase + '\n'
            counter += 1
        return answer

    def add_answer(self, message, answer):
        try:
            self.answers.update({message: answer})
            self.__save_settings__()
        except Exception as e:
            return 1
        return 0

    def remove_answer(self, message):
        if self.answers.get(message) is None:
            return 2
        try:
            self.answers.pop(message)
            self.__save_settings__()
        except Exception as e:
            return 1
        return 0

    def get_answers(self):
        if len(self.parent.core.answers) == 0:
            return 'No answers!'
        answer = ''
        for item in list(self.parent.core.answers.items()):
            answer += item[0] + ':' + item[1] + '\n'
        return answer

    def set_admin(self, id):
        try:
            if id.isnumeric():
                self.parent.core.admin = id
                self.__save_settings__()
                return 0
            else:
                return 2
        except Exception as e:
            return 1

    def set_name(self, name):
        try:
            self.name = name
            self.__save_settings__()
            return 0
        except Exception as e:
            return 1

    def set_timeout(self, timeout):
        try:
            self.parent.core.timeout = float(timeout)
            self.__save_settings__()
            return 0
        except Exception as e:
            return 1