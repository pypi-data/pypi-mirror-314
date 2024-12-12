#!/usr/bin/env python
import unittest
from threading import Event
import numpy as np
import time

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.niryo_ros import NiryoRos
from pyniryo2.objects import PoseObject

from pyniryo2.trajectories.trajectories import Trajectories
from pyniryo2.arm.arm import Arm
from pyniryo2.objects import PoseObject
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Int32, Bool, Header

robot_ip_address = "127.0.0.1"
port = 9090

test_order = ["test_creation_delete_trajectory",
              "test_last_learned_trajectory",
              "test_execute_trajectory",
              "test_execute_trajectory_type",
              "test_execute_registered_trajectory"
              ]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = NiryoRos(ip_address=robot_ip_address, port=port)
        cls.trajectories = Trajectories(cls.client)
        cls.arm = Arm(cls.client)

    @classmethod
    def tearDownClass(cls):
        pass
        # cls.arm.go_to_sleep()
        # cls.client.close()

    @staticmethod
    def assertAlmostEqualVector(a, b, decimal=1):
        np.testing.assert_almost_equal(a, b, decimal)

    def assertEqualUnsortedList(self, a, b):
        a_sorted = a[:]
        a_sorted.sort()
        b_sorted = b[:]
        b_sorted.sort()
        self.assertEqual(a_sorted, b_sorted)


