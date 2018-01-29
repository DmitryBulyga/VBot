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
                pass
            elif command[0] == 'remove':
                pass
            elif command[0] == 'dict':
                pass
            elif command[0] == 'set':
                pass
            elif command[0] == 'dial':
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
        admin_id = input("AdminID (put '0' if there's no admin): ")
        try:
            self.parent.core.auth(login, password, admin_id)
            print("Running...")
        except Exception as e:
            print("Authorization failed!")