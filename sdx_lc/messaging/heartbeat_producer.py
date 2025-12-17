#!/usr/bin/env python
import json
import logging
import os
import threading
import time
from datetime import datetime

import pika

MQ_HOST = os.environ.get("MQ_HOST")
MQ_PORT = os.environ.get("MQ_PORT")
MQ_USER = os.environ.get("MQ_USER")
MQ_PASS = os.environ.get("MQ_PASS")
SDXLC_DOMAIN = os.environ.get("SDXLC_DOMAIN")
HEARTBEAT_INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", 30))  # seconds


class HeartbeatProducer:
    """
    Process-level heartbeat sender.
    One instance per LC process.
    """

    def __init__(self, exchange_name="", routing_key=""):
        self.logger = logging.getLogger(__name__)
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self._stop_event = threading.Event()

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=MQ_HOST,
                port=MQ_PORT,
                credentials=pika.PlainCredentials(username=MQ_USER, password=MQ_PASS),
            )
        )
        self.channel = self.connection.channel()

        self.logger.info("HeartbeatProducer started")

    def _build_msg(self):
        return {
            "type": "Heart Beat",
            "domain": SDXLC_DOMAIN,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    def _run(self):
        # Send immediately on startup
        self._send_once()

        while not self._stop_event.wait(HEARTBEAT_INTERVAL):
            self._send_once()

    def _send_once(self):
        try:
            msg = self._build_msg()
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=self.routing_key,
                body=json.dumps(msg),
            )
            self.logger.info(f"Heartbeat sent: {msg['timestamp']}")
        except Exception as e:
            self.logger.error(f"Heartbeat send failed: {e}")

    def stop(self):
        self.logger.info("Stopping HeartbeatProducer")
        self._stop_event.set()
        try:
            if self.channel.is_open:
                self.channel.close()
        except Exception:
            pass
        try:
            if self.connection.is_open:
                self.connection.close()
        except Exception:
            pass

    def start(self):
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
