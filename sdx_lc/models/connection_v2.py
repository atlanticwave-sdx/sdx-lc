# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from sdx_lc import util
from sdx_lc.models.base_model_ import Model
from sdx_lc.models.connection_qos_metrics import ConnectionQosMetrics  # noqa: F401,E501
from sdx_lc.models.connection_scheduling import ConnectionScheduling  # noqa: F401,E501
from sdx_lc.models.link import Link  # noqa: F401,E501
from sdx_lc.models.port import Port  # noqa: F401,E501


class ConnectionV2(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(
        self,
        id=None,
        name=None,
        endpoints=None,
        description=None,
        notifications=None,
        scheduling=None,
        qos_metrics=None,
        paths=None,
        status=None,
        complete=False,
        quantity=None,
        multi_path=None,
        preempt=None,
        backup_path_type=None,
        exclusive_links=None,
        inclusive_links=None,
    ):  # noqa: E501
        """ConnectionV2 - a model defined in Swagger

        :param id: The id of this ConnectionV2.  # noqa: E501
        :type id: str
        :param name: The name of this ConnectionV2.  # noqa: E501
        :type name: str
        :param endpoints: The endpoints of this ConnectionV2.  # noqa: E501
        :type endpoints: List[Port]
        :param description: The description of this ConnectionV2.  # noqa: E501
        :type description: str
        :param notifications: The notifications of this ConnectionV2.  # noqa: E501
        :type notifications: List[Dict[str, object]]
        :param scheduling: The scheduling of this ConnectionV2.  # noqa: E501
        :type scheduling: ConnectionScheduling
        :param qos_metrics: The qos_metrics of this ConnectionV2.  # noqa: E501
        :type qos_metrics: Dict[str, ConnectionQosMetrics]
        :param paths: The paths of this ConnectionV2.  # noqa: E501
        :type paths: List[str]
        :param status: The status of this ConnectionV2.  # noqa: E501
        :type status: str
        :param complete: The complete of this ConnectionV2.  # noqa: E501
        :type complete: bool
        :param quantity: The quantity of this ConnectionV2.  # noqa: E501
        :type quantity: int
        :param multi_path: The multi_path of this ConnectionV2.  # noqa: E501
        :type multi_path: bool
        :param preempt: The preempt of this ConnectionV2.  # noqa: E501
        :type preempt: bool
        :param backup_path_type: The backup_path_type of this ConnectionV2.  # noqa: E501
        :type backup_path_type: str
        :param exclusive_links: The exclusive_links of this ConnectionV2.  # noqa: E501
        :type exclusive_links: List[Link]
        :param inclusive_links: The inclusive_links of this ConnectionV2.  # noqa: E501
        :type inclusive_links: List[Link]
        """
        self.swagger_types = {
            "id": str,
            "name": str,
            "endpoints": List[Port],
            "description": str,
            "notifications": List[Dict[str, object]],
            "scheduling": ConnectionScheduling,
            "qos_metrics": Dict[str, ConnectionQosMetrics],
            "paths": List[str],
            "status": str,
            "complete": bool,
            "quantity": int,
            "multi_path": bool,
            "preempt": bool,
            "backup_path_type": str,
            "exclusive_links": List[Link],
            "inclusive_links": List[Link],
        }

        self.attribute_map = {
            "id": "id",
            "name": "name",
            "endpoints": "endpoints",
            "description": "description",
            "notifications": "notifications",
            "scheduling": "scheduling",
            "qos_metrics": "qos_metrics",
            "paths": "paths",
            "status": "status",
            "complete": "complete",
            "quantity": "quantity",
            "multi_path": "multi_path",
            "preempt": "preempt",
            "backup_path_type": "backup_path_type",
            "exclusive_links": "exclusive_links",
            "inclusive_links": "inclusive_links",
        }
        self._id = id
        self._name = name
        self._endpoints = endpoints
        self._description = description
        self._notifications = notifications
        self._scheduling = scheduling
        self._qos_metrics = qos_metrics
        self._paths = paths
        self._status = status
        self._complete = complete
        self._quantity = quantity
        self._multi_path = multi_path
        self._preempt = preempt
        self._backup_path_type = backup_path_type
        self._exclusive_links = exclusive_links
        self._inclusive_links = inclusive_links

    @classmethod
    def from_dict(cls, dikt):
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The connection_v2 of this ConnectionV2.  # noqa: E501
        :rtype: ConnectionV2
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this ConnectionV2.


        :return: The id of this ConnectionV2.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ConnectionV2.


        :param id: The id of this ConnectionV2.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this ConnectionV2.


        :return: The name of this ConnectionV2.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ConnectionV2.


        :param name: The name of this ConnectionV2.
        :type name: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    @property
    def endpoints(self):
        """Gets the endpoints of this ConnectionV2.


        :return: The endpoints of this ConnectionV2.
        :rtype: List[Port]
        """
        return self._endpoints

    @endpoints.setter
    def endpoints(self, endpoints):
        """Sets the endpoints of this ConnectionV2.


        :param endpoints: The endpoints of this ConnectionV2.
        :type endpoints: List[Port]
        """
        if endpoints is None:
            raise ValueError(
                "Invalid value for `endpoints`, must not be `None`"
            )  # noqa: E501

        self._endpoints = endpoints

    @property
    def description(self):
        """Gets the description of this ConnectionV2.


        :return: The description of this ConnectionV2.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ConnectionV2.


        :param description: The description of this ConnectionV2.
        :type description: str
        """
        if description is None:
            raise ValueError(
                "Invalid value for `description`, must not be `None`"
            )  # noqa: E501

        self._description = description

    @property
    def notifications(self):
        """Gets the notifications of this ConnectionV2.


        :return: The notifications of this ConnectionV2.
        :rtype: List[Dict[str, object]]
        """
        return self._notifications

    @notifications.setter
    def notifications(self, notifications):
        """Sets the notifications of this ConnectionV2.


        :param notifications: The notifications of this ConnectionV2.
        :type notifications: List[Dict[str, object]]
        """
        if notifications is None:
            raise ValueError(
                "Invalid value for `notifications`, must not be `None`"
            )  # noqa: E501

        self._notifications = notifications

    @property
    def scheduling(self):
        """Gets the scheduling of this ConnectionV2.


        :return: The scheduling of this ConnectionV2.
        :rtype: ConnectionScheduling
        """
        return self._scheduling

    @scheduling.setter
    def scheduling(self, scheduling):
        """Sets the scheduling of this ConnectionV2.


        :param scheduling: The scheduling of this ConnectionV2.
        :type scheduling: ConnectionScheduling
        """
        if scheduling is None:
            raise ValueError(
                "Invalid value for `scheduling`, must not be `None`"
            )  # noqa: E501

        self._scheduling = scheduling

    @property
    def qos_metrics(self):
        """Gets the qos_metrics of this ConnectionV2.


        :return: The qos_metrics of this ConnectionV2.
        :rtype: Dict[str, ConnectionQosMetrics]
        """
        return self._qos_metrics

    @qos_metrics.setter
    def qos_metrics(self, qos_metrics):
        """Sets the qos_metrics of this ConnectionV2.


        :param qos_metrics: The qos_metrics of this ConnectionV2.
        :type qos_metrics: Dict[str, ConnectionQosMetrics]
        """
        if qos_metrics is None:
            raise ValueError(
                "Invalid value for `qos_metrics`, must not be `None`"
            )  # noqa: E501

        self._qos_metrics = qos_metrics

    @property
    def paths(self):
        """Gets the paths of this ConnectionV2.


        :return: The paths of this ConnectionV2.
        :rtype: List[str]
        """
        return self._paths

    @paths.setter
    def paths(self, paths):
        """Sets the paths of this ConnectionV2.


        :param paths: The paths of this ConnectionV2.
        :type paths: List[str]
        """

        self._paths = paths

    @property
    def status(self):
        """Gets the status of this ConnectionV2.

        Connection Status  # noqa: E501

        :return: The status of this ConnectionV2.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ConnectionV2.

        Connection Status  # noqa: E501

        :param status: The status of this ConnectionV2.
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
    def complete(self):
        """Gets the complete of this ConnectionV2.


        :return: The complete of this ConnectionV2.
        :rtype: bool
        """
        return self._complete

    @complete.setter
    def complete(self, complete):
        """Sets the complete of this ConnectionV2.


        :param complete: The complete of this ConnectionV2.
        :type complete: bool
        """

        self._complete = complete

    @property
    def quantity(self):
        """Gets the quantity of this ConnectionV2.


        :return: The quantity of this ConnectionV2.
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this ConnectionV2.


        :param quantity: The quantity of this ConnectionV2.
        :type quantity: int
        """

        self._quantity = quantity

    @property
    def multi_path(self):
        """Gets the multi_path of this ConnectionV2.


        :return: The multi_path of this ConnectionV2.
        :rtype: bool
        """
        return self._multi_path

    @multi_path.setter
    def multi_path(self, multi_path):
        """Sets the multi_path of this ConnectionV2.


        :param multi_path: The multi_path of this ConnectionV2.
        :type multi_path: bool
        """

        self._multi_path = multi_path

    @property
    def preempt(self):
        """Gets the preempt of this ConnectionV2.


        :return: The preempt of this ConnectionV2.
        :rtype: bool
        """
        return self._preempt

    @preempt.setter
    def preempt(self, preempt):
        """Sets the preempt of this ConnectionV2.


        :param preempt: The preempt of this ConnectionV2.
        :type preempt: bool
        """

        self._preempt = preempt

    @property
    def backup_path_type(self):
        """Gets the backup_path_type of this ConnectionV2.


        :return: The backup_path_type of this ConnectionV2.
        :rtype: str
        """
        return self._backup_path_type

    @backup_path_type.setter
    def backup_path_type(self, backup_path_type):
        """Sets the backup_path_type of this ConnectionV2.


        :param backup_path_type: The backup_path_type of this ConnectionV2.
        :type backup_path_type: str
        """
        allowed_values = ["0", "1", "2", "3"]  # noqa: E501
        if backup_path_type not in allowed_values:
            raise ValueError(
                "Invalid value for `backup_path_type` ({0}), must be one of {1}".format(
                    backup_path_type, allowed_values
                )
            )

        self._backup_path_type = backup_path_type

    @property
    def exclusive_links(self):
        """Gets the exclusive_links of this ConnectionV2.


        :return: The exclusive_links of this ConnectionV2.
        :rtype: List[Link]
        """
        return self._exclusive_links

    @exclusive_links.setter
    def exclusive_links(self, exclusive_links):
        """Sets the exclusive_links of this ConnectionV2.


        :param exclusive_links: The exclusive_links of this ConnectionV2.
        :type exclusive_links: List[Link]
        """

        self._exclusive_links = exclusive_links

    @property
    def inclusive_links(self):
        """Gets the inclusive_links of this ConnectionV2.


        :return: The inclusive_links of this ConnectionV2.
        :rtype: List[Link]
        """
        return self._inclusive_links

    @inclusive_links.setter
    def inclusive_links(self, inclusive_links):
        """Sets the inclusive_links of this ConnectionV2.


        :param inclusive_links: The inclusive_links of this ConnectionV2.
        :type inclusive_links: List[Link]
        """

        self._inclusive_links = inclusive_links