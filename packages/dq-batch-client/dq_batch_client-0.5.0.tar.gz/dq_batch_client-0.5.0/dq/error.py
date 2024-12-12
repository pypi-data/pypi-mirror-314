# -*- coding: utf-8 -*-


class DQError(ValueError):

    def __init__(self, status, message):
        super().__init__(status, message)
