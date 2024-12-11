#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@corp.ovh.com>


"""
from collections import OrderedDict
from typing import Type, List

from cdumay_error import Error


class Registry(object):
    """Error registry"""
    __errors = OrderedDict()

    @classmethod
    def register(cls, clazz: Type[Error]) -> Type[Error]:
        """Register a new error type

        :param Type[Error] clazz: Error to register
        :return: the error
        :rtype: Type[Error]
        """
        if clazz.MSGID not in cls.__errors:
            cls.__errors[clazz.MSGID] = clazz
        return clazz

    @classmethod
    def filter_by_status(cls, code: int) -> List[Type[Error]]:
        """Filter error by code

        :param int code: Error code 0=Success, Other=Error
        :return: The list of available errors for this code
        :rtype: List[Type[Error]]
        """
        return [x for x in cls.__errors.values() if x.CODE == code]

    @staticmethod
    def error_to_dict(clazz: Type[Error]) -> dict:
        """Serialize an Error Class to dict

        :param Type[Error] clazz: Error to serialize
        :return: The error serialized
        :rtype: dict
        """
        return dict(
            code=clazz.CODE, description=clazz.__doc__, msgid=clazz.MSGID,
            name=clazz.__name__
        )

    @classmethod
    def to_list(cls) -> List[dict]:
        """List all errors

        :return: registered errors
        :rtype: List[dict]
        """
        return [cls.error_to_dict(x) for x in cls.__errors.values()]

    @classmethod
    def to_dict(cls) -> OrderedDict:
        """Return all registered errors

        :return: registered errors
        :rtype: OrderedDict
        """
        return cls.__errors

    @classmethod
    def craft_error(cls, msgid: str, **kwargs) -> Error:
        """Try to initialize error from dict

        :param str msgid: Error UUID
        :param dict kwargs: Any attribute
        :return: the error
        :rtype: Error
        """
        data = dict(msgid=msgid, **kwargs)
        if msgid in cls.__errors.keys():
            return cls.__errors[msgid](**data)
        else:
            return Error(**data)
