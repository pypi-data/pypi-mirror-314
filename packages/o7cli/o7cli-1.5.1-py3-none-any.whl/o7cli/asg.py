#!/usr/bin/env python
# ************************************************************************
# Copyright 2021 O7 Conseils inc (Philippe Gosselin)
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
#
# ************************************************************************
"""Module allows to view and access Auto-Scaling Groups"""

# --------------------------------
#
# --------------------------------
import logging
import pprint

import o7util.menu as o7m
from o7util.table import ColumnParam, Table, TableParam

from o7cli.base import Base

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class Asg(Base):
    """Class for Auto Scaling Groups for a Profile & Region"""

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autoscaling = self.session.client("autoscaling")
        self.asgs = None

    # *************************************************
    #
    # *************************************************
    def load_asg(self):
        """Returns all Auto-Scaling Groups for this region"""

        logger.info("load_asg")

        paginator = self.autoscaling.get_paginator("describe_auto_scaling_groups")
        self.asgs = []
        param = {}

        for page in paginator.paginate(**param):
            self.asgs.extend(page.get("AutoScalingGroups", []))

        logger.info(f"load_asg: Number of Instances found {len(self.asgs)}")

        return self.asgs

    # *************************************************
    #
    # *************************************************
    def display_asgs(self):
        """Displays a summary of ASGs in a Table Format"""

        self.load_asg()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="AutoScalingGroupName"),
                ColumnParam(title="Min", type="str", data_col="MinSize"),
                ColumnParam(title="Max", type="str", data_col="MaxSize"),
                ColumnParam(title="Desired", type="str", data_col="DesiredCapacity"),
                ColumnParam(title="Instances", type="str", data_col="InstancesCount"),
                ColumnParam(
                    title="Status", type="str", data_col="Status", format="aws-state"
                ),
            ]
        )

        print()
        Table(params, self.asgs).print()

    # *************************************************
    #
    # *************************************************
    def display_asg(self, index):
        """Display a single ASG"""
        if 0 < index <= len(self.asgs):
            print(f"Printing Raw for asg id: {index}")
            pprint.pprint(self.asgs[index - 1])

    # *************************************************
    #
    # *************************************************
    def menu(self):
        """Menu to view and edit all ASGs in current region"""

        obj = o7m.Menu(
            exit_option="b",
            title="Auto Scaling Groups",
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(key="r", name="Raw", callback=lambda: pprint.pprint(self.asgs))
        )

        obj.add_option(
            o7m.Option(key="int", name="Details for a ASG", callback=self.display_asg)
        )

        obj.display_callback = self.display_asgs
        obj.loop()


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    Asg(**kwargs).menu()


# *************************************************
# For Quick Testing
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    # print()

    asg_obj = Asg()
    # obj.load_asg()
    # obj.display_asgs()
    asg_obj.menu()

    # .MenuAutoScalingGroups()
