# Copyright 2020-present, Mayo Clinic Department of Neurology
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


import os
import numpy as np

from copy import deepcopy
from shutil import rmtree

import unittest
from unittest import TestCase

from brainmaze_utils.vector import get_mutual_vectors, get_rot_2d, get_rot_3d, get_rot_3d_x, get_rot_3d_y, get_rot_3d_z, rotate, \
    _rotate_3d, _rotate_2d, _check_scale, _check_dimensions, translate, scale

basedir = os.path.abspath(os.path.dirname(__file__))

class TestVector(TestCase):
    def test_import(self):
        print("Testing import 'from brainmaze_utils.vector'")


class TestCheckDimensions(unittest.TestCase):
    def test_valid_dimensions(self):
        # Test for valid dimensions (1 to 3)
        for dim in range(1, 4):
            with self.subTest(dim=dim):
                x = np.random.rand(5, dim)
                self.assertTrue(_check_dimensions(x))

    def test_invalid_dimensions_too_low(self):
        # Test for dimensions lower than 1
        x = np.random.rand(5, 0)
        with self.assertRaises(AssertionError):
            _check_dimensions(x)

    def test_invalid_dimensions_too_high(self):
        # Test for dimensions higher than 3
        x = np.random.rand(5, 4)
        with self.assertRaises(AssertionError):
            _check_dimensions(x)


class TestCheckScale(unittest.TestCase):
    def test_valid_scale(self):
        # Test for valid scale
        x = np.random.rand(5, 3)
        m = [1, 2, 3]
        self.assertTrue(_check_scale(x, m))

    def test_invalid_scale_length_mismatch(self):
        # Test for mismatch in length of scale
        x = np.random.rand(5, 3)
        m = [1, 2]
        with self.assertRaises(AssertionError):
            _check_scale(x, m)


#
# class TestTransformations(unittest.TestCase):
#     def setUp(self):
#         self.data_2d = np.array([[1, 2], [3, 4]])
#         self.data_3d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
#
#     def test_translate(self):
#         translated = translate(self.data_2d.copy(), [1, 2])
#         expected = np.array([[2, 4], [4, 6]])
#         np.testing.assert_array_equal(translated, expected)
#
#     def test_scale(self):
#         scaled = scale(self.data_2d.copy(), [1, 2])
#         expected = np.array([[0., 0.], [4., 8.]])  # Adjust expected values based on your scale logic
#         np.testing.assert_allclose(scaled, expected)

    # def test_rotate_2d(self):
    #     rotated = rotate(self.data_2d.copy(), 90)
    #     expected = np.array([[-2, 1], [-4, 3]])  # Expected results for 90-degree rotation
    #     np.testing.assert_allclose(rotated, expected, atol=1e-7)
    #
    # def test_rotate_3d(self):
    #     rotated = rotate(self.data_3d.copy(), [90, 90, 90])
    #     expected = self.data_3d  # Adjust expected values based on your 3D rotation logic
    #     np.testing.assert_allclose(rotated, expected, atol=1e-7)

if __name__ == '__main__':
    unittest.main()
