# ************************************************************************
# Copyright 2022 O7 Conseils inc (Philippe Gosselin)
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
"""Module for AWS IAM"""

import logging
import pprint

import o7util.input
import o7util.menu as o7m
import o7util.report

from o7cli.base import Base

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class IAM(Base):
    """Class for AWS IAM"""

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.iam = self.session.client("iam")

    # *************************************************
    #
    # *************************************************
    def get_account_summary(self):
        """Get Account Summary"""
        return self.iam.get_account_summary().get("SummaryMap", {})

    # *************************************************
    #
    # *************************************************
    def get_account_password_policy(self):
        """Get Password Policy"""
        return self.iam.get_account_password_policy()

    # *************************************************
    #
    # *************************************************
    def load_users(self):
        """Get Account Summary"""

        paginator = self.iam.get_paginator("list_users")
        users = []
        param = {}

        for page in paginator.paginate(**param):
            users.extend(page.get("Users", []))

    # *************************************************
    #
    # *************************************************
    def conformity_report(self, report: o7util.report.Report = None):
        """Conformity Report"""

        if report is None:
            report = o7util.report.Report("Account Conformity Report", section_name="IAM")
        else:
            report.add_section("IAM")

        summary = self.get_account_summary()

        # pprint.pprint(summary)

        report.add_test(name="Root Account MFA", critical=True)
        if summary.get("AccountMFAEnabled", 0) != 1:
            report.test_fail("Not Set")
        else:
            report.test_pass("Set")

        report.add_test(name="Root Programatic Access Key", critical=True)

        if summary.get("AccountAccessKeysPresent", 1) != 0:
            report.test_fail("Present (should be removed)")
        else:
            report.test_pass("None")

        return True

    # *************************************************
    #
    # *************************************************
    def menu(self):
        """Top Menu"""

        obj = o7m.Menu(
            exit_option="b",
            title="IAM General Information",
            title_extra=self.session_info(),
        )
        obj.add_option(
            o7m.Option(
                key="s",
                name="Account Summary",
                callback=lambda: pprint.pprint(self.get_account_summary()),
            )
        )
        obj.add_option(
            o7m.Option(
                key="p",
                name="Password Policy",
                callback=lambda: pprint.pprint(self.get_account_password_policy()),
            )
        )
        obj.add_option(
            o7m.Option(
                key="u",
                name="List of users",
                callback=lambda: pprint.pprint(self.load_users()),
            )
        )
        obj.loop()


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Conformity Report"""
    IAM(**kwargs).menu()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    IAM().conformity_report()
    IAM().menu()
