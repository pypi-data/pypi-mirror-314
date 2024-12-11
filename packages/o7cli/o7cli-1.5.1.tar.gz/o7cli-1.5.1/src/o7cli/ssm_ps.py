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
"""Module allows to view and access SSM Parameter Store"""

# --------------------------------
#
# --------------------------------
import datetime
import logging
import pprint

import o7util.input as o7i
import o7util.menu as o7m
from o7util.table import ColumnParam, Table, TableParam

from o7cli.base import Base

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class SsmPs(Base):
    """Class for SSM Parameter Store"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = self.session.client("ssm")

        self.parameters: list = []
        self.parameter: dict = None
        self.parameter_value: dict = None

    # *************************************************
    #
    # *************************************************
    def load_parameters(self):
        """Load all parameters in Region"""

        logger.info("load_parameters")

        paginator = self.client.get_paginator("describe_parameters")
        unsorted = []

        for page in paginator.paginate():
            unsorted.extend(page.get("Parameters", []))

        logger.info(f"load_parameters: Number of Parameters found {len(unsorted)}")
        self.parameters = sorted(unsorted, key=lambda x: x["Name"])

        return self

    # *************************************************
    #
    # *************************************************
    def load_parameter(self):
        """Load  a single parameter"""

        parameter_name = self.parameter.get("Name")

        logger.info(f"load_parameter: parameter_name={parameter_name}")
        resp = self.client.get_parameter(Name=parameter_name)
        self.parameter_value = resp.get("Parameter", {})

        return self

    # *************************************************
    #
    # *************************************************
    def display_parameters(self):
        """Diplay Secrets"""

        self.load_parameters()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="Name"),
                ColumnParam(title="Type", type="str", data_col="Type"),
                ColumnParam(title="Description", type="str", data_col="Description"),
                ColumnParam(title="V.", type="str", data_col="Version"),
                ColumnParam(title="DataType", type="str", data_col="DataType"),
            ]
        )
        print()
        Table(params, self.parameters).print()
        return self

    # *************************************************
    #
    # *************************************************
    def display_parameter(self):
        """Diplay Parameters"""

        self.load_parameter()

        print("")
        print(f'Name: {self.parameter["Name"]}')
        print(f'Description: {self.parameter.get("Description","")}')
        print("")
        print(f'Value: {self.parameter_value.get("Value","")}')
        print("")
        print(f'Version: {self.parameter_value.get("Version","")}')
        last = self.parameter_value.get(
            "LastModifiedDate", datetime.datetime.fromtimestamp(0)
        )
        print(f"LastModifiedDate: {last.isoformat()}")
        print("")
        print(f'DataType: {self.parameter_value.get("DataType","")}')
        print(f'Tier: {self.parameter.get("Tier","")}')
        print(f'Type: {self.parameter.get("Type","")}')
        print("")

    # *************************************************
    #
    # *************************************************
    def edit_parameter(self):
        """Edit active parameter value"""

        new_value = o7i.input_string("Enter New Value : ")
        if new_value is None:
            return self

        if not o7i.is_it_ok(f"Confirm value -> {new_value}"):
            return self

        self.client.put_parameter(
            Name=self.parameter.get("Name"),
            Value=new_value,
            Type=self.parameter.get("Type"),
            Overwrite=True,
        )
        return self

    # *************************************************
    #
    # *************************************************
    def menu_parameter(self, index):
        """Single Parameter view & edit menu"""

        if not 0 < index <= len(self.parameters):
            return self

        self.parameter = self.parameters[index - 1]

        obj = o7m.Menu(
            exit_option="b",
            title="Parameter Details",
            title_extra=self.session_info(),
            compact=False,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                callback=lambda: pprint.pprint(self.parameter_value),
            )
        )
        obj.add_option(
            o7m.Option(key="e", name="Edit current value", callback=self.edit_parameter)
        )

        obj.display_callback = self.display_parameter
        obj.loop()

        return self

    # *************************************************
    #
    # *************************************************
    def menu_parameters(self):
        """All Parameters view"""

        obj = o7m.Menu(
            exit_option="b",
            title="Parameter Store",
            title_extra=self.session_info(),
            compact=False,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.parameters),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                name="Details for a parameter",
                short="Detail",
                callback=self.menu_parameter,
            )
        )

        obj.display_callback = self.display_parameters
        obj.loop()

        return self


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    SsmPs(**kwargs).menu_parameters()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    the_obj = SsmPs().menu_parameters()

    # .menu_parameters()
