#!/usr/bin/env python
import unittest
import numpy as np
from threading import Event

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.niryo_topic import NiryoTopic
from pyniryo2.objects import PoseObject
from pyniryo2.niryo_ros import NiryoRos

from pyniryo2.vision.vision import Vision
from pyniryo2.vision.objects import CameraInfo, ImageParameters
from pyniryo2.vision.enums import ObjectColor

robot_ip_address = "127.0.0.1"
port = 9090

test_order = ["test_camera_info",
              "test_camera_img",
              "test_image_parameters",
              "test_workspace",
              "test_target_from_rel",
              ]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = NiryoRos(ip_address=robot_ip_address, port=port)
        cls.vision = Vision(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    @staticmethod
    def assertAlmostEqualVector(a, b, decimal=1):
        np.testing.assert_almost_equal(a, b, decimal)


# noinspection PyTypeChecker
class TestVision(BaseTest):

    def test_camera_info(self):
        self.assertIsInstance(self.vision.get_camera_intrinsics, NiryoTopic)
        self.assertIsInstance(self.vision.get_camera_intrinsics(), CameraInfo)

        cam_event = Event()
        cam_event.clear()

        def camera_info_callback(cam_info):
            self.assertIsInstance(cam_info, CameraInfo)
            cam_event.set()

        self.assertIsNone(self.vision.get_camera_intrinsics.subscribe(camera_info_callback))
        self.assertTrue(cam_event.wait(10))
        self.assertIsNone(self.vision.get_camera_intrinsics.unsubscribe())

    def test_camera_img(self):
        self.assertIsInstance(self.vision.get_img_compressed, NiryoTopic)
        self.assertIsInstance(self.vision.get_img_compressed(), bytes)

        cam_event = Event()
        cam_event.clear()

        def camera_img_callback(img):
            cam_event.set()
            self.assertIsInstance(img, bytes)

        self.assertIsNone(self.vision.get_img_compressed.subscribe(camera_img_callback))
        self.assertTrue(cam_event.wait(10))
        self.assertIsNone(self.vision.get_img_compressed.unsubscribe())

    def test_image_parameters(self):
        self.assertIsInstance(self.vision.get_image_parameters, NiryoTopic)
        self.assertIsInstance(self.vision.get_image_parameters(), ImageParameters)

        img_param_event = Event()
        img_param_event.clear()

        def img_param_callback(img_param):
            self.assertIsInstance(img_param, ImageParameters)
            img_param_event.set()

        self.assertIsNone(self.vision.get_image_parameters.subscribe(img_param_callback))
        self.assertTrue(img_param_event.wait(10))
        self.assertIsNone(self.vision.get_image_parameters.unsubscribe())

        old_img_param = self.vision.get_image_parameters.value
        for i, function in enumerate(
                [self.vision.set_brightness, self.vision.set_contrast, self.vision.set_saturation]):

            new_value = old_img_param[i] + 1.0
            self.assertIsNone(function(new_value))
            self.assertEqual(self.vision.get_image_parameters()[i], new_value)
            self.assertIsNone(function(1))
            self.assertEqual(self.vision.get_image_parameters()[i], 1)

            with self.assertRaises(RobotCommandException):
                function("1")

            with self.assertRaises(RobotCommandException):
                function(True)

    def test_workspace(self):
        ws_name = "unit_test_ws"
        self.assertIsNone(self.vision.delete_workspace(ws_name))

        unit_test_ws_poses = [ws_name,
                              [0.3, -0.1, 0.0, 0.0, 1.57, 0.0],
                              PoseObject(0.3, 0.1, 0.0, 0.0, 1.57, 0.0),
                              PoseObject(0.1, 0.1, 0.0, 0.0, 1.57, 0.0),
                              [0.1, -0.1, 0.0, 0.0, 1.57, 0.0]]

        unit_test_ws_points = [ws_name,
                               [0.3, -0.1, 0.0],
                               [0.3, 0.1, 0.0],
                               [0.2, 0.1, 0.0],
                               [0.2, -0.1, 0.0]]

        self.assertIsNone(self.vision.save_workspace_from_robot_poses(*unit_test_ws_poses))
        self.assertTrue(ws_name in self.vision.get_workspace_list())
        self.assertAlmostEquals(self.vision.get_workspace_ratio(ws_name), 1.0, places=2)
        # with self.assertRaises(RobotCommandException):
        #     self.vision.save_workspace_from_robot_poses(*unit_test_ws_poses)

        self.assertIsNone(self.vision.delete_workspace(ws_name))
        self.assertFalse(ws_name in self.vision.get_workspace_list())

        self.assertIsNone(self.vision.save_workspace_from_points(*unit_test_ws_points))
        self.assertTrue(ws_name in self.vision.get_workspace_list())
        self.assertAlmostEquals(self.vision.get_workspace_ratio(ws_name), 2.0, places=2)

        test_poses = self.vision.get_workspace_poses(ws_name)
        for pose_obtained, pose_expected in zip(test_poses, unit_test_ws_poses[0:]):
            self.assertAlmostEqualVector(pose_obtained, pose_expected.to_list()[:3], decimal=3)

        self.assertIsNone(self.vision.delete_workspace(ws_name))
        self.assertFalse(ws_name in self.vision.get_workspace_list())

    def test_target_from_rel(self):
        ws_name = "unit_test_ws"
        self.assertIsNone(self.vision.delete_workspace(ws_name))

        unit_test_ws_points = [ws_name,
                               [0.3, -0.1, 0.0],
                               [0.3, 0.1, 0.0],
                               [0.1, 0.1, 0.0],
                               [0.1, -0.1, 0.0]]

        self.assertIsNone(self.vision.save_workspace_from_points(*unit_test_ws_points))
        self.assertTrue(ws_name in self.vision.get_workspace_list())
        pose = self.vision.get_target_pose_from_rel(ws_name, 0.0, 0.5, 0.5, 0.0)
        self.assertIsInstance(pose, PoseObject)
        self.assertAlmostEqualVector(pose.to_list()[:3], [0.2, 0.0, 0.0])

        pose = self.vision.get_target_pose_from_rel(ws_name, 0.0, 0.0, 0.0, 0.0)
        self.assertIsInstance(pose, PoseObject)
        self.assertAlmostEqualVector(pose.to_list()[:3], unit_test_ws_points[1])

        pose = self.vision.get_target_pose_from_rel(ws_name, .10, 1.0, 1., 0.0)
        self.assertIsInstance(pose, PoseObject)
        expected_pose = unit_test_ws_points[-2][:]
        expected_pose[2] -= 0.1
        self.assertAlmostEqualVector(pose.to_list()[:3], expected_pose)

        self.assertIsNone(self.vision.delete_workspace(ws_name))


#
#
# @unittest.skipUnless(simulation, "Vision test is only coded for Gazebo")
# class TestVision(BaseTestTcpApi):
#     workspace_name = "gazebo_1"
#     workspace_h = 0.001
#     point_1 = [0.3369, 0.087, workspace_h]
#     point_2 = [point_1[0], -point_1[1], workspace_h]
#     point_3 = [0.163, -point_1[1], workspace_h]
#     point_4 = [point_3[0], point_1[1], workspace_h]
#
#     def setUp(self):
#         super(TestVision, self).setUp()
#         self.assertIsNone(self.niryo_robot.move_joints(0.0, 0.0, 0.0, 0.0, -1.57, 0.0))
#         self.assertIsNone(self.niryo_robot.update_tool())
#         self.assertIsNone(self.niryo_robot.save_workspace_from_points(
#             self.workspace_name, self.point_1, self.point_2, self.point_3, self.point_4))
#
#     def tearDown(self):
#         self.assertIsNone(self.niryo_robot.delete_workspace(self.workspace_name))
#         super(TestVision, self).tearDown()
#
#     def test_vision_detect(self):
#         # Getting img compressed & calibration object
#         self.assertIsNotNone(self.niryo_robot.get_img_compressed())
#         self.assertIsNotNone(self.niryo_robot.get_camera_intrinsics())
#
#         # Getting target pose's from multiple ways
#         self.assertIsNotNone(self.niryo_robot.get_target_pose_from_rel(
#             self.workspace_name, 0.1, 0.5, 0.5, 0.0))
#
#         self.assertIsNotNone(self.niryo_robot.get_target_pose_from_cam(
#             self.workspace_name, 0.1, ObjectShape.ANY, ObjectColor.ANY))
#
#         self.assertIsNotNone(self.niryo_robot.detect_object(self.workspace_name, ObjectShape.ANY, ObjectColor.RED))
#
#     def test_vision_move(self):
#         # Test to move to the object
#         self.assertIsNotNone(self.niryo_robot.move_to_object(self.workspace_name, 0.1,
#                                                              ObjectShape.ANY, ObjectColor.GREEN))
#         # Going back to observation pose
#         self.assertIsNone(self.niryo_robot.move_joints(0.0, 0.0, 0.0, 0.0, -1.57, 0.0))
#         # Vision Pick
#         self.assertIsNotNone(self.niryo_robot.vision_pick(self.workspace_name, 0.1,
#                                                           ObjectShape.ANY, ObjectColor.BLUE))
#


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestVision(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
