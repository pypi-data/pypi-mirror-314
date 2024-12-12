#!/usr/bin/env python
import unittest
import roslibpy

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.objects import PoseObject
from pyniryo2.niryo_ros import NiryoRos

from pyniryo2.saved_poses.saved_poses import SavedPoses

robot_ip_address = "127.0.0.1"
port = 9090

test_order = ["test_get_saved_poses_list",
              "test_get_saved_pose",
              "test_manage_pose",
              ]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = NiryoRos(ip_address=robot_ip_address, port=port)
        cls.saved_poses = SavedPoses(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()


# noinspection PyTypeChecker
class TestSavedPoses(BaseTest):
    def test_get_saved_poses_list(self):
        self.assertIsInstance(self.saved_poses.get_saved_pose_list(), list)

    def test_get_saved_pose(self):
        for pose_name in self.saved_poses.get_saved_pose_list():
            self.assertIsInstance(self.saved_poses.get_pose_saved(pose_name), PoseObject)

        if "unittest_pose" in self.saved_poses.get_saved_pose_list():
            self.assertIsNone(self.saved_poses.delete_pose("unittest_pose"))
            self.assertFalse("unittest_pose" in self.saved_poses.get_saved_pose_list())
        with self.assertRaises(RobotCommandException):
            self.saved_poses.get_pose_saved("unittest_pose")

    def test_manage_pose(self):
        if "unittest_pose" in self.saved_poses.get_saved_pose_list():
            self.assertIsNone(self.saved_poses.delete_pose("unittest_pose"))
            self.assertFalse("unittest_pose" in self.saved_poses.get_saved_pose_list())

        self.assertIsNone(self.saved_poses.save_pose("unittest_pose", 0.3, 0.0, 0.3, 0.0, 1.57, 0.0))
        self.assertTrue("unittest_pose" in self.saved_poses.get_saved_pose_list())
        self.assertIsInstance(self.saved_poses.get_pose_saved("unittest_pose"), PoseObject)
        self.assertIsInstance(self.saved_poses.get_saved_pose_list()[0], str)
        self.assertIsNone(self.saved_poses.delete_pose("unittest_pose"))
        self.assertFalse("unittest_pose" in self.saved_poses.get_saved_pose_list())

        self.assertIsNone(self.saved_poses.save_pose("unittest_pose", [0.3, 0.0, 0.3, 0.0, 1.57, 0.0]))
        self.assertTrue("unittest_pose" in self.saved_poses.get_saved_pose_list())
        self.assertIsNone(self.saved_poses.delete_pose("unittest_pose"))
        self.assertFalse("unittest_pose" in self.saved_poses.get_saved_pose_list())

        self.assertIsNone(self.saved_poses.save_pose("unittest_pose", PoseObject(0.3, 0.0, 0.3, 0.0, 1.57, 0.0)))
        self.assertIsNone(self.saved_poses.save_pose("unittest_pose", PoseObject(0.3, 0.0, 0.3, 0.0, 1.57, 0.0)))

        self.assertTrue("unittest_pose" in self.saved_poses.get_saved_pose_list())
        self.assertIsNone(self.saved_poses.delete_pose("unittest_pose"))
        self.assertFalse("unittest_pose" in self.saved_poses.get_saved_pose_list())

        with self.assertRaises(RobotCommandException):
            self.assertIsNone(self.saved_poses.save_pose("unittest_pose", 0.3, 0.0))
        with self.assertRaises(RobotCommandException):
            self.assertIsNone(self.saved_poses.save_pose("unittest_pose",  0.3, 0.0, 0.3, 0.0, 1.57, 0.0, 0.0))
        with self.assertRaises(RobotCommandException):
            self.assertIsNone(self.saved_poses.save_pose("unittest_pose", [0.1]*8))
        with self.assertRaises(RobotCommandException):
            self.assertIsNone(self.saved_poses.save_pose("unittest_pose", [0.1]*4))

        self.assertFalse("unittest_pose" in self.saved_poses.get_saved_pose_list())


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestSavedPoses(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
