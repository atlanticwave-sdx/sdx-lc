import datetime
import unittest

from sdx_lc.models.connection_qos_metrics import ConnectionQosMetrics
from sdx_lc.models.connection_scheduling import ConnectionScheduling
from sdx_lc.models.connection_v2 import Connection
from sdx_lc.models.link import Link
from sdx_lc.models.port import Port


class TestConnection(unittest.TestCase):
    def test_connection(self):
        # Create test data
        endpoints = [Port(id="port1"), Port(id="port2")]
        scheduling = ConnectionScheduling(
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now() + datetime.timedelta(hours=1),
        )
        qos_metrics = ConnectionQosMetrics(min_bw=100, max_delay=10, max_number_oxps=2)
        paths = ["path1", "path2"]
        exclusive_links = [Link(id="link1"), Link(id="link2")]

        # Create a Connection instance
        connection = Connection(
            id="connection1",
            name="Test Connection",
            endpoints=endpoints,
            description="Test Description",
            scheduling=scheduling,
            qos_metrics=qos_metrics,
            paths=paths,
            exclusive_links=exclusive_links,
        )
        print(connection.to_dict())
        # Perform assertions
        self.assertEqual(connection.id, "connection1")
        self.assertEqual(connection.name, "Test Connection")
        self.assertEqual(connection.endpoints, endpoints)
        self.assertEqual(connection.description, "Test Description")
        self.assertEqual(connection.scheduling, scheduling)
        self.assertEqual(connection.qos_metrics, qos_metrics)
        self.assertEqual(connection.paths, paths)
        self.assertEqual(connection.exclusive_links, exclusive_links)


if __name__ == "__main__":
    unittest.main()
