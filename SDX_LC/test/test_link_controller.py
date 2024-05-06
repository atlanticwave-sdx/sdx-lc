# coding: utf-8

from __future__ import absolute_import

import datetime

from flask import json
from six import BytesIO

from swagger_server.models.link import Link  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLinkController(BaseTestCase):
    """LinkController integration test stubs"""

    def test_add_link(self):
        """Test case for add_link

        add a new link to the topology
        """
        body = Link(
            id="test_add_link_id",
            name="test_add_link_name",
            short_name="test_add_link_short_name",
            ports=list(),
            bandwidth=1.0,
            residual_bandwidth=1.0,
            latency=1.0,
            packet_loss=0.0,
            availability=0.0,
            status="unknown",
            state="unknown",
            private_attributes=list(),
            timestamp=datetime.datetime.fromtimestamp(0),
            measurement_period=None,
        )
        response = self.client.open(
            "/SDX-LC/1.0.0/link",
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
            "/SDX-LC/1.0.0/link",
            method="DELETE",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_get_link(self):
        """Test case for get_link

        get an existing link
        """
        response = self.client.open("/SDX-LC/1.0.0/link", method="GET")
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_update_link(self):
        """Test case for update_link

        Update an existing link
        """
        body = Link(
            id="test_update_link_id",
            name="test_update_link_name",
            short_name="test_update_link_short_name",
            ports=list(),
            bandwidth=1.0,
            residual_bandwidth=1.0,
            latency=1.0,
            packet_loss=0.0,
            availability=0.0,
            status="unknown",
            state="unknown",
            private_attributes=list(),
            timestamp=datetime.datetime.fromtimestamp(0),
            measurement_period=None,
        )
        response = self.client.open(
            "/SDX-LC/1.0.0/link",
            method="PUT",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    import unittest

    unittest.main()
