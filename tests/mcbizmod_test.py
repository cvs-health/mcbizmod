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
import unittest


class TestMCBizMod(unittest.TestCase):
    def test_lever(self):
        biz = mc.MCBizMod(name='test')
        self.assertIsInstance(biz.levers, dict, 'Lever should be a dict.')
        self.assertIsInstance(biz.lever_names, list, 'Lever Names should be a list.')
        
    def test_segments(self):
        biz = mc.MCBizMod(name='test')
        self.assertIsInstance(biz.segment_names, list, 'Segment Names should be a list.')

    def test_segments(self):
        biz = mc.MCBizMod(name='test')
        self.assertIsInstance(biz.bizcase, dict, 'Bizcase should be a dict.')
        

if __name__ == '__main__':
    unittest.main()
