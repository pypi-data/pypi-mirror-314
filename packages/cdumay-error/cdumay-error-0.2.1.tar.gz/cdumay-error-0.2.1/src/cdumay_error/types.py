#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@ovhcloud.com>

"""
from cdumay_error import Error
from cdumay_error.registry import Registry


@Registry.register
class ConfigurationError(Error):
    """Configuration error"""
    MSGID = "ERR-19036"
    CODE = 400


# noinspection PyShadowingBuiltins
@Registry.register
class IOError(Error):
    """I/O Error"""
    MSGID = "ERR-27582"
    CODE = 500


# noinspection PyShadowingBuiltins
@Registry.register
class NotImplemented(Error):
    """Not Implemented"""
    MSGID = "ERR-04766"
    CODE = 501


@Registry.register
class ValidationError(Error):
    """Validation error"""
    MSGID = "ERR-04413"
    CODE = 400


@Registry.register
class NotFound(Error):
    """Not Found"""
    MSGID = "ERR-08414"
    CODE = 404


@Registry.register
class InternalError(Error):
    """Internal Error"""
    MSGID = "ERR-29885"
    CODE = 500
