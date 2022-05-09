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

from setuptools import setup

setup(name='mcbizmod',
      version='0.0.1',
      description='Distribution-based business cases.',
      url='https://github.com/cvs-health/mcbizmod',
      author='Eugenio Zuccarelli, Eli Goldberg',
      author_email='eugenio.zuccarelli@gmail.com, zuccarellie@aetna.com, goldberge@cvshealth.com',
      packages=['mcbizmod'],
      zip_safe=False,
      install_requires=[
          'pandas', 'numpy', 'datetime', 'scipy', 'seaborn', 'matplotlib',
          'seaborn_qqplot', 'plotly'
      ],
      include_package_data=True,
      package_data={'': ['data/*.csv']})
