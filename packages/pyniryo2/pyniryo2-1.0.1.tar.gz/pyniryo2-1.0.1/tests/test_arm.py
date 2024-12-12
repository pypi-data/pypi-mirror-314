#!/usr/bin/env python
import time
import unittest
import numpy as np
from threading import Event

from pyniryo2.objects import PoseObject
from pyniryo2.niryo_ros import NiryoRos
from pyniryo2.exceptions import RobotCommandException

from pyniryo2.arm.arm import Arm
from pyniryo2.arm.objects import JointStateObject, HardwareStatusObject
from pyniryo2.arm.enums import CalibrateMode, RobotAxis

robot_ip_address = "127.0.0.1"
port = 9090

test_order = ["test_hardware_status",
              "test_synchronous_calibration",
              #"test_calibration_callback",
              #"test_request_new_calibration_callback",
              # "test_learning_mode",
              "test_joints_state",
              "test_pose_state",
              "test_move_joints",
              "test_move_pose",
              "test_move_linear",
              "test_stop_move",
              "test_shift",
              "test_jog_joints",
              "test_jog_pose",
              "test_velocity",
              "test_kinematics"]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = NiryoRos(ip_address=robot_ip_address, port=port)
        cls.arm = Arm(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    @staticmethod
    def assertAlmostEqualVector(a, b, decimal=1):
        np.testing.assert_almost_equal(a, b, decimal)


# noinspection PyTypeChecker
class TestHardwareStatus(BaseTest):

    def test_hardware_status(self):
        self.assertIsNone(time.sleep(1))
        self.assertIsInstance(self.arm.hardware_status(), HardwareStatusObject)
        self.assertIsInstance(self.arm.hardware_status.value, HardwareStatusObject)

    def test_synchronous_calibration(self):
        self.assertIsNone(time.sleep(1))
        # Test Reset calibration
        self.assertIsNone(self.arm.reset_calibration())
        self.assertTrue(self.arm.need_calibration())

        # Test Auto calibration
        self.assertIsNone(self.arm.calibrate(CalibrateMode.AUTO))
        self.assertFalse(self.arm.need_calibration())
        self.assertIsNone(self.arm.reset_calibration())
        self.assertTrue(self.arm.need_calibration())
        self.assertIsNone(self.arm.calibrate_auto())
        self.assertFalse(self.arm.need_calibration())

        # Test Manual Calibration
        self.assertIsNone(self.arm.reset_calibration())
        self.assertTrue(self.arm.need_calibration())
        self.assertIsNone(self.arm.calibrate(CalibrateMode.MANUAL))
        self.assertFalse(self.arm.need_calibration())

    def test_calibration_callback(self):
        self.assertIsNone(time.sleep(1))
        calibration_event = Event()
        calibration_event.clear()

        def callback_calibration_end(response):
            self.assertIsNotNone(response)
            self.assertIsNone(time.sleep(1))
            calibration_event.set()

        self.assertIsNone(self.arm.reset_calibration())
        self.assertTrue(self.arm.need_calibration())

        self.assertIsNone(self.arm.calibrate_auto(callback=callback_calibration_end))
        self.assertTrue(calibration_event.wait(30))
        self.assertIsNone(time.sleep(1))
        self.assertFalse(self.arm.need_calibration())

    def test_request_new_calibration_callback(self):
        calibration_event = Event()
        calibration_event.clear()

        def callback_calibration_end(response):
            self.assertIsNotNone(response)
            self.assertIsNone(time.sleep(1))
            calibration_event.set()

        self.assertIsNone(self.arm.calibrate(CalibrateMode.MANUAL))
        self.assertFalse(self.arm.need_calibration())

        self.assertIsNone(self.arm.request_new_calibration(callback=callback_calibration_end))
        self.assertTrue(self.arm.need_calibration())
        self.assertTrue(calibration_event.wait(30))
        self.assertIsNone(time.sleep(1))
        self.assertFalse(self.arm.need_calibration())

    def test_learning_mode(self):
        self.assertIsNone(time.sleep(1))
        def setter_learning_mode(state):
            self.arm.learning_mode = state

        self.assertIsNone(self.arm.set_learning_mode(False))
        self.assertFalse(self.arm.learning_mode())

        self.assertIsNone(self.arm.set_learning_mode(True))
        self.assertTrue(self.arm.learning_mode())

        self.assertIsNone(setter_learning_mode(False))
        self.assertFalse(self.arm.get_learning_mode())

        self.assertIsNone(setter_learning_mode(True))
        self.assertTrue(self.arm.get_learning_mode())

        self.assertIsNone(time.sleep(2))

    def test_joints_state(self):
        self.assertIsNone(time.sleep(1))
        self.arm.learning_mode = False
        self.assertIsNone(time.sleep(1))
        self.assertAlmostEqualVector(self.arm.joints_state().position, self.arm.joints)
        self.assertAlmostEqualVector(self.arm.joints_state.value.position, self.arm.get_joints())
        self.assertIsInstance(self.arm.joints_state(), JointStateObject)
        #self.arm.learning_mode = True

    def test_pose_state(self):
        self.assertIsNone(time.sleep(1))
        self.assertIsNotNone(self.arm.get_pose())
        self.assertIsNotNone(self.arm.get_pose().x)
        self.assertIsNotNone(self.arm.get_pose().y)
        self.assertIsNotNone(self.arm.get_pose().z)
        self.assertIsNotNone(self.arm.get_pose().roll)
        self.assertIsNotNone(self.arm.get_pose().pitch)
        self.assertIsNotNone(self.arm.get_pose().yaw)
        self.assertIsNotNone(self.arm.get_pose.value)
        self.assertIsNotNone(self.arm.pose)
        self.assertIsNotNone(self.arm.get_pose_quat())

    def test_move_joints(self):
        self.assertIsNone(time.sleep(1))
        def setter_joints(joints):
            self.arm.joints = joints

        self.arm.set_learning_mode(False)

        self.assertIsNone(self.arm.move_joints(6 * [0.2]))
        self.assertAlmostEqualVector(self.arm.joints, 6 * [0.2])

        end_move_event = Event()
        end_move_event.clear()

        def end_move_callback(_):
            end_move_event.set()

        self.assertIsNone(self.arm.move_joints(6 * [-0.2], end_move_callback))
        self.assertTrue(end_move_event.wait(10))
        self.assertAlmostEqualVector(self.arm.joints, 6 * [-0.2])

        self.assertIsNone(setter_joints(6 * [0.2]))
        self.assertAlmostEqualVector(self.arm.get_joints(), 6 * [0.2])

        self.assertIsNone(self.arm.move_to_home_pose())
        self.assertAlmostEqualVector(self.arm.get_joints(), [0.0, 0.3, -1.3, 0.0, 0.0, 0.0])

        self.assertIsNone(self.arm.go_to_sleep())

    def test_move_pose(self):
        self.assertIsNone(time.sleep(1))
        def setter_pose(pose):
            self.arm.pose = pose

        self.assertIsNone(self.arm.move_pose(PoseObject(0.2, 0, 0.1, 0, 1.5, 0)))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), [0.2, 0, 0.1, 0, 1.5, 0])

        self.assertIsNone(setter_pose([0.2, 0, 0.3, 0, 1.5, 0]))
        self.assertAlmostEqualVector(self.arm.pose.to_list(), [0.2, 0, 0.3, 0, 1.5, 0])

        end_move_event = Event()
        end_move_event.clear()

        def end_move_callback(_):
            end_move_event.set()

        self.assertIsNone(self.arm.move_pose([0.1, 0, 0.2, 0, 1.5, 0], end_move_callback))
        self.assertTrue(end_move_event.wait(10))
        self.assertAlmostEqualVector(self.arm.pose.to_list(), [0.1, 0, 0.2, 0, 1.5, 0])

        with self.assertRaises(RobotCommandException):
            self.arm.move_pose([0.54, 0.964, 0.34, "a", "m", CalibrateMode.AUTO])

        #self.arm.set_learning_mode(True)

    def test_move_linear(self):
        self.assertIsNone(time.sleep(1))
        pose1 = [0.2, -0.1, 0.3, 0, 0, 0]
        self.assertIsNone(self.arm.move_pose(pose1))
        self.assertIsNone(time.sleep(0.5))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), pose1)

        pose2 = [0.2, 0., 0.4, 0, 0, 0]
        self.assertIsNone(self.arm.move_linear_pose(pose2))
        self.assertIsNone(time.sleep(0.5))
        self.assertAlmostEqualVector(self.arm.pose.to_list(), pose2)

        pose3 = [0.2, 0.1, 0.3, 0, 0, 0]
        self.assertIsNone(self.arm.move_linear_pose(PoseObject(*pose3)))
        self.assertIsNone(time.sleep(0.5))
        self.assertAlmostEqualVector(self.arm.pose.to_list(), pose3)

        end_move_event = Event()
        end_move_event.clear()

        def end_move_callback(_):
            end_move_event.set()

        pose4 = [0.2, -0.1, 0.3, 0, 0, 0]
        self.assertIsNone(self.arm.move_linear_pose(pose4, end_move_callback))
        self.assertTrue(end_move_event.wait(10))
        self.assertAlmostEqualVector(self.arm.pose.to_list(), pose4)

        with self.assertRaises(RobotCommandException):
            self.arm.move_linear_pose([0.54, 0.964, "m", CalibrateMode.AUTO])

        #self.arm.set_learning_mode(True)

    def test_stop_move(self):
        self.assertIsNone(time.sleep(1))
        joints = [0., 0., 0., 0., 0., 0.]
        self.assertIsNone(self.arm.move_joints(joints))
        self.assertAlmostEqualVector(self.arm.joints, joints)

        end_move_event = Event()
        end_move_event.clear()

        def end_move_callback(_):
            end_move_event.set()

        joints = [0.0, 0.3, -1.3, 0.0, 0.0, 0.0]
        self.assertIsNone(self.arm.move_joints(joints, end_move_callback))
        self.assertIsNone(time.sleep(1))
        self.assertIsNone(self.arm.stop_move())
        self.assertTrue(end_move_event.wait(10))

        with self.assertRaises(AssertionError):
            self.assertAlmostEqualVector(self.arm.joints, joints)

        self.assertIsNone(time.sleep(1))
        self.assertIsNone(self.arm.go_to_sleep())

    def test_shift(self):
        self.assertIsNone(time.sleep(3))
        end_move_event = Event()
        end_move_event.clear()

        def end_move_callback(_):
            end_move_event.set()

        self.assertIsNone(self.arm.move_pose([0.2, 0.1, 0.1, 0, 1., 0]))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), [0.2, 0.1, 0.1, 0, 1., 0])

        self.assertIsNone(self.arm.shift_pose(RobotAxis.X, 0.1))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), [0.3, 0.1, 0.1, 0, 1., 0])

        self.assertIsNone(self.arm.shift_pose(RobotAxis.Y, -0.1))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), [0.3, 0., 0.1, 0, 1., 0])

        self.assertIsNone(self.arm.shift_pose(RobotAxis.Z, 0.1, end_move_callback))
        self.assertTrue(end_move_event.wait(10))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), [0.3, 0., 0.2, 0, 1., 0])

        self.assertIsNone(self.arm.move_pose([0.2, 0., 0.3, 0, 0, 0]))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), [0.2, 0., 0.3, 0, 0, 0])

        self.assertIsNone(self.arm.shift_pose(RobotAxis.PITCH, 1.))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), [0.2, 0., 0.3, 0, 1., 0])

        self.assertIsNone(self.arm.shift_pose(RobotAxis.ROLL, 0.5))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), [0.2, 0., 0.3, 0.5, 1., 0.])

        self.assertIsNone(self.arm.shift_pose(RobotAxis.YAW, -.5))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), [0.2, 0., 0.3, 0.5, 1., -.5])

        self.assertIsNone(self.arm.go_to_sleep())

    def test_jog_joints(self):
        self.assertIsNone(time.sleep(3))
        end_move_event = Event()
        end_move_event.clear()

        def end_move_callback(_):
            end_move_event.set()

        self.assertIsNone(self.arm.move_joints(6 * [0.0]))
        self.assertAlmostEqualVector(self.arm.get_joints(), 6 * [0.0])

        self.assertIsNone(self.arm.set_jog_control(True))

        self.assertIsNone(self.arm.jog_joints([-0.2, 0.0, 0.2, 0.2, 0, 0]))
        self.assertIsNone(time.sleep(2))
        self.assertAlmostEqualVector(self.arm.get_joints(), [-0.2, 0.0, 0.2, 0.2, 0, 0])

        self.assertIsNone(self.arm.jog_joints([0.2, 0.0, -0.2, -0.2, 0, 0], end_move_callback))
        self.assertTrue(end_move_event.wait(10))
        self.assertIsNone(time.sleep(2))
        self.assertAlmostEqualVector(self.arm.get_joints(), 6 * [0.0])

        # Check Exceptions
        with self.assertRaises(RobotCommandException):
            self.arm.jog_joints([0.1, 0.0, -0.1], 0.05)

        self.assertIsNone(self.arm.set_jog_control(False))

    def test_jog_pose(self):
        self.assertIsNone(time.sleep(3))
        end_move_event = Event()
        end_move_event.clear()

        def end_move_callback(_):
            end_move_event.set()

        self.assertIsNone(self.arm.move_pose([0.3, 0.0, 0.3, 0.0, 0.0, 0.0]))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), [0.3, 0.0, 0.3, 0.0, 0.0, 0.0])

        self.assertIsNone(self.arm.jog_pose([-0.01, 0.01, 0.01, 0., 0., 0.]))
        self.assertIsNone(time.sleep(0.5))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list()[:3], [0.29, 0.01, 0.31])

        pose1 = self.arm.get_pose().to_list()
        self.assertIsNone(self.arm.jog_pose([0., 0., 0., 0.1, 0.0, 0.0], end_move_callback))
        self.assertTrue(end_move_event.wait(10))
        self.assertIsNone(time.sleep(0.5))
        pose1[3] += 0.1
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), pose1)

        pose2 = self.arm.get_pose().to_list()
        self.assertIsNone(self.arm.jog_pose([0., 0., 0., 0., -0.1, 0.]))
        self.assertIsNone(time.sleep(0.5))
        pose2[4] -= 0.1
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), pose2)

        pose3 = self.arm.get_pose().to_list()
        self.assertIsNone(self.arm.jog_pose([0., 0., 0., 0., 0., 0.1]))
        self.assertIsNone(time.sleep(0.5))
        pose3[5] += 0.1
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), pose3)

        # Check Exceptions
        with self.assertRaises(RobotCommandException):
            self.arm.jog_pose([0.1, 0.0, -0.1], 0.05)

        self.assertIsNone(self.arm.set_jog_control(False))

    def test_velocity(self):
        self.assertIsNone(time.sleep(1))
        self.assertIsNone(self.arm.set_arm_max_velocity(100))
        self.assertEqual(self.arm.get_arm_max_velocity(), 100)

        self.velocity = None

        def velocity_callback(msg):
            self.velocity = msg

        self.assertIsNone(self.arm.get_arm_max_velocity.subscribe(velocity_callback))
        self.assertIsNone(self.arm.set_arm_max_velocity(50))
        self.assertIsNone(time.sleep(1))
        self.assertEqual(self.velocity, 50)

        with self.assertRaises(RobotCommandException):
            self.arm.set_arm_max_velocity(101)

        with self.assertRaises(RobotCommandException):
            self.arm.set_arm_max_velocity(-1)

        with self.assertRaises(RobotCommandException):
            self.arm.set_arm_max_velocity(0)

        self.assertIsNone(time.sleep(0.5))
        self.assertIsNone(self.arm.set_arm_max_velocity(100))
        self.assertIsNone(time.sleep(0.5))
        self.assertEqual(self.arm.get_arm_max_velocity(), 100)


    def test_kinematics(self):
        self.assertIsNone(time.sleep(1))
        # Forward Kinematics
        joints_target = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        pose_target = self.arm.forward_kinematics(joints_target)
        self.assertIsNone(self.arm.move_pose(pose_target))
        self.assertAlmostEqualVector(pose_target.to_list(), self.arm.get_pose().to_list())
        joints_reached = self.arm.get_joints()
        self.assertAlmostEqualVector(joints_target, joints_reached)

        # Inverse Kinematics
        pose_target = [0.2, 0.0, 0.3, 0.0, 0.0, 0.0]
        joints_target = self.arm.inverse_kinematics(pose_target)
        self.assertIsNone(self.arm.move_joints(joints_target))
        pose_reached = self.arm.get_pose()
        self.assertAlmostEqualVector(pose_target, pose_reached.to_list())

        #self.assertIsNone(self.arm.set_learning_mode(True))


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestHardwareStatus(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
