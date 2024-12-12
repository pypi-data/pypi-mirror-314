#!/usr/bin/env python
import unittest
import time
import random

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.niryo_ros import NiryoRos
from pyniryo2.sound.enums import Language
from pyniryo2.sound.sound import Sound
from pyniryo2.niryo_topic import NiryoTopic

robot_ip_address = "127.0.0.1"
port = 9090

test_order = ["test_volume",
              "test_sound",
              "test_say"]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = NiryoRos(ip_address=robot_ip_address, port=port)
        cls.sound = Sound(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()


# noinspection PyTypeChecker
class TestSound(BaseTest):
    def test_sound(self):
        self.assertIsInstance(self.sound.sounds, list)
        self.assertIsNotNone(self.sound.get_sounds())
        self.assertEqual(self.sound.sounds, self.sound.get_sounds())

        sound_names = self.sound.sounds
        random_sound_name = sound_names[random.randint(0,len(sound_names)-1)]
        self.assertTrue(0 < self.sound.get_sound_duration(random_sound_name))

        start_time = time.time()
        self.assertIsNone(self.sound.play(random_sound_name, True, 0.2, 1.2))
        self.assertTrue(0.5 <= time.time() - start_time <= 3.5)

        start_time = time.time()
        self.assertIsNone(self.sound.play(random_sound_name, False))
        self.assertTrue(time.time() - start_time <= 0.5)

        self.assertEqual(self.sound.state(), random_sound_name)
        self.assertIsNone(self.sound.stop())
        time.sleep(0.1)
        self.assertNotEqual(self.sound.state(), random_sound_name)

        with self.assertRaises(RobotCommandException):
            self.sound.play(450)

        with self.assertRaises(RobotCommandException):
            self.sound.play(True)

    def test_say(self):
        for language in Language:
            start_time = time.time()
            self.assertIsNone(self.sound.say('This is a test', language))
            self.assertTrue(time.time() - start_time > 0.5)

        with self.assertRaises(RobotCommandException):
            self.sound.say('This is a test', 0)

        with self.assertRaises(RobotCommandException):
            self.sound.say(450, Language.ENGLISH)

    def test_volume(self):
        self.assertIsInstance(self.sound.volume, NiryoTopic)
        self.assertIsNotNone(self.sound.volume.value)
        self.assertIsNotNone(self.sound.get_volume())
        self.assertEqual(self.sound.get_volume(), self.sound.volume())

        self.assertIsNone(self.sound.set_volume(50))
        self.assertEqual(self.sound.volume(), 50)

        self.assertIsNone(self.sound.set_volume(10))
        self.assertEqual(self.sound.volume(), 10)

        with self.assertRaises(RobotCommandException):
            self.sound.set_volume(-100)

        with self.assertRaises(RobotCommandException):
            self.sound.set_volume(300)

def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestSound(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
