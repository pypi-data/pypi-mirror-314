# -*- coding: utf-8 -*-

import json

from .error import DQError


class Response:

    def __init__(self, method, status, content):

        self.method = method
        self.status = status
        self.content = content

    def is_ok(self):
        return self.status and int(self.status) < 400

    def json(self):
        return self.result

    def object(self):
        return json.loads(self.content)

    def __repr__(self):
        return "%s %s" % (self.status, self.content)


class from_response():

    def __init__(self, clazz=None):
        self.clazz = clazz

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            if response.status == 404:
                return None
            if not response.is_ok():
                raise DQError(status=response.status, message=response.content)
            obj = response.object()
            if isinstance(obj, list):
                return [self.__to_object(item) for item in obj]
            return self.__to_object(obj)
        return wrapper

    def __to_object(self, obj):
        if self.clazz is None:
            return obj
        return self.clazz(**obj)