# noinspection PyTypeChecker
class TestTrajectories(BaseTest):
    trajectory = [[-0.493, -0.32, -0.505, -0.814, -0.282, 0],
                  [0.834, -0.319, -0.466, 0.822, -0.275, 0],
                  [1.037, -0.081, 0.248, 1.259, -0.276, 0]]

    robot_poses = [[0.3, 0.1, 0.3, 0., 0., 0., 1.],
                   [0.3, -0.1, 0.3, 0., 0., 0., 1.],
                   [0.3, -0.1, 0.4, 0., 0., 0., 1.],
                   [0.3, 0.1, 0.4, 0., 0., 0., 1.]]

    neutral_pose = [0.288, -0.015, 0.441, 0.035, -0.05, -0.05]

    def go_to_neutral_pose(self):
        self.assertIsNone(self.arm.move_pose(self.neutral_pose))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), self.neutral_pose)

    def test_creation_delete_trajectory(self):
        self.assertIsNone(self.trajectories.clean_trajectory_memory())
        # Get saved trajectory list & copy it
        result = self.trajectories.get_saved_trajectory_list()
        self.assertIsInstance(result, list)
        traj_list = self.trajectories.get_saved_trajectory_list()

        # Create new trajectories
        for i in range(3):
            new_name = 'unittest_{:03d}'.format(i)
            new_description = 'unittest_description_{:03d}'.format(i)
            self.assertIsNone(self.trajectories.save_trajectory(self.trajectory, new_name, new_description))
            self.assertEqualUnsortedList(self.trajectories.get_saved_trajectory(new_name), self.trajectory)
            if new_name not in [traj[0] for traj in traj_list]:
                traj_list.append((new_name, new_description))

            result = self.trajectories.get_saved_trajectory_list()
            self.assertEqualUnsortedList(result, traj_list)

        # Update trajectories
        old_names = list([traj[0] for traj in traj_list])
        for i in range(3):
            old_name = 'unittest_{:03d}'.format(i)
            new_name = 'unittest_update_{:03d}'.format(i)
            new_description = 'unittest_update_description_{:03d}'.format(i)
            self.assertIsNone(self.trajectories.update_trajectory_infos(old_name, new_name, new_description))
            self.assertEqualUnsortedList(self.trajectories.get_saved_trajectory(new_name), self.trajectory)
            try:
                name_index = old_names.index(old_name)
                traj_list[name_index] = (new_name, new_description)
            except ValueError:
                pass

            result = self.trajectories.get_saved_trajectory_list()
            self.assertEqualUnsortedList(result, traj_list)

        # Delete created trajectories
        old_names = list([traj[0] for traj in traj_list])
        for i in range(3):
            traj_name = 'unittest_update_{:03d}'.format(i)
            old_names.remove(traj_name)

            self.assertIsNone(self.trajectories.delete_trajectory(traj_name))
            time.sleep(1.0)
            result = self.trajectories.get_saved_trajectory_list()
            self.assertListEqual([traj[0] for traj in result], old_names)

            with self.assertRaises(RobotCommandException):
                self.trajectories.delete_trajectory(traj_name)

    def test_last_learned_trajectory(self):
        for i in range(3):
            new_name = 'unittest_{:03d}'.format(i)
            new_description = 'unittest_description_{:03d}'.format(i)
            self.assertIsNone(self.trajectories.save_trajectory(self.trajectory, new_name, new_description))

        self.assertIsNone(self.trajectories.clean_trajectory_memory())
        self.assertEqual(self.trajectories.get_saved_trajectory_list(), [])

        self.assertIsNone(self.trajectories.save_trajectory(self.trajectory, "last_executed_trajectory", ""))
        self.assertIsNone(self.trajectories.save_last_learned_trajectory("unittest_name", "unittest_description"))

        result = self.trajectories.get_saved_trajectory_list()
        self.assertEqual(result, [("unittest_name", "unittest_description")])
        self.assertIsNone(self.trajectories.clean_trajectory_memory())
        self.assertEqual(self.trajectories.get_saved_trajectory_list(), [])

    def test_execute_trajectory(self):
        # Testing trajectory from poses
        self.assertIsNone(self.arm.calibrate_auto())
        self.go_to_neutral_pose()
        self.assertIsNone(self.trajectories.execute_trajectory_from_poses(self.robot_poses))
        self.assertAlmostEqualVector(self.arm.get_pose().quaternion_pose, self.robot_poses[-1])

        trajectory_event = Event()
        trajectory_event.clear()

        def trajectory_callback(_):
            trajectory_event.set()

        self.go_to_neutral_pose()
        self.assertIsNone(
            self.trajectories.execute_trajectory_from_poses(self.robot_poses, dist_smoothing=0.05,
                                                            callback=trajectory_callback))
        self.assertTrue(trajectory_event.wait(20))
        self.assertAlmostEqualVector(self.arm.get_pose().quaternion_pose, self.robot_poses[-1])

    def test_execute_trajectory_type(self):
        self.assertIsNone(self.arm.calibrate_auto())
        self.go_to_neutral_pose()
        self.trajectories.execute_trajectory_from_poses([[0.3, 0.1, 0.3, 0., 0., 0., 1.],
                                                         PoseObject(0.3, -0.1, 0.3, 0., 0., 0.),
                                                         [0.3, -0.1, 0.4, 0., 0., 0.],
                                                         PoseObject(0.3, 0.1, 0.4, 0., 0., 0.)])
        self.assertAlmostEqualVector(self.arm.get_pose().quaternion_pose, self.robot_poses[-1])

        with self.assertRaises(RobotCommandException):
            self.trajectories.execute_trajectory_from_poses(0)

        with self.assertRaises(RobotCommandException):
            self.trajectories.execute_trajectory_from_poses(PoseObject(0, 0, 0, 0, 0, 0))

        with self.assertRaises(RobotCommandException):
            self.trajectories.execute_trajectory_from_poses([0.3, 0.1, 0.3, 0., 0., 0., 1.])

        with self.assertRaises(RobotCommandException):
            self.trajectories.execute_trajectory_from_poses([[0.3, 0.1, 0.3, 0., 0.]])

        with self.assertRaises(RobotCommandException):
            self.trajectories.execute_trajectory_from_poses(self.robot_poses, dist_smoothing=-0.1)

    def test_execute_registered_trajectory(self):
        # Testing trajectory from poses
        self.assertIsNone(self.arm.calibrate_auto())

        trajectory_event = Event()
        trajectory_event.clear()

        def trajectory_callback(_):
            trajectory_event.set()

        # Create & save a trajectory, then execute it & eventually delete it
        traj_name = "test_trajectory_save_and_execute_registered"
        traj_description = "test_trajectory_save_and_execute_registered_description"
        # self.go_to_neutral_pose()
        self.assertIsNone(self.trajectories.save_trajectory(self.trajectory, traj_name, traj_description))
        self.assertIsNone(self.trajectories.execute_registered_trajectory(traj_name, callback=trajectory_callback))

        trajectory_event.clear()
        self.assertIsNone(self.arm.move_pose(self.neutral_pose))
        self.assertIsNone(self.trajectories.delete_trajectory(traj_name))

        with self.assertRaises(RobotCommandException):
            self.assertIsNone(self.trajectories.execute_registered_trajectory(traj_name))


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestTrajectories(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
