# ************************************************************************
# Copyright 2023 O7 Conseils inc (Philippe Gosselin)
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
"""Module allows to view and access Organizations"""

# --------------------------------
#
# --------------------------------
import json
import logging
import pprint

import o7util.input as o7i
import o7util.menu as o7m
from o7util.table import ColumnParam, Table, TableParam

from o7cli.base import Base

logger = logging.getLogger(__name__)

POLICY_TYPES = [
    "SERVICE_CONTROL_POLICY",
    "TAG_POLICY",
    "BACKUP_POLICY",
    "AISERVICES_OPT_OUT_POLICY",
]


# *************************************************
#
# *************************************************
class Organizations(Base):
    """Class for Organizationr"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.organizations = self.session.client("organizations")

        self.description: dict = None
        self.enabled_services: list = []
        self.accounts: list = []
        self.policies: list = None
        self.delegated_admin: list = None

        self.load_description()

    # *************************************************
    #
    # *************************************************
    def load_description(self):
        """Load Organisations description"""

        logger.info("load_description")
        self.description = self.organizations.describe_organization().get(
            "Organization", {}
        )

        self.enabled_services = []
        paginator = self.organizations.get_paginator(
            "list_aws_service_access_for_organization"
        )
        for page in paginator.paginate():
            self.enabled_services.extend(page.get("EnabledServicePrincipals", []))

        return self

    # *************************************************
    #
    # *************************************************
    def load_accounts(self):
        """Load all linked accounts"""

        logger.info("load_parameters")

        paginator = self.organizations.get_paginator("list_accounts")
        unsorted = []

        for page in paginator.paginate():
            accounts = page.get("Accounts", [])
            unsorted.extend(accounts)

        self.accounts = sorted(unsorted, key=lambda x: x.get("Name", ""))
        logger.info(f"load_accounts: Number of Accounts found {len(unsorted)}")
        return self

    # *************************************************
    #
    # *************************************************
    def load_policies(self):
        """Load all policies"""

        logger.info("load_policies")

        if self.policies is not None:
            return self

        paginator = self.organizations.get_paginator("list_policies")

        self.policies = []

        for policy_type in POLICY_TYPES:
            param = {"Filter": policy_type}
            type_policies = []
            for page in paginator.paginate(**param):
                type_policies.extend(page.get("Policies", []))

            for policy in type_policies:
                policy["Type"] = policy_type

            self.policies.extend(type_policies)

        return self

    # *************************************************
    #
    # *************************************************
    def load_delegated_admin(self):
        """Load all delegated admin"""

        logger.info("load_delegated_admin")

        if self.delegated_admin is not None:
            return self

        paginator = self.organizations.get_paginator("list_delegated_administrators")
        param = {}

        self.delegated_admin = []

        for page in paginator.paginate(**param):
            self.delegated_admin.extend(page.get("DelegatedAdministrators", []))

        return self

    # *************************************************
    #
    # *************************************************
    def display_accounts(self):
        """Display Accounts"""

        self.load_accounts()

        params = TableParam(
            columns=[
                ColumnParam(title="i", type="i", min_width=4),
                ColumnParam(title="Id", type="str", data_col="Id"),
                ColumnParam(title="Name", type="str", data_col="Name"),
                ColumnParam(title="Status", type="str", data_col="Status"),
                ColumnParam(title="Email", type="str", data_col="Email"),
                ColumnParam(title="Joined", type="date", data_col="JoinedTimestamp"),
            ]
        )
        print()
        Table(params, self.accounts).print()

        return self

    # *************************************************
    #
    # *************************************************
    def display_policies(self):
        """Display Policies"""

        self.load_policies()

        params = TableParam(
            columns=[
                ColumnParam(title="i", type="i", min_width=4),
                ColumnParam(title="Id", type="str", data_col="Id"),
                ColumnParam(title="Type", type="str", data_col="Type"),
                ColumnParam(title="AwsManaged", type="str", data_col="AwsManaged"),
                ColumnParam(title="Name", type="str", data_col="Name"),
                ColumnParam(title="Description", type="str", data_col="Description"),
            ]
        )

        Table(params, self.policies).print()
        print()

        return self

    # *************************************************
    #
    # *************************************************
    def display_policy_content(self, index):
        """Display Policy Details"""

        if not 0 < index <= len(self.policies):
            return self

        response = self.organizations.describe_policy(
            PolicyId=self.policies[index - 1].get("Id", "na")
        )
        content = response.get("Policy", {}).get("Content", "")
        content = json.loads(content)
        pprint.pprint(content)

        o7i.wait_input()

    # *************************************************
    #
    # *************************************************
    def display_overview(self):
        """Display Organization"""

        self.load_delegated_admin()

        print()
        print(f'Id: {self.description.get("Id", "na")}')
        print()
        print(f'Master Account Id: {self.description.get("MasterAccountId", "na")}')
        print(f'Master Account Arn: {self.description.get("MasterAccountArn", "na")}')
        print(f'Master Account Email: {self.description.get("MasterAccountEmail", "na")}')
        print()
        print(f'Feature Set: {self.description.get("FeatureSet", "na")}')
        print()
        print("Available Policy Types")
        params = TableParam(
            columns=[
                ColumnParam(title="Type", type="str", data_col="Type"),
                ColumnParam(title="Status", type="str", data_col="Status"),
            ]
        )
        Table(params, self.description.get("AvailablePolicyTypes")).print()
        print()
        print("Available Policy Types")
        params = TableParam(
            columns=[
                ColumnParam(
                    title="ServicePrincipal", type="str", data_col="ServicePrincipal"
                ),
                ColumnParam(title="DateEnabled", type="datetime", data_col="DateEnabled"),
            ]
        )
        Table(params, self.enabled_services).print()
        print()

        print("Delegated Admins")
        params = TableParam(
            columns=[
                ColumnParam(title="Account Id", type="str", data_col="Id"),
                ColumnParam(title="Account Name", type="str", data_col="Name"),
                ColumnParam(title="Email", type="str", data_col="Email"),
                ColumnParam(title="Status", type="str", data_col="Status"),
            ]
        )
        Table(params, self.delegated_admin).print()

    # *************************************************
    #
    # *************************************************
    def menu_accounts(self):
        """Accounts menu"""

        obj = o7m.Menu(
            exit_option="b",
            title="Organization Accounts",
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.accounts),
            )
        )

        obj.display_callback = self.display_accounts
        obj.loop()

        return self

    # *************************************************
    #
    # *************************************************
    def menu_policies(self):
        """Policies menu"""

        obj = o7m.Menu(
            exit_option="b",
            title="Organization Policies",
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.policies),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                name="Details for an Policy",
                short="Policy",
                callback=self.display_policy_content,
            )
        )

        obj.display_callback = self.display_policies
        obj.loop()

        return self

    # *************************************************
    #
    # *************************************************
    def menu_overview(self):
        """Organization menu"""

        obj = o7m.Menu(
            exit_option="b",
            title="Organization Overview",
            title_extra=self.session_info(),
            compact=False,
        )

        obj.add_option(
            o7m.Option(
                key="a",
                name="Display Accounts",
                short="Accounts",
                callback=self.menu_accounts,
            )
        )
        obj.add_option(
            o7m.Option(
                key="p",
                name="Display Policies",
                short="Policies",
                callback=self.menu_policies,
            )
        )
        obj.add_option(
            o7m.Option(
                key="ra",
                name="Raw Delegated Admins",
                short="Raw Admins",
                callback=lambda: pprint.pprint(self.delegated_admin),
            )
        )

        obj.display_callback = self.display_overview
        obj.loop()

        return self


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    Organizations(**kwargs).menu_overview()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    the_obj = Organizations()

    pprint.pprint(the_obj.organizations.list_aws_service_access_for_organization())

    # the_obj.menu_overview()
