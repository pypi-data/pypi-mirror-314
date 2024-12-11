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
"""Module for AWS Reports"""

# --------------------------------
#
# --------------------------------
import logging

import o7util.report

import o7cli.cloudtrail
import o7cli.costexplorer
import o7cli.guardduty
import o7cli.iam
import o7cli.sts
from o7cli.base import Base

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class Report(Base):
    """Class for AWS Reports"""

    # *************************************************
    #
    # *************************************************
    def __init__(self, profile=None, region=None, session=None):
        super().__init__(profile=profile, region=region, session=session)

    # *************************************************
    #
    # *************************************************
    def conformity(self):
        """Conformity Report"""

        report = o7util.report.Report(f"Account Conformity Report - {self.title_line()}")
        report.add_parameter(
            name="Account Id",
            value=o7cli.sts.Sts(session=self.session).get_account_id(),
        )

        o7cli.iam.IAM(session=self.session).conformity_report(report=report)
        o7cli.cloudtrail.Cloudtrail(session=self.session).conformity_report(report=report)
        o7cli.guardduty.Guardduty(session=self.session).conformity_report(report=report)
        o7cli.costexplorer.CostExplorer(session=self.session).conformity_report(
            report=report
        )

        report.complete()

        # TO DO
        # Pager is there

        return True

    # *************************************************
    # TBR
    # *************************************************
    def run(self, report_name: str):
        """Run a report"""

        if report_name == "conformity":
            self.conformity()
        else:
            print(f"Unknown Report Name: {report_name}")


# *************************************************
#
# *************************************************
def run_conformity(**kwargs):
    """Run Conformity Report"""
    Report(**kwargs).conformity()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    Report(profile="cw").run("conformity")
