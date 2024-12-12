#!/usr/bin/env python
import time
import unittest
from threading import Event

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.niryo_topic import NiryoTopic
from pyniryo2.niryo_ros import NiryoRos

from pyniryo2.io.enums import PinID, PinMode, PinState
from pyniryo2.io.objects import DigitalPinObject, AnalogPinObject
from pyniryo2.io.io import IO

robot_ip_address = "127.0.0.1"
port = 9090

test_order = ["get_digital_io_sate",
              "get_analog_io_sate",
              "test_pin_mode",
              "test_set_analog_pin_state",
              "test_set_digital_pin_state",
              ]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = NiryoRos(ip_address=robot_ip_address, port=port)
        cls.client.run()
        cls.io = IO(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()


# noinspection PyTypeChecker
class TestIO(BaseTest):
    def get_digital_io_sate(self):
        for pin in [PinID.DO1, PinID.DI2, PinID.DO4]:
            self.assertIsInstance(self.io.get_digital_io_states, NiryoTopic)
            self.assertIsInstance(self.io.get_digital_io_states(), list)
            self.assertIsInstance(self.io.get_digital_io_states()[0], DigitalPinObject)

            self.assertIsInstance(self.io.get_digital_io_state(pin), DigitalPinObject)
            self.assertIsInstance(self.io.digital_read(pin), bool)

            io_state = self.io.get_digital_io_state(pin)
            self.assertIsInstance(io_state.pin_id, PinID)
            self.assertIsInstance(io_state.name, str)
            self.assertIsInstance(io_state.mode, PinMode)
            self.assertIsInstance(io_state.value, bool)
            self.assertEqual(io_state.value, self.io.digital_read(pin))

            io_state_event = Event()
            io_state_event.clear()

            def io_state_callback(io_state_list):
                self.assertIsInstance(io_state_list, list)
                self.assertIsInstance(io_state_list[0], DigitalPinObject)
                io_state_event.set()

            self.assertIsNone(self.io.get_digital_io_states.subscribe(io_state_callback))
            self.assertTrue(io_state_event.wait(10))
            self.assertIsNone(self.io.get_digital_io_states.unsubscribe())

    def get_analog_io_sate(self):
        for pin in [PinID.AO1, PinID.AI2]:
            self.assertIsInstance(self.io.get_analog_io_states, NiryoTopic)
            self.assertIsInstance(self.io.get_analog_io_states(), list)
            self.assertIsInstance(self.io.get_analog_io_states()[0], AnalogPinObject)

            self.assertIsInstance(self.io.get_analog_io_state(pin), AnalogPinObject)
            self.assertIsInstance(self.io.analog_read(pin), (float, int))

            io_state = self.io.get_analog_io_state(pin)
            self.assertIsInstance(io_state.pin_id, PinID)
            self.assertIsInstance(io_state.name, str)
            self.assertIsInstance(io_state.mode, PinMode)
            self.assertIsInstance(io_state.value, (float, int))
            self.assertEqual(io_state.value, self.io.analog_read(pin))

            io_state_event = Event()
            io_state_event.clear()

            def io_state_callback(io_state_list):
                self.assertIsInstance(io_state_list, list)
                self.assertIsInstance(io_state_list[0], DigitalPinObject)
                io_state_event.set()

            self.assertIsNone(self.io.get_digital_io_states.subscribe(io_state_callback))
            self.assertTrue(io_state_event.wait(10))
            self.assertIsNone(self.io.get_digital_io_states.unsubscribe())

    def test_pin_mode(self):
        for pin_in in [PinID.DI1, PinID.DO1, PinID.AI1, PinID.AO1]:
            with self.assertRaises(RobotCommandException):
                self.assertIsNone(self.io.set_pin_mode(pin_in, PinMode.OUTPUT))

            with self.assertRaises(RobotCommandException):
                self.assertIsNone(self.io.set_pin_mode(pin_in, PinMode.INPUT))

    def test_set_digital_pin_state(self):
        # with self.assertRaises(RobotCommandException):
        #    self.io.digital_write(PinID.DI3, PinState.HIGH)

        for pin_id in [PinID.DO3]:  # , PinID.DO4]:
            self.assertIsNone(self.io.digital_write(pin_id, PinState.HIGH))
            time.sleep(0.1)
            self.assertEqual(self.io.get_digital_io_state(pin_id).value, True)
            self.assertEqual(self.io.digital_read(pin_id), True)
            self.assertIsNone(self.io.digital_write(pin_id, PinState.LOW))
            time.sleep(0.1)
            self.assertEqual(self.io.get_digital_io_state(pin_id).value, False)
            self.assertEqual(self.io.digital_read(pin_id), False)

            self.assertIsNone(self.io.digital_write(pin_id.value, True))
            time.sleep(0.1)
            self.assertEqual(self.io.get_digital_io_state(pin_id).value, True)
            self.assertEqual(self.io.digital_read(pin_id), True)
            self.assertIsNone(self.io.digital_write(pin_id.value, False))
            time.sleep(0.1)
            self.assertEqual(self.io.get_digital_io_state(pin_id).value, False)
            self.assertEqual(self.io.digital_read(pin_id), False)

        with self.assertRaises(RobotCommandException):
            self.io.digital_write(1, PinState.LOW)

        with self.assertRaises(RobotCommandException):
            self.io.digital_write(PinID.DO1, 0)

    def test_set_analog_pin_state(self):
        # with self.assertRaises(RobotCommandException):
        #    self.io.digital_write(PinID.AI1, PinState.HIGH)

        for pin_id in [PinID.AO1]:
            for value in [5.0, 2.5, 0]:
                self.assertIsNone(self.io.analog_write(pin_id, value))
                time.sleep(0.1)
                self.assertEqual(self.io.get_analog_io_state(pin_id).value, value)
                self.assertEqual(self.io.analog_read(pin_id), value)

            with self.assertRaises(RobotCommandException):
                self.io.analog_write(pin_id, PinState.LOW)

            with self.assertRaises(RobotCommandException):
                self.io.analog_write(pin_id, -1)

            with self.assertRaises(RobotCommandException):
                self.io.analog_write(pin_id, 10)

        with self.assertRaises(RobotCommandException):
            self.io.analog_write(PinID.DO1, 0)


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestIO(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
