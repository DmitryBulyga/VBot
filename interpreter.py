# -*- coding: utf-8 -*-

import getpass


class Interpreter:

    def __init__(self, bot):
        self.parent = bot

    def main_loop(self):
        working = True
        while working:
            com_str = input()
            working = self.interpret(com_str)

    def interpret(self, com_str):
        command = com_str.split(' ')
        if command[0] == 'auth':
            self.__auth__()
        elif command[0] == 'ignore':
            if len(command) == 3:
                if command[1] == 'add':
                    self.__ignore_add__(command[2])
                elif command[1] == 'remove':
                    self.__ignore_remove__(command[2])
            elif len(command) == 2:
                if command[1] == 'show':
                    self.__ignore_show__()
            else:
                print('Incorrect command!')

        elif command[0] == 'dict':
            if command[1] == 'add' and len(command) >= 3:
                self.__dict_add__(command[2:])
            elif command[1] == 'remove' and len(command) == 3:
                self.__dict_remove__(command[2])
            elif command[1] == 'show' and len(command) == 2:
                self.__dict_show__()
            else:
                print('Incorrect command!')

        elif command[0] == 'answers':
            if len(command) >= 3 and command[1] == 'add':
                self.__answers_add__(command[2:])
            elif len(command) >= 3 and command[1] == 'remove':
                self.__answers_remove__(command[2:])
            elif len(command) == 2 and command[1] == 'show':
                self.__answers_show__()
            else:
                print('Incorrect command!')

        elif command[0] == 'setadmin':
            if len(command) == 2:
                self.__setadmin__(command[1])
            else:
                print('Incorrect command!')

        elif command[0] == 'setname':
            if len(command) == 2:
                self.__setname__(command[1])
            else:
                print('Incorrect command!')

        elif command[0] == 'settimeout':
            if len(command) == 2:
                self.__settimeout__(command[1])
            else:
                print('Incorrect command!')

        elif command[0] == 'exit':
            self.parent.core.running = False
            return False
        elif command[0] == 'stop':
            if self.parent.core.running:
                self.parent.core.running = False
                print('Stopped!')
            else:
                print("Bot is not running!")
        return True

    def __auth__(self):
        if self.parent.core.running:
            print('Bot is already running!')
            return
        login = input("Login: ")
        password = getpass.getpass("Password: ")
        admin_id = input("AdminID (enter '0' if there's no admin): ")
        try:
            self.parent.core.auth(login, password, admin_id)
            print("Running...")
        except Exception as e:
            print("Authorization failed!")

    def __ignore_add__(self, user):
        if not user.isnumeric():
            print('Wrong user ID!')
            return
        res = self.parent.core.add_ignore(user)
        if res == 0:
            print('Done!')
        else:
            print('Unknown error')

    def __ignore_remove__(self, index):
        if not index.isnumeric():
            print('Wrong index!')
            return
        res = self.parent.core.remove_ignore(int(index))
        if res == 0:
            print('Done!')
        elif res == 2:
            print('Wrong index!')
        else:
            print('Unknown error')

    def __ignore_show__(self):
        res = self.parent.core.get_ignore()
        print(res)

    def __dict_add__(self, phrase):
        phrase = ' '.join(phrase)
        res = self.parent.core.add_phrase_in_dict(phrase)
        if res == 0:
            print('Done!')
        else:
            print('Unknown error!')

    def __dict_remove__(self, index):
        if not index.isnumeric():
            print('Wrong index!')
            return
        res = self.parent.core.remove_phrase_from_dict(int(index))
        if res == 0:
            print('Done!')
        elif res == 2:
            print('Wrong index!')
        else:
            print('Unknown error!')

    def __dict_show__(self):
        res = self.parent.core.get_dict()
        print(res)

    def __answers_add__(self, string):
        string = ' '.join(string)
        if '|' in string:
            message, answer = string.split('|')
            res = self.parent.core.add_answer(message, answer)
            if res == 0:
                print('Done!')
            else:
                print('Unknown error!')
        else:
            print('Symbol "|" wasn\'t found')

    def __answers_remove__(self, message):
        message = ' '.join(message)
        res = self.parent.core.remove_answer(message)
        if res == 0:
            print('Done!')
        elif res == 2:
            print('Answer was\'nt found')
        else:
            print('Unknown error!')

    def __answers_show__(self):
        res = self.parent.core.get_answers()
        print(res)

    def __setadmin__(self, id):
        pass

    def __setname__(self, name):
        pass

    def __settimeout__(self, timeout):
        pass

