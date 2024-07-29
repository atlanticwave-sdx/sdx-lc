# coding: utf-8

from __future__ import absolute_import

import datetime

from flask import json
from six import BytesIO

from sdx_lc.models.link import Link  # noqa: E501
from sdx_lc.test import BaseTestCase


class TestLinkController(BaseTestCase):
    """LinkController integration test stubs"""

    def test_add_link(self):
        """Test case for add_link

        add a new link to the topology
        """
        body = Link(
            id="urn:sdx:link:test.net:test_add_link_name",
            name="test_add_link_name",
            ports=[
                "urn:sdx:port:test.net:test1:1",
                "urn:sdx:port:test.net:test2:2",
            ],
            bandwidth=1.0,
            residual_bandwidth=1.0,
            latency=1.0,
            packet_loss=0.0,
            availability=0.0,
            status="up",
            state="enabled",
            measurement_period=None,
        )
        response = self.client.open(
            "/SDX-LC/2.0.0/link",
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_delete_link(self):
        """Test case for delete_link

        Deletes a link
        """
        query_string = [("node_id", 789)]
        headers = [("api_key", "api_key_example")]
        response = self.client.open(
            "/SDX-LC/2.0.0/link",
            method="DELETE",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_get_link(self):
        """Test case for get_link

        get an existing link
        """
        response = self.client.open("/SDX-LC/2.0.0/link", method="GET")
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_update_link(self):
        """Test case for update_link

        Update an existing link
        """
        body = Link(
            id="urn:sdx:link:test.net:test_update_link_name",
            name="test_update_link_name",
            ports=[
                "urn:sdx:port:test.net:test1:1",
                "urn:sdx:port:test.net:test2:2",
            ],
            bandwidth=1.0,
            residual_bandwidth=1.0,
            latency=1.0,
            packet_loss=0.0,
            availability=0.0,
            status="down",
            state="enabled",
            private=list(),
            measurement_period=None,
        )
        response = self.client.open(
            "/SDX-LC/2.0.0/link",
            method="PUT",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    import unittest

    unittest.main()
