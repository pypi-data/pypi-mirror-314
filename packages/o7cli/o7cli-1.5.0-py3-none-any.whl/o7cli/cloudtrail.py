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
"""Module for AWS CloudTrail"""

# --------------------------------
#
# --------------------------------
import logging

import o7util.report

from o7cli.base import Base

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class Cloudtrail(Base):
    """Class for AWS CloudTrail"""

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cloudtrail = self.session.client("cloudtrail")

    # *************************************************
    #
    # *************************************************
    def conformity_report(self, report: o7util.report.Report = None):
        """Conformity Report"""

        if report is None:
            report = o7util.report.Report(
                "Account Conformity Report", section_name="Cloud Trail"
            )
        else:
            report.add_section("Cloud Trail")

        resp = self.cloudtrail.describe_trails()
        # pprint.pprint(resp)

        report.add_test(name="Global Trail present for account", critical=True)

        trailist = resp.get("trailList", [])

        if len(trailist) < 1:
            report.test_fail(
                "No Trails for this account (recommend name: account-global-trail)"
            )
            return False

        # pprint.pprint(trailist)

        global_trail = None
        for trail in resp["trailList"]:
            if (
                trail["IsMultiRegionTrail"] is True
                and trail["IncludeGlobalServiceEvents"] is True
            ):
                global_trail = trail

        if global_trail is None:
            report.test_fail("No Global Trail found for this account")
            return False

        report.test_pass(f'{global_trail["Name"]}')

        report.add_test(
            name="S3 bucket into which CloudTrail delivers your trail files",
            critical=True,
        )
        if "S3BucketName" in global_trail:
            report.test_pass(global_trail["S3BucketName"])

        if not global_trail.get("IsOrganizationTrail", False):
            report.add_test(name="Cloudwatch where logs are delivered", critical=True)
            if "CloudWatchLogsLogGroupArn" in global_trail:
                report.test_pass(global_trail["CloudWatchLogsLogGroupArn"])

        report.add_test(name="Log file validation is enabled", critical=True)
        if global_trail["LogFileValidationEnabled"] is True:
            report.test_pass()

        report.test_fail()

        return True


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    Cloudtrail().conformity_report()
