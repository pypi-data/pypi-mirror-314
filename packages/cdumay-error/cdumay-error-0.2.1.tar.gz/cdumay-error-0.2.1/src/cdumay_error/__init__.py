#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import sys
import traceback
from typing import Optional, Any

from marshmallow import Schema, fields, EXCLUDE
from marshmallow import ValidationError as MarshmallowValidationError
from marshmallow.fields import Mapping


class Error(Exception):
    """Mother class for all errors"""
    MSGID = "Err-00000"
    CODE = 1
    MESSAGE = None

    def __init__(self,
                 message: Optional[str] = None,
                 extra: Optional[dict] = None,
                 msgid: Optional[str] = None,
                 stack: Optional[str] = None,
                 name: Optional[str] = None,
                 code: Optional[int] = None,
                 **kwargs):
        self.message = message or self.MESSAGE or self.__doc__
        Exception.__init__(self, code, self.message)
        self.code = code or self.CODE
        self.extra = extra or kwargs
        self.stack = stack
        self.msgid = msgid or self.MSGID
        self.name = name or self.__class__.__name__

        if self.stack is None:
            exc_t, exc_v, exc_tb = sys.exc_info()
            if exc_t and exc_v and exc_tb:
                self.stack = "\n".join([
                    x.rstrip() for x in traceback.format_exception(
                        exc_t, exc_v, exc_tb
                    )
                ])

    def to_json(self) -> str:
        """Serialize to JSON

        :return: Error into JSON representation
        :rtype: str
        """
        return ErrorSchema().dumps(self)

    def to_dict(self) -> dict:
        """Serialize as Dict

        :return: Error dumped into a dict
        :rtype: dict
        """
        return ErrorSchema().dump(self)

    @classmethod
    def from_json(cls, data: Mapping) -> "Error":
        """Deserialize from JSON

        :param Mapping data: JSON representation
        :return: The error
        :rtype: Error
        """
        return ErrorSchema().load(data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<code={self.code}," \
               f" msgid={self.msgid}, message={self.message}>"

    def __str__(self) -> str:
        return f"{self.msgid}: {self.message}"


class ErrorSchema(Schema):
    """Error Serializer"""

    class Meta:
        """Marshamllow field management"""
        unknown = EXCLUDE

    code = fields.Integer()
    name = fields.String()
    message = fields.String()
    msgid = fields.String()
    extra = fields.Dict()
    stack = fields.String(allow_none=True)

    @staticmethod
    def class_name(data: Error) -> str:
        """Return error name

        :param Error data: Error to name
        :return: Error name
        :rtype: str
        """
        return data.__class__.__name__


def from_exc(exc: Exception, extra: Optional[dict] = None) -> Any:
    """ Try to convert exception into an JSOn serializable

    :param Exception exc: exception
    :param Optional[dict] extra: extra data
    :return: an Error
    :rtype: Any Error
    """
    if isinstance(exc, Error):
        return exc

    if isinstance(exc, MarshmallowValidationError):
        from cdumay_error.types import ValidationError
        return ValidationError(
            "Invalid field(s) value: {}".format(
                ", ".join(exc.normalized_messages().keys())
            ), extra=exc.normalized_messages()
        )

    from cdumay_error.types import InternalError
    return InternalError(message=str(exc), extra=extra)
