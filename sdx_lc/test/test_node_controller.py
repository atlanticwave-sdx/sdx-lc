# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from sdx_lc.models.location import Location
from sdx_lc.models.node import Node  # noqa: E501
from sdx_lc.models.port import Port
from sdx_lc.test import BaseTestCase


class TestNodeController(BaseTestCase):
    """NodeController integration test stubs"""

    __location = Location(
        address="unknown",
        latitude=0.0,
        longitude=0.0,
        iso3166_2_lvl4="US-FL",
    )

    __ports = [
        Port(
            id="urn:sdx:port:test.net:test1:1",
            name="test_node_port_name",
            node="urn:sdx:node:test.net:test1",
            status="up",
            state="enabled",
            type="100GE",
        )
    ]

    __node = Node(
        id="urn:sdx:node:test.net:test1",
        name="test_node_name",
        location=__location,
        ports=__ports,
    )

    def test_add_node(self):
        """Test case for add_node

        add a new node to the topology
        """
        response = self.client.open(
            "/SDX-LC/2.0.0/node",
            method="POST",
            data=json.dumps(self.__node),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_delete_node(self):
        """Test case for delete_node

        Deletes a node
        """
        query_string = [("node_id", 789)]
        headers = [("api_key", "api_key_example")]
        response = self.client.open(
            "/SDX-LC/2.0.0/node",
            method="DELETE",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_get_node(self):
        """Test case for get_node

        get an existing node
        """
        response = self.client.open("/SDX-LC/2.0.0/node", method="GET")
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_update_node(self):
        """Test case for update_node

        Update an existing node
        """
        location = Location(
            address="unknown",
            latitude=0.0,
            longitude=0.0,
            iso3166_2_lvl4="US-FL",
        )
        response = self.client.open(
            "/SDX-LC/2.0.0/node",
            method="PUT",
            data=json.dumps(self.__node),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    import unittest

    unittest.main()
