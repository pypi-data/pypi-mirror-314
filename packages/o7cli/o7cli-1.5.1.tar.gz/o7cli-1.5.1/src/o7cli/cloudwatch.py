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
"""Module for AWS Cloudwatch"""

# --------------------------------
#
# --------------------------------
import logging

import o7util.report
import pandas as pd

import o7cli.sns
from o7cli.base import Base

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class Cloudwatch(Base):
    """Class for AWS Cloudwatch"""

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cw_us_east_1 = self.session.client("cloudwatch", region_name="us-east-1")
        # self.cw = self.session.client('cloudwatch')

    # *************************************************
    #
    # *************************************************
    def report_alarm_sns_email(
        self,
        report: o7util.report.Report,
        name: str,
        namespace: str = "",
        metric_name: str = "",
        minimum: int = 0,
    ):
        """Add to Report if SNS Email Subcription exist for Alarm"""

        df_alarm = self.load_alarms_us_east_1()

        # Check for Event Rule
        report.add_test(name=f"{name} Alarm Exist", critical=True)

        df_alarm = df_alarm[df_alarm["Namespace"] == namespace]
        df_alarm = df_alarm[df_alarm["MetricName"] == metric_name]

        if len(df_alarm.index) == 0:
            report.test_fail("No Alarm")
            return report

        alarm = df_alarm.iloc[0]
        alarm_name = alarm["AlarmName"]
        report.test_pass(f"Alarm name {alarm_name}")

        # Check it is enable
        report.add_test(name=f"{name} Alarm Threshold", critical=True)
        threshold = alarm["Threshold"]

        if threshold > minimum:
            report.test_pass(f"{threshold}")
        else:
            report.test_fail(f"Too Low {threshold} < {minimum}")

        # Check it is enable
        report.add_test(name=f"{name} Alarm is Enable", critical=True)
        if alarm["ActionsEnabled"] is True:
            report.test_pass()
        else:
            report.test_fail(f'State is {alarm["State"] }')

        # Check for SNS Target
        report.add_test(name=f"{name} Alarm has an SNS Target", critical=True)
        actions = alarm["AlarmActions"]
        sns_targets = [s for s in actions if "arn:aws:sns:" in s]
        if len(sns_targets) == 0:
            report.test_fail("No SNS Target")
            return report

        arn = sns_targets[0]
        report.test_pass(f"Arn {arn}")

        # Check for Active Email Subcription
        report.add_test(name=f"{name} Alarm has email subcription", critical=True)
        subs = o7cli.sns.Sns(session=self.session, region="us-east-1").load_subcriptions(
            arn
        )
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
    def load_alarms_us_east_1(self) -> pd.DataFrame:
        """Load all alarms in us-east-1"""

        # print(f"Getting All Event Rules")
        paginator = self.cw_us_east_1.get_paginator("describe_alarms")
        param = {}
        alarms = []

        for page in paginator.paginate(**param):
            alarms.extend(page.get("MetricAlarms", []))

        df_alarms = pd.DataFrame(
            alarms,
            columns=[
                "AlarmName",
                "Namespace",
                "MetricName",
                "StateValue",
                "AlarmActions",
                "Threshold",
            ],
        )
        # print(df_alarms)

        return df_alarms


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", 10)
    pd.set_option("display.width", 200)
    pd.set_option("display.max_colwidth", 20)

    r = o7util.report.Report("Account Conformity Report", section_name="CloudWatch")
    r = Cloudwatch().report_alarm_sns_email(
        r, name="Billing", namespace="AWS/Billing", metric_name="EstimatedCharges"
    )

    # alarms = LoadAlarms()

    # pprint.pprint(rules[['Name','EventPattern']])

    # pprint.pprint(rules[rules['EventPattern'] == '{"source":["aws.guardduty"]}'])
