#!/usr/bin/env python
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
"""Module allows to view and access Lambda Functions"""

# --------------------------------
#
# --------------------------------
import logging

# import datetime
import pprint

import o7util.format as o7f
import o7util.menu as o7m
import o7util.terminal as o7t
from o7util.table import ColumnParam, Table, TableParam

import o7cli.logs
from o7cli.base import Base

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class Lambda(Base):
    """Class for Cloudformation Stacks for a Profile & Region"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = self.session.client("lambda")

        self.lambdafcts = []
        self.fct_name = ""
        self.fct_info = {}

    # *************************************************
    #
    # *************************************************
    def load_functions(self):
        """Returns all Functions this Session"""

        logger.info("load_functions")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_functions
        paginator = self.client.get_paginator("list_functions")
        unsorted = []
        param = {}

        for page in paginator.paginate(**param):
            unsorted.extend(page.get("Functions", []))

        logger.info(f"load_functions: Number of Functions found {len(unsorted)}")

        self.lambdafcts = sorted(unsorted, key=lambda x: x.get("FunctionName", ""))

        return self

    # *************************************************
    #
    # *************************************************
    def load_function_info(self):
        """Returns Function details this Session"""

        logger.info(f"load_function_info: fct_name={self.fct_name}")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_function
        self.fct_info = self.client.get_function(FunctionName=self.fct_name)

        return self

    # *************************************************
    #
    # *************************************************
    def invoke_function(self):
        """Invoke the current lambda function"""

        logger.info(f"invoke_function: fct_name={self.fct_name}")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html
        response = self.client.invoke(FunctionName=self.fct_name, InvocationType="Event")

        pprint.pprint(response)

        return response

    # *************************************************
    #
    # *************************************************
    def display_functions(self):
        """Displays a summary of Functions in a Table Format"""

        self.load_functions()
        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="FunctionName"),
                ColumnParam(title="Updated", type="str", data_col="LastModified"),
                ColumnParam(title="Runtime", type="str", data_col="Runtime"),
                ColumnParam(
                    title="Description",
                    type="str",
                    data_col="Description",
                    max_width=50,
                ),
            ]
        )
        Table(params, self.lambdafcts).print()

        return self

    # *************************************************
    #
    # *************************************************
    def display_function(self):
        """Displays a details of a functions"""

        self.load_function_info()
        config = self.fct_info["Configuration"]

        print()
        print(f'Description: {config.get("Description", "na")}')
        print(f'State: {o7t.format_aws_state(config.get("State", "na"))}')
        print()
        print(f'Handler: {config.get("Handler", "na")}')
        print(f'Runtime: {config.get("Runtime", "na")}')
        print(f'Timeout: {config.get("Timeout", "na")}')
        print(f'CodeSize: {o7f.to_bytes(config.get("CodeSize", "na"))}')
        print(f'Role: {config.get("Role", "na")}')
        print()

        print("Environment Variables")
        variables = config.get("Environment", {}).get("Variables", {})
        Table(
            TableParam(
                columns=[
                    ColumnParam(title="Key", type="str", data_col="Key"),
                    ColumnParam(title="Value", type="str", data_col="Value"),
                ],
            ),
            [{"Key": key, "Value": variables[key]} for key in sorted(variables)],
        ).print()
        print()

        print("Tags")
        tags = self.fct_info.get("Tags", {})
        Table(
            TableParam(
                columns=[
                    ColumnParam(title="Key", type="str", data_col="Key"),
                    ColumnParam(title="Value", type="str", data_col="Value"),
                ],
            ),
            [{"Key": key, "Value": tags[key]} for key in sorted(tags)],
        ).print()
        print()

    # *************************************************
    #
    # *************************************************
    def menu_function(self, index):
        """Menu to view and edit all functions in current region"""

        if not 0 < index <= len(self.lambdafcts):
            return self

        self.fct_name = self.lambdafcts[index - 1]["FunctionName"]

        obj = o7m.Menu(
            exit_option="b",
            title=f"Lambda Function - {self.fct_name}",
            title_extra=self.session_info(),
            compact=False,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                callback=lambda: pprint.pprint(self.fct_info),
            )
        )
        obj.add_option(
            o7m.Option(
                key="l",
                name="Views Logs",
                callback=lambda: o7cli.logs.Logs(session=self.session).menu_log_streams(
                    log_group_name=f"/aws/lambda/{self.fct_name}"
                ),
            )
        )
        obj.add_option(
            o7m.Option(key="i", name="Invoke Functions", callback=self.invoke_function)
        )

        obj.display_callback = self.display_function
        obj.loop()

        return self

    # *************************************************
    #
    # *************************************************
    def menu_functions(self):
        """Menu to view and edit all functions in current region"""

        obj = o7m.Menu(
            exit_option="b",
            title="Lambda Functions",
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                callback=lambda: pprint.pprint(self.lambdafcts),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int", name="Details for a function", callback=self.menu_function
            )
        )

        obj.display_callback = self.display_functions
        obj.loop()

        return self


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    Lambda(**kwargs).menu_functions()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    lambda_obj = Lambda().menu_functions()

    # lambda_obj = Lambda()
    # lambda_obj.fct_name = 'ApiStack-InvoiceServicecCreateInvoice8F5D448A-yWQomciUz6v0'
    # lambda_obj.load_function_info()

    # pprint.pprint(lambda_obj.lambdafcts)
