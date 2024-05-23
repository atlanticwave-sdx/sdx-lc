# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from sdx_lc import util
from sdx_lc.models.base_model_ import Model


class LinkMeasurementPeriod(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, period=None, time_unit=None):  # noqa: E501
        """LinkMeasurementPeriod - a model defined in Swagger

        :param period: The period of this LinkMeasurementPeriod.  # noqa: E501
        :type period: float
        :param time_unit: The time_unit of this LinkMeasurementPeriod.  # noqa: E501
        :type time_unit: str
        """
        self.swagger_types = {"period": float, "time_unit": str}

        self.attribute_map = {"period": "period", "time_unit": "time_unit"}
        self._period = period
        self._time_unit = time_unit

    @classmethod
    def from_dict(cls, dikt):
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The link_measurement_period of this LinkMeasurementPeriod.  # noqa: E501
        :rtype: LinkMeasurementPeriod
        """
        return util.deserialize_model(dikt, cls)

    @property
    def period(self):
        """Gets the period of this LinkMeasurementPeriod.


        :return: The period of this LinkMeasurementPeriod.
        :rtype: float
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this LinkMeasurementPeriod.


        :param period: The period of this LinkMeasurementPeriod.
        :type period: float
        """

        self._period = period

    @property
    def time_unit(self):
        """Gets the time_unit of this LinkMeasurementPeriod.


        :return: The time_unit of this LinkMeasurementPeriod.
        :rtype: str
        """
        return self._time_unit

    @time_unit.setter
    def time_unit(self, time_unit):
        """Sets the time_unit of this LinkMeasurementPeriod.


        :param time_unit: The time_unit of this LinkMeasurementPeriod.
        :type time_unit: str
        """

        self._time_unit = time_unit