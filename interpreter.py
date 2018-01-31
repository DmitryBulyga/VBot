# -*- coding: utf-8 -*-

import getpass


class Interpreter:

    def __init__(self, bot):
        self.parent = bot

    def main_loop(self):
        while True:
            com_str = input()
            answer = self.interpret(com_str)
            if answer is None:
                return
            else:
                print(answer)

    def interpret(self, com_str):

        command = com_str.split(' ')

        if command[0] == 'auth':
            return self.__auth__()

        if command[0] == 'start':
            return self.__start__()

        if command[0] == 'ignore':
            if len(command) == 3:
                if command[1] == 'add':
                    return self.__ignore_add__(command[2])
                elif command[1] == 'remove':
                    return self.__ignore_remove__(command[2])
            elif len(command) == 2:
                if command[1] == 'show':
                    return self.__ignore_show__()
            else:
                return 'Incorrect command!'

        if command[0] == 'dict':
            if command[1] == 'add' and len(command) >= 3:
                return self.__dict_add__(command[2:])
            elif command[1] == 'remove' and len(command) == 3:
                return self.__dict_remove__(command[2])
            elif command[1] == 'show' and len(command) == 2:
                return self.__dict_show__()
            else:
                return 'Incorrect command!'

        if command[0] == 'answers':
            if len(command) >= 3 and command[1] == 'add':
                return self.__answers_add__(command[2:])
            elif len(command) >= 3 and command[1] == 'remove':
                return self.__answers_remove__(command[2:])
            elif len(command) == 2 and command[1] == 'show':
                return self.__answers_show__()
            else:
                return 'Incorrect command!'

        if command[0] == 'setadmin':
            if len(command) == 2:
                return self.__setadmin__(command[1])
            else:
                return 'Incorrect command!'

        if command[0] == 'usermode':
            self.parent.core.admin_mode = False
            return 'User mode is enabled.'

        if command[0] == 'adminmode':
            self.parent.core.admin_mode = True
            return 'Admin mode is enabled.'

        if command[0] == 'setname':
            if len(command) == 2:
                return self.__setname__(command[1])
            else:
                return 'Incorrect command!'

        if command[0] == 'settimeout':
            if len(command) == 2:
                return self.__settimeout__(command[1])
            else:
                return 'Incorrect command!'

        if command[0] == 'exit':
            self.parent.core.running = False
            return None

        if command[0] == 'stop':
            if self.parent.core.running:
                self.parent.core.running = False
                return 'Stopped!'
            else:
                return 'Bot is not running!'

        return 'Wrong command!'

    def __auth__(self):
        if self.parent.core.running:
            return 'Bot is already running!'
        login = input('Login: ')
        password = getpass.getpass('Password: ')
        res = self.parent.core.auth(login, password)
        if res == 0:
            return 'Authorized! Use "start" to run the bot.'
        else:
            return 'Authorization failed!'

    def __start__(self):
        res = self.parent.core.start()
        if res == 0:
            return 'Running!'
        elif res == 2:
            return 'Authorization required! Use "auth".'
        else:
            return 'Unknown error!'

    def __ignore_add__(self, user):
        if not user.isnumeric():
            return 'Wrong user ID!'
        res = self.parent.core.add_ignore(user)
        if res == 0:
            return 'Done!'
        else:
            return 'Unknown error'

    def __ignore_remove__(self, index):
        if not index.isnumeric():
            return 'Wrong index!'
        res = self.parent.core.remove_ignore(int(index))
        if res == 0:
            return 'Done!'
        elif res == 2:
            return 'Wrong index!'
        else:
            return 'Unknown error'

    def __ignore_show__(self):
        return self.parent.core.get_ignore()

    def __dict_add__(self, phrase):
        phrase = ' '.join(phrase)
        res = self.parent.core.add_phrase_in_dict(phrase)
        if res == 0:
            return 'Done!'
        else:
            return 'Unknown error!'

    def __dict_remove__(self, index):
        if not index.isnumeric():
            return 'Wrong index!'
        res = self.parent.core.remove_phrase_from_dict(int(index))
        if res == 0:
            return 'Done!'
        elif res == 2:
            return 'Wrong index!'
        else:
            return 'Unknown error!'

    def __dict_show__(self):
        return self.parent.core.get_dict()

    def __answers_add__(self, string):
        string = ' '.join(string)
        if '|' in string:
            message, answer = string.split('|')
            res = self.parent.core.add_answer(message, answer)
            if res == 0:
                return 'Done!'
            else:
                return 'Unknown error!'
        else:
            return 'Symbol "|" wasn\'t found'

    def __answers_remove__(self, message):
        message = ' '.join(message)
        res = self.parent.core.remove_answer(message)
        if res == 0:
            return 'Done!'
        elif res == 2:
            return 'Answer was\'nt found'
        else:
            return 'Unknown error!'

    def __answers_show__(self):
        return self.parent.core.get_answers()

    def __setadmin__(self, id):
        res = self.parent.core.set_admin(id)
        if res == 0:
            return 'Done!'
        elif res == 2:
            return 'Incorrect admin ID!'
        else:
            return 'Unknown error!'

    def __setname__(self, name):
        res = self.parent.core.set_name(name)
        if res == 0:
            return 'Done!'
        else:
            return 'Unknown error!'

    def __settimeout__(self, timeout):
        res = self.parent.core.set_timeout(timeout)
        if res == 0:
            return 'Done!'
        else:
            return 'Unknown error!'

