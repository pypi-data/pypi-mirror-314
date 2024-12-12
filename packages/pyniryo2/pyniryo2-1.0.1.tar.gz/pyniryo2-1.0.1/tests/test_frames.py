#!/usr/bin/env python
import unittest
from threading import Event
import numpy as np

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.niryo_ros import NiryoRos
from pyniryo2.objects import PoseObject

from pyniryo2.frames.frames import Frames
from pyniryo2.arm.arm import Arm

robot_ip_address = "127.0.0.1"
port = 9090

test_order = ["test_creation_edition_frame",
              "test_move_in_frame",
              "test_deletion"
              ]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = NiryoRos(ip_address=robot_ip_address, port=port)
        cls.frames = Frames(cls.client)
        cls.arm = Arm(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.arm.go_to_sleep()
        #cls.client.close()

    @staticmethod
    def assertAlmostEqualVector(a, b, decimal=1):
        np.testing.assert_almost_equal(a, b, decimal)

# noinspection PyTypeChecker


class TestFrames(BaseTest):
    robot_poses = [[
        [0.2, 0.2, 0.1, 0, 0, 0],
        [0.4, 0.3, 0.1, 0, 0, 0],
        [0.3, 0.4, 0.1, 0, 0, 0]
    ],
        [
        [-0.2, -0.2, 0.1, 0, 0, 0],
        [-0.4, -0.3, 0.1, 0, 0, 0],
        [-0.3, -0.4, 0.1, 0, 0, 0],
    ]
    ]

    robot_point = [[
        [-0.2, 0.2, 0.1],
        [0.4, 0.3, 0],
        [0.3, 0.4, 0]
    ],
        [
        [0.2, -0.2, 0.1],
        [-0.4, -0.3, 0],
        [-0.3, -0.4, 0]
    ]
    ]

    def test_creation_edition_frame(self):
        base_dict =  self.frames.get_saved_dynamic_frame_list()
        new_base_dict = base_dict.copy()

        # Create frame by poses
        list_saved = []
        for i in range(4):
            if (i < 2):
                # Test creation by poses
                new_name = 'unitTestFramePose_{:03d}'.format(i)
                new_desc = 'descTestFramePose_{:03d}'.format(i)
                pose_o = self.robot_poses[i][0]
                pose_x = self.robot_poses[i][1]
                pose_y = self.robot_poses[i][2]
                self.assertIsNone(self.frames.save_dynamic_frame_from_poses(new_name, new_desc, pose_o, pose_x, pose_y))

                # Test edition
                new_edit_name = 'unitEditTestFramePose_{:03d}'.format(i)
                new_edit_desc = 'descEditTestFramePose_{:03d}'.format(i)
                self.assertIsNone(self.frames.edit_dynamic_frame(new_name, new_edit_name, new_edit_desc))
                self.assertEqual(self.frames.get_saved_dynamic_frame(new_edit_name).description, new_edit_desc)

                with self.assertRaises(RobotCommandException):
                    self.frames.get_saved_dynamic_frame(0)


                new_base_dict[new_edit_name] = new_edit_desc

                self.assertEqual(self.frames.get_saved_dynamic_frame_list(), new_base_dict)

                with self.assertRaises(RobotCommandException):
                    self.frames.save_dynamic_frame_from_poses(0, "unittest", pose_o, pose_x, pose_y)

                with self.assertRaises(RobotCommandException):
                    self.frames.save_dynamic_frame_from_points(0, "unittest", pose_o, pose_x, pose_y)

                with self.assertRaises(RobotCommandException):
                    self.frames.edit_dynamic_frame("unitTestFramePose_000", 0, 0)

            else:
                # Test creation by points
                new_name = 'unitTestFramePose_{:03d}'.format(i)
                new_desc = 'descTestFramePose_{:03d}'.format(i)
                point_o = self.robot_point[2-i][0]
                point_x = self.robot_point[2-i][1]
                point_y = self.robot_point[2-i][2]
                self.assertIsNone(self.frames.save_dynamic_frame_from_points(new_name, new_desc, point_o, point_x, point_y))

                # Test edition
                new_edit_name = 'unitEditTestFramePose_{:03d}'.format(i)
                new_edit_desc = 'descEditTestFramePose_{:03d}'.format(i)
                self.assertIsNone(self.frames.edit_dynamic_frame(new_name, new_edit_name, new_edit_desc))
                self.assertEqual(self.frames.get_saved_dynamic_frame(new_edit_name)[1], new_edit_desc)

                new_base_dict[new_edit_name] = new_edit_desc

                self.assertEqual(self.frames.get_saved_dynamic_frame_list(), new_base_dict)

    def test_move_in_frame(self):
        # Move frame 000
        pose0 = (0, 0, 0, 0, 1.57, 0)
        self.assertIsNone(self.arm.move_pose(pose0, "unitEditTestFramePose_000"))
        self.assertIsNone(self.arm.move_linear_pose((0.05, 0.05, 0.05, 0, 1.57, 0), "unitEditTestFramePose_000"))

        # Move frame 001
        pose1 = PoseObject(0, 0, 0, 0, 1.57, 0)
        self.assertIsNone(self.arm.move_pose(pose1, "unitEditTestFramePose_001"))
        self.assertIsNone(self.arm.move_linear_pose((0.05, 0.05, 0.05, 0, 1.57, 0), "unitEditTestFramePose_001"))

        # Move frame 002
        pose2 = (0, 0, 0, 0, 1.57, 0)
        self.assertIsNone(self.arm.move_pose(pose2, "unitEditTestFramePose_002"))
        self.assertIsNone(self.arm.move_relative([0.05, 0.05, 0.05, 0.1, 0.1, 0.1], "unitEditTestFramePose_002"))
        self.assertIsNone(self.arm.move_linear_relative([-0.05, -0.05, -0.05, 0, 0, 0], "unitEditTestFramePose_002"))

        # Move frame 003
        pose3 = PoseObject(0, 0, 0, 0, 1.57, 0)
        self.assertIsNone(self.arm.move_pose(pose3, "unitEditTestFramePose_003"))
        self.assertIsNone(self.arm.move_relative([0.05, 0.05, 0.05, 0.1, 0.1, 0.1], "unitEditTestFramePose_003"))
        self.assertIsNone(self.arm.move_linear_relative([-0.05, -0.05, -0.05, 0, 0, 0], "unitEditTestFramePose_003"))

        # Test default world
        self.assertIsNone(self.arm.move_linear_relative([0.1, 0.1, 0.1, 0, 0, 0]))
        self.assertIsNone(self.arm.move_linear_relative([0, 0, -0.1, 0, 0, 0]))

        with self.assertRaises(RobotCommandException):
            self.arm.move_relative([0.05, 0.05, 0.05, 0.1, 0.1, 0.1], 0)

        with self.assertRaises(RobotCommandException):
            self.arm.move_linear_relative([0.05, 0.05, 0.05, 0.1, 0.1, 0.1], 0)

    def test_deletion(self):
        base_dict = self.frames.get_saved_dynamic_frame_list()
        new_base_dict = base_dict.copy()

        for i in range(4):
            name_delete = 'unitEditTestFramePose_{:03d}'.format(i)
            self.assertIsNone(self.frames.delete_saved_dynamic_frame(name_delete))

            new_base_dict.pop(name_delete)

            self.assertEqual(self.frames.get_saved_dynamic_frame_list(), new_base_dict)


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestFrames(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
