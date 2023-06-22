""" New_topology class """
# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.new_topology_links import NewTopologyLinks  # noqa: F401,E501
from swagger_server.models.new_topology_nodes import NewTopologyNodes  # noqa: F401,E501
import re  # noqa: F401,E501
from swagger_server import util


class NewTopology(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: str=None, name: str=None, version: int=None, model_version: str=None, timestamp: datetime=None, nodes: List[NewTopologyNodes]=None, links: List[NewTopologyLinks]=None):  # noqa: E501
        """NewTopology - a model defined in Swagger

        :param id: The id of this NewTopology.  # noqa: E501
        :type id: str
        :param name: The name of this NewTopology.  # noqa: E501
        :type name: str
        :param version: The version of this NewTopology.  # noqa: E501
        :type version: int
        :param model_version: The model_version of this NewTopology.  # noqa: E501
        :type model_version: str
        :param timestamp: The timestamp of this NewTopology.  # noqa: E501
        :type timestamp: datetime
        :param nodes: The nodes of this NewTopology.  # noqa: E501
        :type nodes: List[NewTopologyNodes]
        :param links: The links of this NewTopology.  # noqa: E501
        :type links: List[NewTopologyLinks]
        """
        self.swagger_types = {
            'id': str,
            'name': str,
            'version': int,
            'model_version': str,
            'timestamp': datetime,
            'nodes': List[NewTopologyNodes],
            'links': List[NewTopologyLinks]
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'version': 'version',
            'model_version': 'model_version',
            'timestamp': 'timestamp',
            'nodes': 'nodes',
            'links': 'links'
        }
        self._id = id
        self._name = name
        self._version = version
        self._model_version = model_version
        self._timestamp = timestamp
        self._nodes = nodes
        self._links = links

    @classmethod
    def from_dict(cls, dikt) -> 'NewTopology':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The NewTopology of this NewTopology.  # noqa: E501
        :rtype: NewTopology
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this NewTopology.


        :return: The id of this NewTopology.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this NewTopology.


        :param id: The id of this NewTopology.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this NewTopology.


        :return: The name of this NewTopology.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this NewTopology.


        :param name: The name of this NewTopology.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def version(self) -> int:
        """Gets the version of this NewTopology.


        :return: The version of this NewTopology.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version: int):
        """Sets the version of this NewTopology.


        :param version: The version of this NewTopology.
        :type version: int
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def model_version(self) -> str:
        """Gets the model_version of this NewTopology.


        :return: The model_version of this NewTopology.
        :rtype: str
        """
        return self._model_version

    @model_version.setter
    def model_version(self, model_version: str):
        """Sets the model_version of this NewTopology.


        :param model_version: The model_version of this NewTopology.
        :type model_version: str
        """
        if model_version is None:
            raise ValueError("Invalid value for `model_version`, must not be `None`")  # noqa: E501

        self._model_version = model_version

    @property
    def timestamp(self) -> datetime:
        """Gets the timestamp of this NewTopology.


        :return: The timestamp of this NewTopology.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        """Sets the timestamp of this NewTopology.


        :param timestamp: The timestamp of this NewTopology.
        :type timestamp: datetime
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

        self._timestamp = timestamp

    @property
    def nodes(self) -> List[NewTopologyNodes]:
        """Gets the nodes of this NewTopology.


        :return: The nodes of this NewTopology.
        :rtype: List[NewTopologyNodes]
        """
        return self._nodes

    @nodes.setter
    def nodes(self, nodes: List[NewTopologyNodes]):
        """Sets the nodes of this NewTopology.


        :param nodes: The nodes of this NewTopology.
        :type nodes: List[NewTopologyNodes]
        """

        self._nodes = nodes

    @property
    def links(self) -> List[NewTopologyLinks]:
        """Gets the links of this NewTopology.


        :return: The links of this NewTopology.
        :rtype: List[NewTopologyLinks]
        """
        return self._links

    @links.setter
    def links(self, links: List[NewTopologyLinks]):
        """Sets the links of this NewTopology.


        :param links: The links of this NewTopology.
        :type links: List[NewTopologyLinks]
        """

        self._links = links