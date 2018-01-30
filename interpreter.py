# -*- coding: utf-8 -*-

import getpass


class Interpreter:

    def __init__(self, bot):
        self.parent = bot

    def main_loop(self):
        while True:
            com_str = input()
            command = com_str.split(' ')
            if command[0] == 'auth':
                self.__auth__()
            elif command[0] == 'ignore':
                self.__ignore__(command)
            elif command[0] == 'dict':
                self.__dict__(command)
            elif command[0] == 'answers':
                self.__answers__(command)
            elif command[0] == 'admin':
                self.__admin__(command)
            elif command[0] == 'set':
                pass
            elif command[0] == 'exit':
                self.parent.core.running = False
                break
            elif command[0] == 'stop':
                if self.parent.core.running:
                    self.parent.core.running = False
                    print('Stopped!')
                else:
                    print("Bot is not running!")

    def __auth__(self):
        login = input("Login: ")
        password = getpass.getpass("Password: ")
        admin_id = input("AdminID (enter '0' if there's no admin): ")
        try:
            self.parent.core.auth(login, password, admin_id)
            print("Running...")
        except Exception as e:
            print("Authorization failed!")

    def __dict__(self, command):
        if len(command) < 3:
            print('Incorrect command!')
            return
        if command[1] == 'add':
            phrase = ' '.join(command[2:])
            self.parent.core.add_phrase_in_dict(phrase)
        else:
            return
        print('Done!')

    def __ignore__(self, command):
        if command[1] == 'add':
            if len(command) < 3:
                print('Incorrect command!')
                return
            if not command[2].isnumeric():
                print('Wrong user ID!')
                return
            self.parent.core.add_ignore(command[2])
        elif command[1] == 'remove':
            if len(command) < 3:
                print('Incorrect command!')
                return
            if not command[2].isnumeric() or int(command[2]) >= len(self.parent.core.ignore):
                print('Wrong index!')
                return
            index = int(command[2])
            self.parent.core.ignore.pop(index)
        elif command[1] == 'show':
            if len(self.parent.core.ignore) == 0:
                print('No ignored users')
            for user in self.parent.core.ignore:
                print('https://vk.com/id' + str(user) + '\n')
            return
        else:
            return
        print('Done!')

    def __answers__(self, command):
        if len(command) != 2:
            print('Incorrect command!')
            return
        if command[1] == 'add':
            message = input("Message: ")
            answer = input("Bot's answer: ")
            self.parent.core.add_answer(message, answer)
        elif command[1] == 'show':
            for item in list(self.parent.core.answers.items()):
                print(item[0] + ':' + item[1] + '\n')
                return
        else:
            return
        print('Done!')

    def __admin__(self, command):
        if len(command) < 2:
            print('Incorrect command!')
            return
        elif command[1] == 'show':
            if self.parent.core.admin == 0:
                print('No admin!')
                return
            print(self.parent.core.admin)


