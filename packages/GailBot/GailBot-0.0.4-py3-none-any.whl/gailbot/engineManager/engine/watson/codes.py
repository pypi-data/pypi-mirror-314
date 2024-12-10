# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-16 11:07:12
# @Last Modified by:   Joanne Fan
# @Last Modified time: 2024-05-16 16:07:46

from enum import IntEnum

class WatsonReturnCodes(IntEnum):
    """
    Return codes from Watson.
    """
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    CONFLICT = 409
    UNSUPPORTED = 415
    SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503
