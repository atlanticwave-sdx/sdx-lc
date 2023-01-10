# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from swagger_server import util
from swagger_server.models.base_model_ import Model
from swagger_server.models.port import Port  # noqa: F401,E501


class Connection(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(
        self,
        id: str = None,
        name: str = None,
        ingress_port: Port = None,
        egress_port: Port = None,
        quantity: int = None,
        start_time: datetime = None,
        end_time: datetime = None,
        status: str = None,
        complete: bool = False,
    ):  # noqa: E501
        """Connection - a model defined in Swagger

        :param id: The id of this Connection.  # noqa: E501
        :type id: str
        :param name: The name of this Connection.  # noqa: E501
        :type name: str
        :param ingress_port: The ingress_port of this Connection.  # noqa: E501
        :type ingress_port: Port
        :param egress_port: The egress_port of this Connection.  # noqa: E501
        :type egress_port: Port
        :param quantity: The quantity of this Connection.  # noqa: E501
        :type quantity: int
        :param start_time: The start_time of this Connection.  # noqa: E501
        :type start_time: datetime
        :param end_time: The end_time of this Connection.  # noqa: E501
        :type end_time: datetime
        :param status: The status of this Connection.  # noqa: E501
        :type status: str
        :param complete: The complete of this Connection.  # noqa: E501
        :type complete: bool
        """
        self.swagger_types = {
            "id": str,
            "name": str,
            "ingress_port": Port,
            "egress_port": Port,
            "quantity": int,
            "start_time": datetime,
            "end_time": datetime,
            "status": str,
            "complete": bool,
        }

        self.attribute_map = {
            "id": "id",
            "name": "name",
            "ingress_port": "ingress_port",
            "egress_port": "egress_port",
            "quantity": "quantity",
            "start_time": "start_time",
            "end_time": "end_time",
            "status": "status",
            "complete": "complete",
        }
        self._id = id
        self._name = name
        self._ingress_port = ingress_port
        self._egress_port = egress_port
        self._quantity = quantity
        self._start_time = start_time
        self._end_time = end_time
        self._status = status
        self._complete = complete

    @classmethod
    def from_dict(cls, dikt) -> "Connection":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The connection of this Connection.  # noqa: E501
        :rtype: Connection
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this Connection.


        :return: The id of this Connection.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this Connection.


        :param id: The id of this Connection.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this Connection.


        :return: The name of this Connection.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Connection.


        :param name: The name of this Connection.
        :type name: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    @property
    def ingress_port(self) -> Port:
        """Gets the ingress_port of this Connection.


        :return: The ingress_port of this Connection.
        :rtype: Port
        """
        return self._ingress_port

    @ingress_port.setter
    def ingress_port(self, ingress_port: Port):
        """Sets the ingress_port of this Connection.


        :param ingress_port: The ingress_port of this Connection.
        :type ingress_port: Port
        """
        if ingress_port is None:
            raise ValueError(
                "Invalid value for `ingress_port`, must not be `None`"
            )  # noqa: E501

        self._ingress_port = ingress_port

    @property
    def egress_port(self) -> Port:
        """Gets the egress_port of this Connection.


        :return: The egress_port of this Connection.
        :rtype: Port
        """
        return self._egress_port

    @egress_port.setter
    def egress_port(self, egress_port: Port):
        """Sets the egress_port of this Connection.


        :param egress_port: The egress_port of this Connection.
        :type egress_port: Port
        """
        if egress_port is None:
            raise ValueError(
                "Invalid value for `egress_port`, must not be `None`"
            )  # noqa: E501

        self._egress_port = egress_port

    @property
    def quantity(self) -> int:
        """Gets the quantity of this Connection.


        :return: The quantity of this Connection.
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        """Sets the quantity of this Connection.


        :param quantity: The quantity of this Connection.
        :type quantity: int
        """

        self._quantity = quantity

    @property
    def start_time(self) -> datetime:
        """Gets the start_time of this Connection.


        :return: The start_time of this Connection.
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: datetime):
        """Sets the start_time of this Connection.


        :param start_time: The start_time of this Connection.
        :type start_time: datetime
        """

        self._start_time = start_time

    @property
    def end_time(self) -> datetime:
        """Gets the end_time of this Connection.


        :return: The end_time of this Connection.
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: datetime):
        """Sets the end_time of this Connection.


        :param end_time: The end_time of this Connection.
        :type end_time: datetime
        """

        self._end_time = end_time

    @property
    def status(self) -> str:
        """Gets the status of this Connection.

        Connection Status  # noqa: E501

        :return: The status of this Connection.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this Connection.

        Connection Status  # noqa: E501

        :param status: The status of this Connection.
        :type status: str
        """
        allowed_values = ["success", "fail", "scheduled", "provisioining"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}".format(
                    status, allowed_values
                )
            )

        self._status = status

    @property
    def complete(self) -> bool:
        """Gets the complete of this Connection.


        :return: The complete of this Connection.
        :rtype: bool
        """
        return self._complete

    @complete.setter
    def complete(self, complete: bool):
        """Sets the complete of this Connection.


        :param complete: The complete of this Connection.
        :type complete: bool
        """

        self._complete = complete
