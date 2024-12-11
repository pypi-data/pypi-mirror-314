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
"""Module for AWS Guardduty"""

# --------------------------------
#
# --------------------------------
import logging

import o7util.report

import o7cli.eventbridge
from o7cli.base import Base

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class Guardduty(Base):
    """Class for AWS Guardduty"""

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.guardduty = self.session.client("guardduty")

    # *************************************************
    #
    # *************************************************
    def conformity_report(self, report: o7util.report.Report = None):
        """Conformity Report"""

        if report is None:
            report = o7util.report.Report(
                "Account Conformity Report", section_name="Guard Duty"
            )
        else:
            report.add_section("Guard Duty")

        resp = self.guardduty.list_detectors()

        report.add_test(name="Detector present for account", critical=True)

        if "DetectorIds" not in resp:
            report.test_fail("No DetectorIds in record")
            return False

        if len(resp["DetectorIds"]) < 1:
            report.test_fail("No Detector for this account")
            return False

        if len(resp["DetectorIds"]) > 1:
            report.test_fail("Found Multiple Detectors for this account, unexpected !")
            return False

        detector_id = resp["DetectorIds"][0]
        report.test_pass(f"id {detector_id}")

        resp = self.guardduty.get_detector(DetectorId=detector_id)
        # pprint.pprint(resp)

        report.add_test(name="Service Enable", critical=True)
        if "Status" in resp and resp["Status"] == "ENABLED":
            report.test_pass()

        sources = resp.get("DataSources", {})

        report.add_test(name="Source - CloudTrail Enable", critical=True)
        if sources.get("CloudTrail", {}).get("Status", "") == "ENABLED":
            report.test_pass()

        report.add_test(name="Source - DNSLogs Enable", critical=True)
        if sources.get("DNSLogs", {}).get("Status", "") == "ENABLED":
            report.test_pass()

        report.add_test(name="Source - FlowLogs Enable", critical=True)
        if sources.get("FlowLogs", {}).get("Status", "") == "ENABLED":
            report.test_pass()

        report.add_test(name="Source - S3Logs Enable", critical=True)
        if sources.get("S3Logs", {}).get("Status", "") == "ENABLED":
            report.test_pass()

        report.add_test(name="Source - EC2 Malware Protection", critical=True)
        if (
            sources.get("MalwareProtection", {})
            .get("ScanEc2InstanceWithFindings", {})
            .get("EbsVolumes", {})
            .get("Status", "")
            == "ENABLED"
        ):
            report.test_pass()

        report.add_test(name="Findings Exported to S3", critical=True)

        resp = self.guardduty.list_publishing_destinations(DetectorId=detector_id)
        # pprint.pprint(resp)

        if len(resp.get("Destinations", [])) > 0:
            for destination in resp["Destinations"]:
                if (
                    destination["DestinationType"] == "S3"
                    and destination["Status"] == "PUBLISHING"
                ):
                    report.test_pass()

        report.test_fail(
            "Not Enable (recommended S3 Name: aws-guardduty-logs-<accountId>"
        )

        report = o7cli.eventbridge.Eventbridge(
            session=self.session
        ).report_event_rule_sns_email(
            report=report,
            name="GuardDuty",
            patterns=[
                '{"source":["aws.guardduty"]}',
                '{"source":["aws.guardduty"],"detail-type":["GuardDuty Finding"]}',
            ],
        )

        # Get $ usage per Datasource
        # resp = gd.get_usage_statistics(DetectorId=d,UsageStatisticType='SUM_BY_DATA_SOURCE', UsageCriteria={'DataSources':['FLOW_LOGS','CLOUD_TRAIL','DNS_LOGS','S3_LOGS']})
        # pprint.pprint(resp)

        return True


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    Guardduty().conformity_report()
