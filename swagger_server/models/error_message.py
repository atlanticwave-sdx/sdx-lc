""" class error_message """
# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ErrorMessage(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, error_code: str=None, error_message: str=None):  # noqa: E501
        """ErrorMessage - a model defined in Swagger

        :param error_code: The error_code of this ErrorMessage.  # noqa: E501
        :type error_code: str
        :param error_message: The error_message of this ErrorMessage.  # noqa: E501
        :type error_message: str
        """
        self.swagger_types = {
            'error_code': str,
            'error_message': str
        }

        self.attribute_map = {
            'error_code': 'error_code',
            'error_message': 'error_message'
        }
        self._error_code = error_code
        self._error_message = error_message

    @classmethod
    def from_dict(cls, dikt) -> 'ErrorMessage':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ErrorMessage of this ErrorMessage.  # noqa: E501
        :rtype: ErrorMessage
        """
        return util.deserialize_model(dikt, cls)

    @property
    def error_code(self) -> str:
        """Gets the error_code of this ErrorMessage.


        :return: The error_code of this ErrorMessage.
        :rtype: str
        """
        return self._error_code

    @error_code.setter
    def error_code(self, error_code: str):
        """Sets the error_code of this ErrorMessage.


        :param error_code: The error_code of this ErrorMessage.
        :type error_code: str
        """
        if error_code is None:
            raise ValueError("Invalid value for `error_code`, must not be `None`")  # noqa: E501

        self._error_code = error_code

    @property
    def error_message(self) -> str:
        """Gets the error_message of this ErrorMessage.


        :return: The error_message of this ErrorMessage.
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message: str):
        """Sets the error_message of this ErrorMessage.


        :param error_message: The error_message of this ErrorMessage.
        :type error_message: str
        """
        if error_message is None:
            raise ValueError("Invalid value for `error_message`, must not be `None`")  # noqa: E501

        self._error_message = error_message

