"""Module to explore AWS costs"""

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

# --------------------------------
#
# --------------------------------
import datetime
import logging

import botocore.exceptions
import o7util.input
import o7util.report
import pandas as pd

import o7cli.cloudwatch
import o7cli.organizations
from o7cli.base import Base

pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class CostExplorer(Base):
    """Class to Explore AWS costs"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cost_explorer = self.session.client(
            "ce",
            config=botocore.config.Config(connect_timeout=5, retries={"max_attempts": 0}),
        )

        self.df_accounts = None
        self.tags = None

        self.common_filter = {
            "And": [
                {
                    "Not": {
                        "Dimensions": {
                            "Key": "RECORD_TYPE",
                            "Values": ["Credit", "Refund"],
                            "MatchOptions": ["EQUALS"],
                        }
                    }
                },
                {
                    "Not": {
                        "Dimensions": {
                            "Key": "SERVICE",
                            "Values": ["Tax"],
                            "MatchOptions": ["EQUALS"],
                        }
                    }
                },
            ]
        }

        self.group_type: str = None
        self.group_key: str = None
        self.filters: list = []

        self.df_costs: pd.DataFrame = None
        self.df_costs_summarize: pd.DataFrame = None

    # *************************************************
    #
    # *************************************************
    def conformity_report(self, report: o7util.report.Report = None):
        """Generate a conformity report section"""

        section_name = "Cost Explorer & Billing"
        if report is None:
            report = o7util.report.Report(
                "Account Conformity Report", section_name=section_name
            )
        else:
            report.add_section(section_name)

        o7cli.cloudwatch.Cloudwatch(session=self.session).report_alarm_sns_email(
            report,
            name="Billing",
            namespace="AWS/Billing",
            metric_name="EstimatedCharges",
        )

        report.add_test(name="Cost Explorer Status", critical=True)
        try:
            tags = self.load_tags()
        except botocore.exceptions.ClientError:
            report.TestFail("Not Enable in Account")
            return False

        report.test_pass("Enable")

        report.add_test(name="Cost Explorer Tag", critical=True)
        if len(tags) == 0:
            report.test_fail("No Tags Found")
            return False

        report.test_pass(f"Found {len(tags)} Tags")

        report.add_test(name="Tag PROJECT created", critical=False)
        if "PROJECT" in tags:
            report.test_pass()

        report.test_fail()

        return True

    # *************************************************
    #
    # *************************************************
    def load_tags(self):
        """Load cost of tags"""

        if self.tags is not None:
            return self.tags

        # print(f"Getting AWS Cost Tags")
        now = datetime.datetime.now()
        date_start = (now - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        date_end = now.strftime("%Y-%m-%d")

        self.tags = []
        param = {
            "TimePeriod": {"Start": date_start, "End": date_end},
        }
        response = self.cost_explorer.get_tags(**param)

        self.tags.extend(response.get("Tags", []))

        return self.tags
