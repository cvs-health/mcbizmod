# Copyright 2022 CVS Health and/or one of its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mcbizmod as mc
import numpy as np
import unittest
from dataclasses import dataclass, field


class TestDistP(unittest.TestCase):
    samples: np.ndarray = field(default_factory=lambda: np.array([0, 1, 2]))
    samples_mean: np.float64 = field(default_factory=lambda: 0)
    samples_median: np.float64 = field(default_factory=lambda: 0)
    samples_std: np.float64 = field(default_factory=lambda: 0)
    samples_percentiles: list = field(default_factory=lambda: [0])
    
    def test_name(self):
        dist = mc.DistP()
        self.assertIsInstance(dist.name, str, 'Name should be a string.')
        
    def test_lever(self):
        dist = mc.DistP()
        self.assertIsInstance(dist.lever, str, 'Lever should be a string.')

    def test_segment(self):
        dist = mc.DistP()
        self.assertIsInstance(dist.segment, str, 'Segment should be a string.')
        
    def test_distfunc(self):
        dist = mc.DistP()
        self.assertIsInstance(dist.distfunc, object, 'Distfunc should be an object.')
        
    def test_bounds(self):
        dist = mc.DistP()
        self.assertIsInstance(dist.segment, str, 'Bounds should be a list.')
        self.assertIsInstance(dist.bound_method, str, 'Bounds Method should be a string.')
        
    def test_size(self):
        dist = mc.DistP()
        self.assertIsInstance(dist.size, int, 'Size should be an int.')
        
    def test_samples(self):
        dist = mc.DistP()
        self.assertIsInstance(dist.samples, np.ndarray, 'Samples should be a np.ndarray.')
        self.assertIsInstance(dist.samples_mean, np.float64, 'Samples Mean should be a np.float64.')
        self.assertIsInstance(dist.samples_median, np.float64, 'Samples Median should be a np.float64.')
        self.assertIsInstance(dist.samples_std, np.float64, 'Samples STD should be a np.float64.')
        self.assertIsInstance(dist.samples_percentiles, list, 'Samples Percentiles should be a list.')

        
if __name__ == '__main__':
    unittest.main()
