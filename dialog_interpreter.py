# -*- coding: utf-8 -*-

"""
Created on 28.01.18

:author: Dmitry Bulyga

Интерпретатор команд из диалога ВКонтакте


"""

class DialogInterpreter:

    def __init__(self, bot):
        self.parent = bot

    def handle(self, message):
        print(message)