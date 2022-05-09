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

"""
# MCBizMod
## Markov Chain Monte Carlo (MCMC)
MCMC is a sampling technique that works well in many situations.
However, this is NOT a conditional distribution (or Gibbs) sampling tool!
This is for several reasons:

1. Mostly, we don't have enough information, usually, to set an appropriate prior.

2. Where we do, we could, however, we don't know the conditional effect (i.e., paired variable covariance) on the distribution from the most critical variables, namely engagement and the treatment effect. Thus,
it's likely better to assume absolute ignorance rather than create a partially broken conditional probability chain. This mimicks typical business cases (which obviously don't use markov-chain-based distribution sampling methods).

To make this simple task a bit easier, we've built a basic dataclass constructor to track the assumptions made and make your business cases repeatable, inspectable, and (more) accurate. Or at least, wrong in a quantifiable way:).

"""
__docformat__ = "google"
import pandas as pd
from copy import deepcopy
from dataclasses import dataclass, asdict


@dataclass
class MCBizMod:
    """
    A mini business case tool.

    """
    name: str

    def __post_init__(self):
        """
        Dataclass post init setting.
        Returns:

        """
        setattr(self, 'levers', dict())
        setattr(self, 'lever_names', [])
        setattr(self, 'segment_names', [])
        setattr(self, 'bizcase', dict())

    def add_dist_params(self, markers):
        """
        Add a bunch of distribution markers

        Args:
            markers: a list of DistP objects.

        Returns:
            self

        """

        for marker in markers:
            self.add_dist_param(marker)

        return self

    def add_dist_param(self, marker):
        """
        Add a distribution parameter to the class.

        Args:
            marker: a DistP object

        Returns:
            self

        """

        # if the marker name is in the marker
        if marker.lever in self.levers.keys():
            if marker.segment in self.levers.get(marker.lever).keys():
                if marker.name in self.levers.get(marker.lever).get(marker.segment):
                    self.levers.get(marker.lever).get(marker.segment).update({marker.name: marker})
                else:
                    self.levers.get(marker.lever).get(marker.segment).update({marker.name: marker})
                    self.segment_names.append(marker.segment)

            else:
                self.levers.get(marker.lever).update({marker.segment: {marker.name: marker}})
                self.segment_names.append(marker.segment)
        else:
            self.levers.update({marker.lever: {marker.segment: {marker.name: marker}}})
            self.lever_names.append(marker.lever)
            self.segment_names.append(marker.segment)

        return self

    def value_lever(self,
                    dist_name,
                    operator,
                    lever,
                    segment='default segment',
                    label='mcs'):
        """
        Chain instantiated distributions to create an MCS distribution.
        Args:
            dist_name: the name of the distp object in the data class
            operator: One of the following '*', '/', '+', '-', or '*k'.
            label: Instantiated class attribute e.g,. 'mcs'.

        Returns:
            self

        """

        # assert that the lever exists
        assert lever in self.levers.keys()
        
        # assert that segment exists in lever
        assert segment in self.levers.get(lever).keys(), 'not in segment keys'
        
        # assert that distname exists in segment
        assert dist_name in self.levers.get(lever).get(segment).keys(), 'not in lever keys'

        if operator == 'base':
            # update bizcase with distribution.
            base_dist = deepcopy(self.levers.get(lever).get(segment).get(dist_name))
            base_dist = self.update_dist_stats(base_dist, label)
            self.bizcase.update(
                {lever: {
                    segment: {
                        label: base_dist
                    }}})

        else:
            # call biz math on base bizcase distribution with label
            base_dist = deepcopy(self.bizcase.get(lever).get(segment).get(label))
            new_dist = self.levers.get(lever).get(segment).get(dist_name)
            chain_dist = self.chain_math(base_dist=base_dist,
                                         new_dist=new_dist,
                                         operator=operator)

            chain_dist = deepcopy(chain_dist)
            chain_dist = self.update_dist_stats(chain_dist, label)

            self.bizcase.update({lever: {segment: {label: chain_dist}}})

        return self

    def update_dist_stats(self, dist, label):
        dist.update('name', label)
        dist.update_diststats()
        dist.update('kwargs', None)
        dist.update('distfunc', None)
        dist.update('bounds', None)
        dist.update('bound_method', None)
        dist.update('size_kwd', None)
        return dist

    def chain_math(self, base_dist, new_dist, operator):
        """
        Internal function to provide some syntatic sugar
        to operations on distributions
        Args:
            new_dist: Distp class
            operator: One of the following '*', '/', '+', '-', or '*k'.
            label: instantiated class attribute e.g,. 'mcs'.

        Returns:
            base_dist: the resultant operated-upon DistP object

        """

        if operator == '*':
            base_dist = base_dist.chain_mult(new_dist)
        if operator == '/':
            base_dist = base_dist.chain_divide(new_dist)
        if operator == '+':
            base_dist = base_dist.chain_add(new_dist)
        if operator == '-':
            base_dist = base_dist.chain_sub(new_dist)
        if operator == '*k':
            base_dist = base_dist.mult_const(new_dist)

        return base_dist

    def sum_over_levers_segments(self, labels, segments):
        """
        Args:
            labels: list of labels e.g., ['mcs','revenue','cost']

        Returns:
            self

        """

        for i, lever in enumerate(self.bizcase.keys()):
            for label in labels:
                for segment in segments:
                    if i == 0:
                        chain_dist = deepcopy(self.bizcase.get(lever).get(segment).get(label))

                    else:
                        base_dist = deepcopy(self.bizcase.get(lever).get(segment).get(label))
                        chain_dist = self.chain_math(base_dist=base_dist,
                                                     new_dist=chain_dist,
                                                     operator='+')

        return chain_dist

    def return_assumptions(self, drop_cols=False):
        """
        Return all the assumptions for all distributions in all levers

        Args:
            drop_cols: list, call headers you wish to
            exclude ['bound_method', 'size_kwd', 'samples']

        Returns:
            df_list: pd.DataFrame, a concat'd datafrmae

        """

        df_list = []
        for lever in self.levers.keys():
            for segment in self.levers[lever].keys():
                for dist in self.levers.get(lever).get(segment).keys():
                    dist_ob = self.levers.get(lever).get(segment).get(dist)
                    df = pd.DataFrame.from_dict(asdict(dist_ob), 
                                                orient='index').T
                    df_list.append(df)

        for lever in self.bizcase.keys():
            for segment in self.bizcase[lever].keys():
                for dist in self.bizcase.get(lever).get(segment).keys():
                    dist_ob = self.bizcase.get(lever).get(segment).get(dist)
                    df = pd.DataFrame.from_dict(asdict(dist_ob), 
                                                orient='index').T
                    df_list.append(df)

        df_list = pd.concat(df_list)

        if drop_cols:
            df_list = df_list.drop(drop_cols, axis=1)

        return df_list
