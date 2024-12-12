#!/usr/bin/env python

import numpy as np
import sys
import unittest
import roslibpy
from threading import Event

from pyniryo2.niryo_topic import NiryoTopic
from pyniryo2.exceptions import TopicException
from pyniryo2.niryo_ros import NiryoRos

robot_ip_address = "127.0.0.1"
port = 9090


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = NiryoRos(ip_address=robot_ip_address, port=port)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    @staticmethod
    def assertAlmostEqualVector(a, b, decimal=1):
        np.testing.assert_almost_equal(a, b, decimal)


# noinspection PyTypeChecker
class TestTopic(BaseTest):

    def setUp(self):
        self.topic_name = '/joint_states'
        self.topic_type = 'sensor_msgs/JointState'

    def test_subscribe_unsubscribe(self):
        self.topic_message = None
        self.message_event = Event()
        self.message_event.clear()

        def callback(message):
            self.topic_message = message
            self.message_event.set()

        topic = NiryoTopic(self.client, self.topic_name, self.topic_type)

        self.assertFalse(topic.is_subscribed)

        # Try a bad subscription
        with self.assertRaises(TopicException):
            topic.subscribe(None)

        # Subscribe
        self.assertIsNone(topic.subscribe(callback))
        self.assertTrue(topic.is_subscribed)

        # Wait a message
        self.assertTrue(self.message_event.wait(timeout=0.5))
        self.assertIsNotNone(self.topic_message)

        # Unsubscibe
        self.assertIsNone(topic.unsubscribe())
        self.assertFalse(topic.is_subscribed)

    def test_type_conversion(self):
        def conversion_get_joint_name(msg):
            return str(msg["name"][0])

        topic = NiryoTopic(self.client, self.topic_name, self.topic_type, conversion_function=conversion_get_joint_name)
        self.assertIsInstance(topic(), str)

        def conversion_get_joint_value(msg):
            return float(msg["position"][0])

        topic = NiryoTopic(self.client, self.topic_name, self.topic_type,
                           conversion_function=conversion_get_joint_value)
        self.assertIsInstance(topic(), float)

    def test_synchronous_access(self):
        self.assertTrue(self.client.is_connected)

        topic = NiryoTopic(self.client, self.topic_name, self.topic_type)
        self.assertFalse(topic.is_subscribed)

        # Wait a message
        message = topic()
        self.assertIsNotNone(message)
        self.assertNotEqual(message, topic())

        self.assertFalse(topic.is_subscribed)

    def test_synchronous_with_asynchronous_access(self):
        self.topic_message = None
        self.message_event = Event()
        self.message_event.clear()

        def callback(message):
            self.assertEqual(topic(), message)
            self.topic_message = message
            self.message_event.set()

        topic = NiryoTopic(self.client, self.topic_name, self.topic_type)

        # Synchronous access
        self.assertIsNotNone(topic())
        self.assertFalse(topic.is_subscribed)

        # Subscribe
        self.assertIsNone(topic.subscribe(callback))
        self.assertTrue(topic.is_subscribed)

        # Wait a message
        self.assertTrue(self.message_event.wait(timeout=0.5))
        self.assertIsNotNone(self.topic_message)

        # Unsubscibe
        self.assertIsNone(topic.unsubscribe())
        self.assertFalse(topic.is_subscribed)


if __name__ == '__main__':
    unittest.main()
