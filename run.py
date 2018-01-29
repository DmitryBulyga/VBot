# -*- coding: utf-8 -*-

"""
Created on 28.01.18

:author: Dmitry Bulyga

Бот для ВКонтакте

Управление ботом осуществляется из терминала
или из диалога ВКонтакте


"""

from bot_core import BotCore
from dialog_interpreter import DialogInterpreter
from interpreter import Interpreter

class VBot:
    """ Основной класс, синхронизирует ядро бота и интерпретаторы


    """

    def __init__(self):
        self.core = BotCore(self) # ядро бота
        self.dialog_interpreter = DialogInterpreter(self) # интерпретатор команд из диалога ВКонтакте
        self.interpreter = Interpreter(self) # интерпретатор команд терминала

    def start(self):
        self.interpreter.main_loop()


b = VBot()
b.start()
