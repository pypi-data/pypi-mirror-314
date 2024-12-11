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
import datetime
import logging
import pprint

import o7util.menu as o7m
import o7util.terminal as o7t
import pandas as pd

import o7cli.organizations
from o7cli.base import Base

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class SsoAdmin(Base):  # pylint: disable=too-many-instance-attributes
    """Class for SSO Admin"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ssoadmin = self.session.client("sso-admin")
        self.idstore = self.session.client("identitystore")

        self.accounts: list = []

        self.sso_instance_arn = None
        self.sso_id_store = None

        self.df_accounts: pd.DataFrame = None
        self.df_users: pd.DataFrame = None
        self.df_groups: pd.DataFrame = None
        self.df_group_members: pd.DataFrame = None
        self.df_permission_sets: pd.DataFrame = None
        self.df_account_assignments: pd.DataFrame = None

    # *************************************************
    #
    # *************************************************
    def load_all(self):
        """Load all information"""

        print("Loading All Information for the SSO Admin")
        print("Loading General Information")
        self.load_general()
        print("Loading Accounts")
        self.load_accounts()
        print("Loading Users")
        self.load_users()
        print("Loading Groups")
        self.load_groups()
        print("Loading Group Members")
        self.load_group_members()
        print("Loading Permission Sets")
        self.load_permissions_sets()
        print("Loading Account Assignments")
        self.load_account_assignments()

        return self

    # *************************************************
    #
    # *************************************************
    def load_general(self):
        """Load general information"""

        iam_instances = self.ssoadmin.list_instances().get("Instances", [])

        if len(iam_instances) == 0:
            logger.error("No SSO Instance found")
            return self

        self.sso_instance_arn = iam_instances[0]["InstanceArn"]
        self.sso_id_store = iam_instances[0]["IdentityStoreId"]

        return self

    # *************************************************
    #
    # *************************************************
    def load_accounts(self):
        """Load accounts"""

        accounts = (
            o7cli.organizations.Organizations(session=self.session)
            .load_accounts()
            .accounts
        )
        self.df_accounts = pd.DataFrame(data=accounts)

        self.df_accounts["JoinedTimestamp"] = self.df_accounts[
            "JoinedTimestamp"
        ].dt.tz_localize(None)

        return self

    # *************************************************
    #
    # *************************************************
    def load_users(self):
        """Load users"""

        paginator = self.idstore.get_paginator("list_users")
        users = []
        param = {"IdentityStoreId": self.sso_id_store}

        for page in paginator.paginate(**param):
            users.extend(page.get("Users", []))

        self.df_users = pd.DataFrame(data=users)

        return self

    # *************************************************
    #
    # *************************************************
    def load_groups(self):
        """Load Groups"""

        paginator = self.idstore.get_paginator("list_groups")
        groups = []
        param = {"IdentityStoreId": self.sso_id_store}

        for page in paginator.paginate(**param):
            groups.extend(page.get("Groups", []))

        self.df_groups = pd.DataFrame(data=groups)

        return self

        # *************************************************

    #
    # *************************************************
    def load_group_members(self):
        """Load Users for each Groups"""

        paginator = self.idstore.get_paginator("list_group_memberships")
        group_members = []

        # pylint: disable=unused-variable
        for (
            _index,
            group,
        ) in self.df_groups.iterrows():
            param = {"IdentityStoreId": self.sso_id_store, "GroupId": group["GroupId"]}
            print(f"    Group: {group['GroupId']} - {group['DisplayName']}")
            for page in paginator.paginate(**param):
                group_members.extend(page.get("GroupMemberships", []))

        for member in group_members:
            member["UserId"] = member["MemberId"].get("UserId", None)

        self.df_group_members = pd.DataFrame(data=group_members)

        return self

    # *************************************************
    #
    # *************************************************
    def load_permissions_sets(self):
        """Load all permission sets"""

        paginator = self.ssoadmin.get_paginator("list_permission_sets")
        permission_sets = []
        param = {"InstanceArn": self.sso_instance_arn}

        for page in paginator.paginate(**param):
            permission_sets.extend(page.get("PermissionSets", []))

        permission_sets_details = []

        # Loop through all permission sets
        for permission_set in permission_sets:
            response = self.ssoadmin.describe_permission_set(
                InstanceArn=self.sso_instance_arn, PermissionSetArn=permission_set
            )
            permission_sets_details.append(response["PermissionSet"])

        self.df_permission_sets = pd.DataFrame(data=permission_sets_details)
        self.df_permission_sets["CreatedDate"] = self.df_permission_sets[
            "CreatedDate"
        ].dt.tz_localize(None)

        return self

    # *************************************************
    #
    # *************************************************
    def load_account_assignments(self):
        """Load all permission sets"""

        account_assignments = []

        # pylint: disable=unused-variable
        for (
            _index_a,
            account,
        ) in self.df_accounts.iterrows():
            print(f"    Account: {account['Id']} - {account['Name']}")

            # Loop through all permission sets to list account assignments
            for _index_ps, permission_set in self.df_permission_sets.iterrows():
                account_assignments_response = self.ssoadmin.list_account_assignments(
                    InstanceArn=self.sso_instance_arn,
                    AccountId=account["Id"],
                    PermissionSetArn=permission_set["PermissionSetArn"],
                )
                account_assignments.extend(
                    account_assignments_response["AccountAssignments"]
                )

        self.df_account_assignments = pd.DataFrame(data=account_assignments)
        return self

    # *************************************************
    #
    # *************************************************
    def display_overview(self):
        """Display Instances"""

        if self.sso_instance_arn is None:
            self.load_all()

        print()
        print(f"SSO Instance Arn: {self.sso_instance_arn}")
        print(f"SSO Store Id: {self.sso_id_store}")
        print()
        print(f"Number of Accounts: {len(self.df_accounts.index)}")
        print(f"Number of Users: {len(self.df_users.index)}")
        print(f"Number of Groups: {len(self.df_groups.index)}")
        print()
        print(f"Number of Permission Sets: {len(self.df_permission_sets.index)}")
        print(f"Number of Account Assignments: {len(self.df_account_assignments.index)}")
        print()

    # *************************************************
    #
    # *************************************************
    def compile_account_user_access(self) -> pd.DataFrame:
        """For Each Account list the users and their access"""

        df = self.df_account_assignments.merge(
            self.df_group_members[["UserId", "GroupId"]],
            left_on="PrincipalId",
            right_on="GroupId",
            how="left",
        )

        df = df.merge(
            self.df_users["UserId"],
            left_on="PrincipalId",
            right_on="UserId",
            how="left",
            suffixes=("_group", "_user"),
        )
        df["UserId"] = df["UserId_group"].combine_first(df["UserId_user"])

        # Add account info
        self.df_accounts["AccountName"] = self.df_accounts["Name"]
        df = df.merge(
            self.df_accounts[["Id", "AccountName"]],
            left_on="AccountId",
            right_on="Id",
            how="left",
        )

        # Add Permission info
        self.df_permission_sets["PermissionSetName"] = self.df_permission_sets["Name"]
        df = df.merge(
            self.df_permission_sets[["PermissionSetArn", "PermissionSetName"]],
            left_on="PermissionSetArn",
            right_on="PermissionSetArn",
            how="left",
        )

        # Add Group info
        self.df_groups["GroupName"] = self.df_groups["DisplayName"]
        df = df.merge(
            self.df_groups[["GroupId", "GroupName"]],
            left_on="GroupId",
            right_on="GroupId",
            how="left",
        )

        # Add user info
        df = df.merge(
            self.df_users[["UserId", "UserName"]],
            left_on="UserId",
            right_on="UserId",
            how="left",
        )

        # df.info()
        df = df[
            ["AccountId", "AccountName", "GroupName", "PermissionSetName", "UserName"]
        ]
        df.set_index(
            ["AccountId", "AccountName", "GroupName", "PermissionSetName"], inplace=True
        )

        return df

    # *************************************************
    #
    # *************************************************
    def to_excel(self):
        """Save to Excel"""

        filename = f"aws-ssoadmin-{datetime.datetime.now().isoformat()[0:19].replace(':','-')}.xlsx"
        with pd.ExcelWriter(filename) as writer:  # pylint: disable=abstract-class-instantiated
            df_parameters = pd.DataFrame(
                [
                    {"Parameter": "Date", "Value": datetime.datetime.now().isoformat()},
                    {"Parameter": "SSO Store Id", "Value": f"{self.sso_id_store }"},
                    {
                        "Parameter": "SSO Instance Arn",
                        "Value": f"{self.sso_instance_arn }",
                    },
                ]
            )

            df_parameters.to_excel(writer, sheet_name="Parameters")
            self.compile_account_user_access().to_excel(writer, sheet_name="Summary")
            self.df_accounts.to_excel(writer, sheet_name="Accounts")
            self.df_users.to_excel(writer, sheet_name="Users")
            self.df_groups.to_excel(writer, sheet_name="Groups")
            self.df_group_members.to_excel(writer, sheet_name="Group Members")
            self.df_permission_sets.to_excel(writer, sheet_name="Permission Sets")
            self.df_account_assignments.to_excel(writer, sheet_name="Account Assignments")

        print(f"SSO Admin saved in file: {filename}")

    # *************************************************
    #
    # *************************************************
    def from_excel(self, filename):
        """Save to Excel"""

        print(f"Loading file: {filename}")
        self.df_accounts = pd.read_excel(filename, sheet_name="Accounts")
        self.df_users = pd.read_excel(filename, sheet_name="Users")
        self.df_groups = pd.read_excel(filename, sheet_name="Groups")
        self.df_group_members = pd.read_excel(filename, sheet_name="Group Members")
        self.df_permission_sets = pd.read_excel(filename, sheet_name="Permission Sets")
        self.df_account_assignments = pd.read_excel(
            filename, sheet_name="Account Assignments"
        )

    # *************************************************
    #
    # *************************************************
    def menu_overview(self):
        """Accounts menu"""

        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", o7t.get_width())
        pd.set_option("display.max_colwidth", None)

        obj = o7m.Menu(
            exit_option="b",
            title="SSO Admin",
            title_extra=self.session_info(),
            compact=False,
        )

        obj.add_option(
            o7m.Option(
                key="a",
                name="Display Accounts",
                short="Accounts",
                callback=lambda: pprint.pprint(
                    self.df_accounts.to_dict(orient="records")
                ),
            )
        )
        obj.add_option(
            o7m.Option(
                key="u",
                name="Display Users",
                short="Users",
                callback=lambda: pprint.pprint(self.df_users.to_dict(orient="records")),
            )
        )
        obj.add_option(
            o7m.Option(
                key="g",
                name="Display Groups",
                short="Groups",
                callback=lambda: pprint.pprint(self.df_groups.to_dict(orient="records")),
            )
        )
        obj.add_option(
            o7m.Option(
                key="m",
                name="Display Group Members",
                short="Group Members",
                callback=lambda: pprint.pprint(
                    self.df_group_members.to_dict(orient="records")
                ),
            )
        )
        obj.add_option(
            o7m.Option(
                key="p",
                name="Display Permission Sets",
                short="Permission Sets",
                callback=lambda: pprint.pprint(
                    self.df_permission_sets.to_dict(orient="records")
                ),
            )
        )
        obj.add_option(
            o7m.Option(
                key="s",
                name="Display Account Assignments",
                short="Account Assignments",
                callback=lambda: pprint.pprint(
                    self.df_account_assignments.to_dict(orient="records")
                ),
            )
        )
        obj.add_option(
            o7m.Option(
                key="x", name="Save to Excel", short="Excel", callback=self.to_excel
            )
        )
        obj.add_option(
            o7m.Option(
                key="c",
                name="Compile Account User Access",
                short="Compile",
                callback=lambda: print(self.compile_account_user_access()),
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
    SsoAdmin(**kwargs).menu_overview()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    the_obj = SsoAdmin()

    the_obj.from_excel("aws-ssoadmin-2023-09-20T13-17-56.xlsx")
    print(the_obj.compile_account_user_access())

    # the_obj.load_permissions_sets()

    # the_obj.load_general()
    # the_obj.load_users()
    # pprint.pprint(the_obj.dfUsers.to_dict(orient='records'))

    # the_obj.menu_overview()
