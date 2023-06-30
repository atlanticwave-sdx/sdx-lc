# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.new_event import NewEvent  # noqa: F401,E501
from swagger_server.models.new_kytos_topology import NewKytosTopology  # noqa: F401,E501
from swagger_server import util


class NewConstructor(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, event: List[NewEvent]=None, kytostopology: NewKytosTopology=None):  # noqa: E501
        """NewConstructor - a model defined in Swagger

        :param event: The event of this NewConstructor.  # noqa: E501
        :type event: List[NewEvent]
        :param kytostopology: The kytostopology of this NewConstructor.  # noqa: E501
        :type kytostopology: NewKytosTopology
        """
        self.swagger_types = {
            'event': List[NewEvent],
            'kytostopology': NewKytosTopology
        }

        self.attribute_map = {
            'event': 'event',
            'kytostopology': 'kytostopology'
        }
        self._event = event
        self._kytostopology = kytostopology

    @classmethod
    def from_dict(cls, dikt) -> 'NewConstructor':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The NewConstructor of this NewConstructor.  # noqa: E501
        :rtype: NewConstructor
        """
        return util.deserialize_model(dikt, cls)

    @property
    def event(self) -> List[NewEvent]:
        """Gets the event of this NewConstructor.


        :return: The event of this NewConstructor.
        :rtype: List[NewEvent]
        """
        return self._event

    @event.setter
    def event(self, event: List[NewEvent]):
        """Sets the event of this NewConstructor.


        :param event: The event of this NewConstructor.
        :type event: List[NewEvent]
        """

        self._event = event

    @property
    def kytostopology(self) -> NewKytosTopology:
        """Gets the kytostopology of this NewConstructor.


        :return: The kytostopology of this NewConstructor.
        :rtype: NewKytosTopology
        """
        return self._kytostopology

    @kytostopology.setter
    def kytostopology(self, kytostopology: NewKytosTopology):
        """Sets the kytostopology of this NewConstructor.


        :param kytostopology: The kytostopology of this NewConstructor.
        :type kytostopology: NewKytosTopology
        """

        self._kytostopology = kytostopology
