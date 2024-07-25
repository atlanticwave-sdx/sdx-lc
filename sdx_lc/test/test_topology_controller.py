# coding: utf-8

from __future__ import absolute_import

import datetime

from flask import json
from six import BytesIO

from sdx_lc.models.api_response import ApiResponse  # noqa: E501
from sdx_lc.models.link import Link
from sdx_lc.models.location import Location
from sdx_lc.models.node import Node
from sdx_lc.models.port import Port
from sdx_lc.models.topology import Topology  # noqa: E501
from sdx_lc.test import BaseTestCase


class TestTopologyController(BaseTestCase):
    """TopologyController integration test stubs"""

    __location = Location(
        address="unknown",
        latitude=0.0,
        longitude=0.0,
        iso3166_2_lvl4="US-FL",
    )

    __ports = [
        Port(
            id="urn:sdx:port:example.net:test1:1",
            name="test_topology_port_name",
            node="urn:sdx:node:example.net:test1",
            nni="urn:sdx:link:example.net:test1/1_test1/2",
            status="up",
            state="enabled",
            type="100GE",
            mtu=9000,
        ),
        Port(
            id="urn:sdx:port:example.net:test1:2",
            name="test_topology_port_name2",
            node="urn:sdx:node:example.net:test1",
            nni="urn:sdx:link:example.net:test1/1_test1/2",
            status="up",
            state="enabled",
            type="100GE",
            mtu=9000,
        ),
        Port(
            id="urn:sdx:port:example.net:test1:3",
            name="test_topology_port_name3",
            node="urn:sdx:node:example.net:test1",
            nni="",
            status="up",
            state="enabled",
            type="100GE",
            mtu=9000,
        ),
        Port(
            id="urn:sdx:port:example.net:test1:4",
            name="test_topology_port_name4",
            node="urn:sdx:node:example.net:test1",
            nni="urn:sdx:port:otheroxp.net:other_sw:99",
            status="up",
            state="enabled",
            type="100GE",
            mtu=9000,
        ),
    ]

    __nodes = [
        Node(
            id="urn:sdx:node:example.net:test1",
            name="test_topology_node_name",
            location=__location,
            ports=__ports,
        )
    ]

    __links = [
        Link(
            id="urn:sdx:link:example.net:test1/1_test1/2",
            name="test_topology_link_name",
            ports=[
                "urn:sdx:port:example.net:test1:1",
                "urn:sdx:port:example.net:test1:2",
            ],
            bandwidth=1.0,
            residual_bandwidth=1.0,
            latency=1.0,
            packet_loss=0.0,
            availability=0.0,
            status="error",
            state="maintenance",
            measurement_period=None,
        )
    ]

    __topology = Topology(
        id="urn:sdx:topology:example.net",
        name="test_topology_name",
        model_version="2.0.0",
        services=None,
        version=0,
        timestamp=datetime.datetime.fromtimestamp(0),
        nodes=__nodes,
        links=__links,
        private_attributes=None,
    )

    def test_add_topology(self):
        """Test case for add_topology

        Send a new topology to SDX-LC
        """
        response = self.client.open(
            "/SDX-LC/2.0.0/topology",
            method="POST",
            data=json.dumps(self.__topology),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_delete_topology(self):
        """Test case for delete_topology

        Deletes a topology
        """
        query_string = [("topology_id", 789)]
        headers = [("api_key", "api_key_example")]
        response = self.client.open(
            "/SDX-LC/2.0.0/topology",
            method="DELETE",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_delete_topology_version(self):
        """Test case for delete_topology_version

        Deletes a topology version
        """
        query_string = [("topology_id", 789)]
        headers = [("api_key", "api_key_example")]
        response = self.client.open(
            "/SDX-LC/2.0.0/topology/{version}".format(version=789),
            method="DELETE",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_get_topology(self):
        """Test case for get_topology

        get an existing topology
        """
        response = self.client.open("/SDX-LC/2.0.0/topology", method="GET")
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_get_topologyby_version(self):
        """Test case for get_topologyby_version

        Find topology by version
        """
        query_string = [("topology_id", 789)]
        response = self.client.open(
            "/SDX-LC/2.0.0/topology/{version}".format(version=789),
            method="GET",
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_topology_version(self):
        """Test case for topology_version

        Finds topology version
        """
        query_string = [("topology_id", "topology_id_example")]
        response = self.client.open(
            "/SDX-LC/2.0.0/topology/version", method="GET", query_string=query_string
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_update_topology(self):
        """Test case for update_topology

        Update an existing topology
        """
        response = self.client.open(
            "/SDX-LC/2.0.0/topology",
            method="PUT",
            data=json.dumps(self.__topology),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_upload_file(self):
        """Test case for upload_file

        uploads an topology image
        """
        body = Topology()
        response = self.client.open(
            "/SDX-LC/2.0.0/topology/{topology_id}/uploadImage".format(topology_id=789),
            method="POST",
            data=json.dumps(body),
            content_type="application/octet-stream",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    import unittest

    unittest.main()
