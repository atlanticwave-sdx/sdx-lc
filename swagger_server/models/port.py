# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from swagger_server import util
from swagger_server.models.base_model_ import Model


class Port(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(
        self,
        id: str = None,
        name: str = None,
        short_name: str = None,
        node: str = None,
        label_range: List[str] = None,
        status: str = None,
        state: str = None,
        private_attributes: List[str] = None,
    ):  # noqa: E501
        """Port - a model defined in Swagger

        :param id: The id of this Port.  # noqa: E501
        :type id: str
        :param name: The name of this Port.  # noqa: E501
        :type name: str
        :param short_name: The short_name of this Port.  # noqa: E501
        :type short_name: str
        :param node: The node of this Port.  # noqa: E501
        :type node: str
        :param label_range: The label_range of this Port.  # noqa: E501
        :type label_range: List[str]
        :param status: The status of this Port.  # noqa: E501
        :type status: str
        :param state: The state of this Port.  # noqa: E501
        :type state: str
        :param private_attributes: The private_attributes of this Port.  # noqa: E501
        :type private_attributes: List[str]
        """
        self.swagger_types = {
            "id": str,
            "name": str,
            "short_name": str,
            "node": str,
            "label_range": List[str],
            "status": str,
            "state": str,
            "private_attributes": List[str],
        }

        self.attribute_map = {
            "id": "id",
            "name": "name",
            "short_name": "short_name",
            "node": "node",
            "label_range": "label_range",
            "status": "status",
            "state": "state",
            "private_attributes": "private_attributes",
        }
        self._id = id
        self._name = name
        self._short_name = short_name
        self._node = node
        self._label_range = label_range
        self._status = status
        self._state = state
        self._private_attributes = private_attributes

    @classmethod
    def from_dict(cls, dikt) -> "Port":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The port of this Port.  # noqa: E501
        :rtype: Port
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this Port.


        :return: The id of this Port.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this Port.


        :param id: The id of this Port.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this Port.


        :return: The name of this Port.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Port.


        :param name: The name of this Port.
        :type name: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    @property
    def short_name(self) -> str:
        """Gets the short_name of this Port.


        :return: The short_name of this Port.
        :rtype: str
        """
        return self._short_name

    @short_name.setter
    def short_name(self, short_name: str):
        """Sets the short_name of this Port.


        :param short_name: The short_name of this Port.
        :type short_name: str
        """

        self._short_name = short_name

    @property
    def node(self) -> str:
        """Gets the node of this Port.


        :return: The node of this Port.
        :rtype: str
        """
        return self._node

    @node.setter
    def node(self, node: str):
        """Sets the node of this Port.


        :param node: The node of this Port.
        :type node: str
        """
        if node is None:
            raise ValueError(
                "Invalid value for `node`, must not be `None`"
            )  # noqa: E501

        self._node = node

    @property
    def label_range(self) -> List[str]:
        """Gets the label_range of this Port.


        :return: The label_range of this Port.
        :rtype: List[str]
        """
        return self._label_range

    @label_range.setter
    def label_range(self, label_range: List[str]):
        """Sets the label_range of this Port.


        :param label_range: The label_range of this Port.
        :type label_range: List[str]
        """

        self._label_range = label_range

    @property
    def status(self) -> str:
        """Gets the status of this Port.


        :return: The status of this Port.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this Port.


        :param status: The status of this Port.
        :type status: str
        """
        if status is None:
            raise ValueError(
                "Invalid value for `status`, must not be `None`"
            )  # noqa: E501

        self._status = status

    @property
    def state(self) -> str:
        """Gets the state of this Port.


        :return: The state of this Port.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state: str):
        """Sets the state of this Port.


        :param state: The state of this Port.
        :type state: str
        """

        self._state = state

    @property
    def private_attributes(self) -> List[str]:
        """Gets the private_attributes of this Port.


        :return: The private_attributes of this Port.
        :rtype: List[str]
        """
        return self._private_attributes

    @private_attributes.setter
    def private_attributes(self, private_attributes: List[str]):
        """Sets the private_attributes of this Port.


        :param private_attributes: The private_attributes of this Port.
        :type private_attributes: List[str]
        """

        self._private_attributes = private_attributes
