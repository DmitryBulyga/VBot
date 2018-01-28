# -*- coding: utf-8 -*-

"""
Created on 28.01.18

:author: Dmitry Bulyga

Бот для ВКонтакте

Управление ботом осуществдяется из командной строки
или из диалога ВКонтакте


"""

from bot_core import BotCore
from dialog_interpreter import DialogInterpreter

class VBot:
    """ Основной класс, синхронизирует ядро бота и интерпретаторы


    """

    def __init__(self):
        self.core = BotCore(self) # ядро бота
        self.dialog_interpreter = DialogInterpreter() # интерпретатор команд из диалога ВКонтакте



b = VBot()
b.core.auth(' ', ' ', ' ')
