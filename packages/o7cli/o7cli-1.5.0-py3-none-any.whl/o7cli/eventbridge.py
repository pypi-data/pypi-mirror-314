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
"""Module for AWS Eventbridge"""

# --------------------------------
#
# --------------------------------
import logging
import pprint

import o7util.report
import pandas as pd

import o7cli.sns
from o7cli.base import Base

logger = logging.getLogger(__name__)

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#cloudwatchevents


# *************************************************
#
# *************************************************
class Eventbridge(Base):
    """Class for AWS Eventbridge"""

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cwe = self.session.client("events")

    # *************************************************
    #
    # *************************************************
    def report_event_rule_sns_email(
        self, report: o7util.report.Report, name: str, patterns: list = None
    ):
        """Add to Report if SNS Email Subcription exist for Event Rule"""

        patterns = [] if patterns is None else patterns
        rules = self.load_rules()

        # Check for Event Rule
        report.add_test(name=f"{name} Event Exist", critical=True)

        gd_rule = rules[rules["EventPattern"].isin(patterns)]

        if len(gd_rule.index) == 0:
            report.test_fail("No Event Rule")
            return report

        gd_name = gd_rule.iloc[0]["Name"]
        report.test_pass(f"Rule name {gd_name}")

        # Check it is enable
        report.add_test(name=f"{name} Event Rule is Enable", critical=True)
        if gd_rule.iloc[0]["State"] == "ENABLED":
            report.test_pass()
        else:
            report.test_fail(f'State is {gd_rule.iloc[0]["State"] }')

        # Check for SNS Target
        report.add_test(name=f"{name} Event Rule has an SNS Target", critical=True)
        targets = self.load_targets(gd_name)
        sns_targets = targets[targets["Arn"].str.contains("arn:aws:sns:")]
        if len(sns_targets.index) == 0:
            report.test_fail("No SNS Target")
            return report

        arn = sns_targets.iloc[0]["Arn"]
        report.test_pass(f"Arn {arn}")

        # Check for Active Email Subcription
        report.add_test(name=f"{name} Event Rule has email subcription", critical=True)
        subs = o7cli.sns.Sns(session=self.session).load_subcriptions(arn)
        subs_email = subs[subs["Protocol"] == "email"]
        subs_email = subs_email[
            subs_email["SubscriptionArn"].str.contains("arn:aws:sns:")
        ]

        if len(subs_email.index) == 0:
            report.test_fail("No Email Subcription")
            return report

        emails = ",".join(subs_email["Endpoint"].tolist())
        report.test_pass(f"{emails}")

        return report

    # *************************************************
    #
    # *************************************************
    def load_targets(self, rule_name):
        """Load all targets for a rule"""

        # print(f"Getting Targets for Rule: {ruleName}")

        paginator = self.cwe.get_paginator("list_targets_by_rule")
        targets = []
        param = {"Rule": rule_name}

        for page in paginator.paginate(**param):
            targets.extend(page.get("Targets", []))

        return pd.DataFrame(data=targets, columns=["Id", "Arn"])

    # *************************************************
    #
    # *************************************************
    def load_rules(self) -> pd.DataFrame:
        """Load all rules"""

        # print(f"Getting All Event Rules")

        paginator = self.cwe.get_paginator("list_rules")
        rules = []
        param = {}

        for page in paginator.paginate(**param):
            rules.extend(page.get("Rules", []))

        return pd.DataFrame(data=rules, columns=["Name", "EventPattern", "Arn", "State"])


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", -1)
    pd.set_option("display.max_colwidth", None)

    # r = o7lib.util.report.Report('Account Conformity Report', sectionName="Event Bridge")
    # r = Eventbridge().ReportEventRuleSnsEmail(r, name = 'GuardDuty', patterns = ['{"source":["aws.guardduty"]}', '{"source":["aws.guardduty"],"detail-type":["GuardDuty Finding"]}'])

    the_rules = Eventbridge().load_rules()
    pprint.pprint(the_rules[["Name", "State"]])

    the_targets = Eventbridge().load_targets(rule_name="Automated-GuardDuty-Notification")
    pprint.pprint(the_targets.iloc[0])

    # pprint.pprint(rules[rules['EventPattern'] == '{"source":["aws.guardduty"]}'])
