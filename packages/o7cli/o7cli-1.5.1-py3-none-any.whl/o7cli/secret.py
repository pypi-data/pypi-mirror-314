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
# distributed under the License is distibuted on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ************************************************************************
"""Module allows to view and access Secrets"""

# --------------------------------
#
# --------------------------------
import json
import logging
import pprint

import o7util.menu as o7m
from o7util.table import ColumnParam, Table, TableParam

from o7cli.base import Base

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class Secret(Base):
    """Class for Secrets Manager"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = self.session.client("secretsmanager")

        self.secrets: list = []
        self.secret_name: str = None
        self.secret_details: dict = None

    # *************************************************
    #
    # *************************************************
    def load_secrets(self):
        """Load all secret in Region"""

        logger.info("load_secrets")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/list_secrets.html
        paginator = self.client.get_paginator("list_secrets")
        unsorted = []
        param = {"IncludePlannedDeletion": False}

        for page in paginator.paginate(**param):
            unsorted.extend(page.get("SecretList", []))

        logger.info(f"load_parameters: Number of Secret found {len(unsorted)}")

        self.secrets = sorted(unsorted, key=lambda x: x["Name"])

        return self

    # *************************************************
    #
    # *************************************************
    def load_secret(self):
        """Load a single secret"""
        logger.info("load_secrets")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/describe_secret.html
        self.secret_details = self.client.describe_secret(SecretId=self.secret_name)

    # *************************************************
    #
    # *************************************************
    def load_secret_value(self, stage: str = "AWSCURRENT"):
        """Load  a single secret"""

        logger.info(f"load_secret_value: secret_name={self.secret_name} stage={stage}")
        secret_value = self.client.get_secret_value(
            SecretId=self.secret_name, VersionStage=stage
        )

        return secret_value

    # *************************************************
    #
    # *************************************************
    def view_secret(self, stage: str = "AWSCURRENT"):
        """View a single secret value"""

        secret_data = self.load_secret_value(stage)
        secret_value = secret_data.get("SecretString", "NOT A STRING")

        try:
            secret_dict = json.loads(secret_value)
        except json.decoder.JSONDecodeError:
            secret_dict = secret_value

        pprint.pprint(secret_dict)
        return self

    # *************************************************
    #
    # *************************************************
    def display_secrets(self):
        """Diplay Secrets"""

        self.load_secrets()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="Name"),
                ColumnParam(title="Description", type="str", data_col="Description"),
                ColumnParam(title="Rotation?", type="str", data_col="RotationEnabled"),
            ]
        )
        print()
        Table(params, self.secrets).print()
        return self

    # *************************************************
    #
    # *************************************************
    def display_secret(self):
        """Display Instances"""

        self.load_secret()

        print("")

        print(f'Name: {self.secret_details.get("Name", "")}')
        print(f'Description: {self.secret_details.get("Description", "")}')
        print()
        print(f'RotationEnabled: {self.secret_details.get("RotationEnabled", "")}')
        print()
        print(f'Last ChangedD ate: {self.secret_details.get("LastChangedDate", "")}')
        print(f'Last Accessed Date: {self.secret_details.get("LastAccessedDate", "")}')
        print(f'Next Rotation Date: {self.secret_details.get("NextRotationDate", "")}')
        print()
        print("Tags")
        Table(
            TableParam(
                columns=[
                    ColumnParam(title="Key", type="str", data_col="Key"),
                    ColumnParam(title="Value", type="str", data_col="Value"),
                ]
            ),
            self.secret_details.get("Tags", []),
        ).print()
        print()
        print("Versions Id To Stage")
        Table(
            TableParam(
                columns=[
                    ColumnParam(title="Version Id", type="str", data_col="Key"),
                    ColumnParam(title="Stage", type="str", data_col="Value"),
                ]
            ),
            [
                {"Key": key, "Value": value}
                for key, value in self.secret_details.get(
                    "VersionIdsToStages", []
                ).items()
            ],
        ).print()
        print()

    # *************************************************
    #
    # *************************************************
    def menu_secret(self, index):
        """Single Secret view & edit menu"""

        if not 0 < index <= len(self.secrets):
            return self

        self.secret_name = self.secrets[index - 1].get("Name")

        obj = o7m.Menu(
            exit_option="b",
            title="Secret Details",
            title_extra=self.session_info(),
            compact=False,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                callback=lambda: pprint.pprint(self.secret_details),
            )
        )
        obj.add_option(
            o7m.Option(
                key="c",
                name="View Current Value",
                callback=lambda: self.view_secret("AWSCURRENT"),
            )
        )
        obj.add_option(
            o7m.Option(
                key="p",
                name="View Previous Value",
                callback=lambda: self.view_secret("AWSPREVIOUS"),
            )
        )

        obj.display_callback = self.display_secret
        obj.loop()

        return self

    # *************************************************
    #
    # *************************************************
    def menu_secrets(self):
        """All Secrets view"""

        obj = o7m.Menu(
            exit_option="b",
            title="Secrets",
            title_extra=self.session_info(),
            compact=False,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.secrets),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                name="Details for a secret",
                short="Detail",
                callback=self.menu_secret,
            )
        )

        obj.display_callback = self.display_secrets
        obj.loop()

        return self


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    Secret(**kwargs).menu_secrets()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    Secret().menu_secrets()
