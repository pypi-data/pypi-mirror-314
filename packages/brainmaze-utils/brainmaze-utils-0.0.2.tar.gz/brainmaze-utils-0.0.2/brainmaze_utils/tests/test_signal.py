# Copyright 2020-present, Mayo Clinic Department of Neurology
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


import unittest
from unittest import TestCase
from brainmaze_utils.files import *

basedir = os.path.abspath(os.path.dirname(__file__))

class TestSignal(TestCase):
    def test_import(self):
        print("Testing import 'from brainmaze_utils.signal'")


if __name__ == '__main__':
    unittest.main()
