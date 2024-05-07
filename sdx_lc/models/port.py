# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from sdx_lc import util
from sdx_lc.models.base_model_ import Model
from sdx_lc.models.service import Service  # noqa: F401,E501


class Port(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(
        self,
        id=None,
        name=None,
        short_name=None,
        node=None,
        label_range=None,
        status=None,
        state=None,
        services=None,
        private_attributes=None,
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
        :param services: The services of this Port.  # noqa: E501
        :type services: Service
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
            "services": Service,
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
            "services": "services",
            "private_attributes": "private_attributes",
        }
        self._id = id
        self._name = name
        self._short_name = short_name
        self._node = node
        self._label_range = label_range
        self._status = status
        self._state = state
        self._services = services
        self._private_attributes = private_attributes

    @classmethod
    def from_dict(cls, dikt):
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The port of this Port.  # noqa: E501
        :rtype: Port
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Port.


        :return: The id of this Port.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Port.


        :param id: The id of this Port.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this Port.


        :return: The name of this Port.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
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
    def short_name(self):
        """Gets the short_name of this Port.


        :return: The short_name of this Port.
        :rtype: str
        """
        return self._short_name

    @short_name.setter
    def short_name(self, short_name):
        """Sets the short_name of this Port.


        :param short_name: The short_name of this Port.
        :type short_name: str
        """

        self._short_name = short_name

    @property
    def node(self):
        """Gets the node of this Port.


        :return: The node of this Port.
        :rtype: str
        """
        return self._node

    @node.setter
    def node(self, node):
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
    def label_range(self):
        """Gets the label_range of this Port.


        :return: The label_range of this Port.
        :rtype: List[str]
        """
        return self._label_range

    @label_range.setter
    def label_range(self, label_range):
        """Sets the label_range of this Port.


        :param label_range: The label_range of this Port.
        :type label_range: List[str]
        """

        self._label_range = label_range

    @property
    def status(self):
        """Gets the status of this Port.


        :return: The status of this Port.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
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
    def state(self):
        """Gets the state of this Port.


        :return: The state of this Port.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Port.


        :param state: The state of this Port.
        :type state: str
        """

        self._state = state

    @property
    def services(self):
        """Gets the services of this Port.


        :return: The services of this Port.
        :rtype: Service
        """
        return self._services

    @services.setter
    def services(self, services):
        """Sets the services of this Port.


        :param services: The services of this Port.
        :type services: Service
        """

        self._services = services

    @property
    def private_attributes(self):
        """Gets the private_attributes of this Port.


        :return: The private_attributes of this Port.
        :rtype: List[str]
        """
        return self._private_attributes

    @private_attributes.setter
    def private_attributes(self, private_attributes):
        """Sets the private_attributes of this Port.


        :param private_attributes: The private_attributes of this Port.
        :type private_attributes: List[str]
        """

        self._private_attributes = private_attributes
