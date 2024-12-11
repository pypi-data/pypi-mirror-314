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
"""Module allows to view and access Cloud Formation"""

# --------------------------------
#
# --------------------------------
import datetime
import logging
import os
import pprint

import botocore
import botocore.config
import o7util.file_explorer as o7fe
import o7util.input as o7i
import o7util.menu as o7m
import o7util.terminal as o7t
from o7util.table import ColumnParam, Table, TableParam

import o7cli.s3

# import o7lib.util.displays as o7d
# import o7lib.util.terminal as o7t
# import o7lib.util.table
from o7cli.base import Base

logger = logging.getLogger(__name__)

# COLOR_OK = '\033[92m'
# COLOR_WARNING = '\033[93m'
# COLOR_FAIL = '\033[91m'
# COLOR_END = '\033[0m'


# *************************************************
#
# *************************************************
class Cloudformation(Base):
    """Class for Cloudformation Stacks for a Profile & Region"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#cloudformation

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cfn = self.session.client(
            "cloudformation", config=botocore.config.Config(connect_timeout=5)
        )

        self.s3_for_upload = None

        self.stacks = []
        self.stack_name = None
        self.stack = None

        self.events = []
        self.max_events_per_page = 50

        self.resources = []

        self.drifters = []

    # *************************************************
    #
    # *************************************************
    def load_stacks(self, stack_name=None):
        """Returns all Stacks for this Session"""

        logger.info("load_stacks")

        param = {}
        stacks = []
        if stack_name is not None:
            param["StackName"] = stack_name

        paginator = self.cfn.get_paginator("describe_stacks")
        for page in paginator.paginate(**param):
            stacks.extend(page.get("Stacks", []))

        # Reformat some data
        for stack in stacks:
            drift_status = stack["DriftInformation"].get("StackDriftStatus", "")
            drift_date = stack["DriftInformation"].get("LastCheckTimestamp", None)
            if drift_date is not None:
                drift_status = f"{drift_status} ({drift_date:%Y-%m-%d})"

            stack["DriftStatus"] = drift_status

        if stack_name is not None:
            self.stack = stacks[0]
        else:
            self.stacks = stacks

    # *************************************************
    #
    # *************************************************
    def load_events(self):
        """Returns latest events for a stacks"""
        logger.info("LoadEvents")

        param = {
            "StackName": self.stack_name,
        }

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_events
        resp = self.cfn.describe_stack_events(**param)
        # pprint.pprint(resp)
        logger.info(f'LoadEvents: Number of Events found {len(resp["StackEvents"])}')

        self.events = resp["StackEvents"]

        if self.max_events_per_page is not None:
            self.events = self.events[0 : self.max_events_per_page]

    # *************************************************
    #
    # *************************************************
    def load_resources(self):
        """Returns all resources for a stack"""

        logger.info("LoadResources")

        self.resources = []
        param = {
            "StackName": self.stack_name,
        }

        paginator = self.cfn.get_paginator("list_stack_resources")
        for page in paginator.paginate(**param):
            self.resources.extend(page.get("StackResourceSummaries", []))

        # Reformat some data
        for resources in self.resources:
            drift_status = resources["DriftInformation"].get(
                "StackResourceDriftStatus", ""
            )
            resources["DriftStatus"] = drift_status

    # *************************************************
    #
    # *************************************************
    def load_drifters(self):
        """Return all drifters post a drift detection"""

        logger.info("LoadDrifters for Stack : {self.stack_name}")

        self.drifters = []
        param = {
            "StackName": self.stack_name,
            "StackResourceDriftStatusFilters": ["MODIFIED"],
        }

        while True:
            resp = self.cfn.describe_stack_resource_drifts(**param)
            self.drifters.extend(resp.get("StackResourceDrifts", []))

            if resp.get("NextToken", None) is None:
                break
            param["NextToken"] = resp["NextToken"]

    # *************************************************
    #
    # *************************************************
    def init_drift_detection(self):
        """Initialize the drift verification for a stack"""

        logger.info("InitDriftDetection for stack : {self.stack_name}")

        if o7i.is_it_ok(f"Confirm Drift Detection for Stack: {self.stack_name}") is False:
            return

        param = {"StackName": self.stack_name}
        resp = self.cfn.detect_stack_drift(**param)
        pprint.pprint(resp)

        logger.info("InitDriftDetection Response : {resp}")

    # *************************************************
    #
    # *************************************************
    def find_s3_for_upload(self):
        """Find bucket where to upload template file"""
        logger.info("find_s3_for_upload")

        s3_obj = o7cli.s3.S3()
        buckets = s3_obj.load_buckets().buckets

        for bucket in buckets:
            if (
                s3_obj.get_bucket_region(bucket=bucket["Name"])
                == self.session.region_name
            ):
                names = bucket["Name"].split("-")
                if len(names) >= 3:
                    if names[0] == "cf" and names[1] == "templates":
                        logger.info(f'find_s3_for_upload: found bucket {bucket["Name"]}')
                        self.s3_for_upload = bucket["Name"]

    # *************************************************
    #
    # *************************************************
    def upload_template(self, file_path):
        """Unload the CFN template to S3 for update or creation"""

        logger.info(f"upload_template: {file_path=}")

        if self.s3_for_upload is None:
            self.find_s3_for_upload()

        if self.s3_for_upload is None:
            logger.error("Not able to find upload bucket")
            return None

        basename = os.path.basename(file_path)
        prefix = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        key = f"{prefix}-{basename}"

        s3_path = o7cli.s3.S3().upload_file_obj(
            bucket=self.s3_for_upload, key=key, file_path=file_path
        )

        logger.info(f"upload_template: Done {s3_path=}")
        return s3_path

    # *************************************************
    #
    # *************************************************
    def validate_template(self, file_path=None):
        """Validate and Load a CFN template, returns parameters for Update function"""

        logger.info(f"validate_template: {file_path=}")

        if file_path is not None:
            # Load File to S3
            s3_path = self.upload_template(file_path)
            try:
                # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.validate_template
                response = self.cfn.validate_template(TemplateURL=s3_path)
            except botocore.exceptions.ClientError as error:
                print(f"validate_template: {error}")
                return None
        else:
            response = self.stack

        # print('-' * 50)
        # pprint.pprint(stack)
        # print('-' * 50)
        # pprint.pprint(response)
        print("=" * 50)
        print("Stack Update Validation")
        print("=" * 50)
        print(f"Name: {o7t.format_normal(self.stack['StackName'])}")
        print("")

        # ---------------------------------
        #  Validate Description
        # ---------------------------------
        new_desc = response.get("Description", "").replace("\n", " ").strip()
        cur_desc = self.stack.get("Description", "").replace("\n", " ").strip()
        if new_desc == cur_desc:
            print(f"Description: {o7t.format_normal(cur_desc)}")
        else:
            print(f"Current Description -> {o7t.format_alarm(cur_desc)}")
            print(f"New Description     -> {o7t.format_alarm(new_desc)}")
            if o7i.is_it_ok("Do you Accept a New Description ?") is False:
                return None

        # ---------------------------------
        #  Validate Parameters
        # ---------------------------------
        temp_parameters = []
        for new_param in response.get("Parameters", []):
            temps_param = {
                "key": new_param["ParameterKey"],
                "currentValue": new_param.get("DefaultValue", ""),
                "default": new_param.get("DefaultValue", ""),
                "description": new_param.get("Description", ""),
                "action": "add",
            }
            # look if current param is there
            for cur_param in self.stack.get("Parameters", []):
                if cur_param["ParameterKey"] == new_param["ParameterKey"]:
                    temps_param["currentValue"] = cur_param["ParameterValue"]
                    temps_param["action"] = "same"
                    break

            temp_parameters.append(temps_param)

        # ---------------------------------
        # Look for missing parameters
        # ---------------------------------
        for cur_param in self.stack.get("Parameters", []):
            missing = True
            for temp_param in temp_parameters:
                if temp_param["key"] == cur_param["ParameterKey"]:
                    missing = False

            if missing:
                temp_parameters.append(
                    {
                        "key": cur_param["ParameterKey"],
                        "currentValue": cur_param["ParameterValue"],
                        "action": "delete",
                    }
                )

        # ---------------------------------
        #  Menu to edit param
        # ---------------------------------
        print("")
        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="key"),
                ColumnParam(
                    title="Action",
                    type="str",
                    data_col="action",
                    format="aws-edit",
                ),
                ColumnParam(title="Current", type="str", data_col="currentValue"),
                ColumnParam(title="Description", type="str", data_col="description"),
            ]
        )
        temp_parameters = sorted(temp_parameters, key=lambda x: x["key"])

        while True:
            Table(params, temp_parameters).print()

            key = o7i.input_multi(
                "Are Those Parameters Acceptable (y/n) Edit Parameter(int):"
            )

            if isinstance(key, str):
                if key.lower() == "y":
                    break
                if key.lower() == "n":
                    return None

            if isinstance(key, int) and key > 0 and key <= len(temp_parameters):
                p_key = temp_parameters[key - 1]["key"]
                p_value = o7i.input_string(f"Enter new value for {p_key} -> ")
                temp_parameters[key - 1]["currentValue"] = p_value
                temp_parameters[key - 1]["action"] = "modify"

        # ---------------------------------
        #  Validate Capabilies
        # ---------------------------------
        capabilities = response.get("Capabilities", [])
        cap_reason = response.get("CapabilitiesReason", "").replace("\n", "").strip()

        if len(capabilities) > 0:
            print("")
            print(f"Required Capabilities : {capabilities}")
            print(f"Reason: {cap_reason}")
            if o7i.is_it_ok("Do you Accept Required Capabilities ?") is False:
                return None

        # ---------------------------------
        #  Prepare Update stack Parameters
        # ---------------------------------
        ret = {
            "StackName": self.stack["StackName"],
            "Parameters": [],
            "Capabilities": capabilities,
        }

        if file_path is not None:
            ret["TemplateURL"] = s3_path
        else:
            ret["UsePreviousTemplate"] = True

        # Building Parameter structure without the deleted parameters
        for parameter in temp_parameters:
            if parameter["action"] != "delete":
                update = {
                    "ParameterKey": parameter["key"],
                    "ParameterValue": parameter["currentValue"],
                }
                ret["Parameters"].append(update)

        return ret

    # *************************************************
    #
    # *************************************************
    def update_template(self, file_path=None):
        """Update the stack template"""

        logger.info(f"update_template: {self.stack_name=} {file_path=}")
        self.load_stacks(stack_name=self.stack_name)

        # Validating Template
        update_param = self.validate_template(file_path=file_path)
        if update_param is None:
            logger.error(f"UpdateTemplate: Template Valiadation Failed {file_path=}")
            return None

        logger.debug(f"update_template: Ready to Update {update_param=}")
        # pprint.pprint(update_param)

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.update_stack
        try:
            resp_update = self.cfn.update_stack(**update_param)
        except botocore.exceptions.ClientError as error:
            print(f"Error: {error}")
            return None

        print(f"Success = {resp_update}")

        return resp_update

    # *************************************************
    #
    # *************************************************
    def update_template_file(self):
        """Update the stack template with a new input file"""

        file_path = o7fe.FileExplorer().select_file(
            filters={"extensions": [".yaml", "yml"]}
        )
        if file_path is None:
            print("No file selected")
            return

        self.update_template(file_path=file_path)

    # *************************************************
    #
    # *************************************************
    def display_stacks(self):
        """Displays a summary of Stacks in a Table Format"""

        self.load_stacks()

        print("")

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", max_width=50, data_col="StackName"),
                ColumnParam(title="Creation", type="date", data_col="CreationTime"),
                ColumnParam(title="Updated", type="since", data_col="LastUpdatedTime"),
                ColumnParam(
                    title="Status",
                    type="str",
                    data_col="StackStatus",
                    format="aws-status",
                ),
                ColumnParam(
                    title="Reason",
                    type="str",
                    data_col="StackStatusReason",
                    max_width=50,
                ),
                ColumnParam(
                    title="Drift",
                    type="str",
                    width=20,
                    data_col="DriftStatus",
                    format="aws-drift",
                ),
            ]
        )
        print()
        Table(params, self.stacks).print()

    # *************************************************
    #
    # *************************************************
    def display_events(self):
        """Displays a summary of Events in a Table Format"""

        self.load_events()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Date Time", type="datetime", data_col="Timestamp"),
                ColumnParam(
                    title="Logical ID",
                    type="str",
                    max_width=30,
                    data_col="LogicalResourceId",
                ),
                # ColumnParam(
                #     title="Physical ID",
                #     type="str",
                #     width=30,
                #     data_col="PhysicalResourceId",
                # ),
                ColumnParam(title="Type", type="str", data_col="ResourceType"),
                ColumnParam(
                    title="Status",
                    type="str",
                    data_col="ResourceStatus",
                    format="aws-status",
                    max_width=20,
                ),
                ColumnParam(title="Reason", type="str", data_col="ResourceStatusReason"),
            ]
        )

        Table(params, self.events).print()

    # *************************************************
    #
    # *************************************************
    def display_resources(self):
        """Displays a summary of Resources in a Table Format"""

        self.load_resources()

        params = TableParam(
            columns=[
                ColumnParam(
                    title="Logical ID",
                    type="str",
                    data_col="LogicalResourceId",
                    sort="asc",
                ),
                ColumnParam(title="Type", type="str", data_col="ResourceType"),
                ColumnParam(
                    title="Physical ID",
                    type="str",
                    data_col="PhysicalResourceId",
                    max_width=40,
                ),
                ColumnParam(
                    title="Updated",
                    type="datetime",
                    data_col="LastUpdatedTimestamp",
                ),
                ColumnParam(
                    title="Status",
                    type="str",
                    data_col="ResourceStatus",
                    format="aws-status",
                ),
                ColumnParam(
                    title="Drift",
                    type="str",
                    data_col="DriftStatus",
                    format="aws-drift",
                ),
                ColumnParam(title="Reason", type="str", data_col="ResourceStatusReason"),
            ]
        )
        Table(params, self.resources).print()

    # *************************************************
    #
    # *************************************************
    def display_drifters(self):
        """Displays a summary of Drifters in a Table Format"""

        self.load_drifters()
        drifts = []

        for drifter in self.drifters:
            l_id = drifter["LogicalResourceId"]
            for diff in drifter["PropertyDifferences"]:
                drift = {
                    "LogicalResourceId": l_id,
                    "DifferenceType": diff["DifferenceType"],
                    "PropertyPath": diff["PropertyPath"],
                    "ExpectedValue": diff["ExpectedValue"],
                    "ActualValue": diff["ActualValue"],
                }
                drifts.append(drift)

        params = TableParam(
            title=f"List of Drifts - {self.title_line()}",
            columns=[
                ColumnParam(
                    title="Logical ID",
                    type="str",
                    data_col="LogicalResourceId",
                    sort="asc",
                ),
                ColumnParam(title="Type", type="str", data_col="DifferenceType"),
                ColumnParam(title="Property", type="str", data_col="PropertyPath"),
                ColumnParam(title="Expected", type="str", data_col="ExpectedValue"),
                ColumnParam(title="Actual", type="str", data_col="ActualValue"),
            ],
        )

        Table(params, drifts).print()

    # *************************************************
    #
    # *************************************************
    def _display_parameters(self, parameters, max_parameters=None):
        """Displays a summary of Parameters in a Table Format"""
        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(
                    title="Key",
                    type="str",
                    width=30,
                    data_col="ParameterKey",
                    sort="asc",
                ),
                ColumnParam(
                    title="Value",
                    type="str",
                    width=50,
                    data_col="ParameterValue",
                ),
                ColumnParam(
                    title="Resolved Value",
                    type="str",
                    width=30,
                    data_col="ResolvedValue",
                ),
            ]
        )

        if max is not None:
            parameters = parameters[0:max_parameters]

        Table(params, parameters).print()

    # *************************************************
    #
    # *************************************************
    def display_outputs(self, outputs, max_output=None):
        """Displays a summary of Outputs in a Table Format"""

        params = TableParam(
            columns=[
                ColumnParam(
                    title="Key",
                    type="str",
                    width=30,
                    data_col="OutputKey",
                    sort="asc",
                ),
                ColumnParam(
                    title="Value",
                    type="str",
                    width=80,
                    data_col="OutputValue",
                ),
                ColumnParam(
                    title="Description",
                    type="str",
                    width=20,
                    data_col="Description",
                ),
                ColumnParam(
                    title="Export Name",
                    type="str",
                    width=30,
                    data_col="ExportName",
                ),
            ]
        )

        if max is not None:
            outputs = outputs[0:max_output]
        Table(params, outputs).print()

    # *************************************************
    #
    # *************************************************
    def display_single_stack(self):
        """Display details for a specific Stack"""

        self.load_stacks(stack_name=self.stack_name)

        print("")

        print(f'Description: {self.stack.get("Description", "")}')
        print(f'Creation: {self.stack.get("CreationTime", ""):%Y-%m-%d}')
        print(f'Last Updated: {self.stack.get("LastUpdatedTime", "NA")}')
        print(f'Status: {o7t.format_aws_status(self.stack.get("StackStatus", ""))}')
        print(f'Status Reason: {self.stack.get("StackStatusReason", "-")}')

        print(
            f'Drift Detection: {o7t.format_aws_drift(self.stack.get("DriftStatus", "-"))}'
        )

        print(f'Capabilities: {self.stack.get("Capabilities", [])}')
        print(f'Tags: {self.stack.get("Tags", [])}')

        print("")
        print("Parameters")
        self._display_parameters(self.stack.get("Parameters", []))
        print("")
        print("Outputs")
        self.display_outputs(self.stack.get("Outputs", []))
        print("")

        return

    # *************************************************
    #
    # *************************************************
    def menu_stacks(self):
        """Menu to view and edit all stacks in current region"""

        obj = o7m.Menu(
            exit_option="b",
            title="Cloudformation Stacks",
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                short="Raw",
                callback=lambda: pprint.pprint(self.stacks),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                short="Details",
                callback=self.menu_single_stack,
            )
        )

        obj.display_callback = self.display_stacks
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_single_stack(self, index):
        """Menu to view and edit a specific stack"""

        if not 0 < index <= len(self.stacks):
            return self

        self.stack_name = self.stacks[index - 1]["StackName"]

        obj = o7m.Menu(
            exit_option="b",
            title=f"Stack - {self.stack_name}",
            title_extra=self.session_info(),
            compact=True,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                short="Raw",
                callback=lambda: pprint.pprint(self.stack),
            )
        )
        obj.add_option(o7m.Option(key="e", short="Events", callback=self.menu_events))
        obj.add_option(
            o7m.Option(key="s", short="Resources", callback=self.menu_resources)
        )
        obj.add_option(
            o7m.Option(
                key="d",
                short="Init Drift Detection",
                callback=self.init_drift_detection,
            )
        )
        obj.add_option(
            o7m.Option(key="p", short="Parameters", callback=self.update_template)
        )
        obj.add_option(
            o7m.Option(
                key="u", short="Update Template", callback=self.update_template_file
            )
        )
        obj.display_callback = self.display_single_stack
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_events(self):
        """Menu to view and edit a stack events for a stack"""

        self.max_events_per_page = 50

        obj = o7m.Menu(
            exit_option="b",
            title=f"Cloudformation Events in Stack: {self.stack_name}",
            title_extra=self.session_info(),
            compact=True,
        )
        obj.add_option(
            o7m.Option(
                key="a",
                short="All",
                callback=lambda: (setattr(self, "max_events_per_page", None)),
            )
        )
        obj.add_option(
            o7m.Option(key="int", short="Details", callback=print)  # Too be fix
        )

        obj.display_callback = self.display_events
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_resources(self):
        """Menu to view and edit stack resources fro a stack"""

        obj = o7m.Menu(
            exit_option="b",
            title=f"Cloudformation Resources for Stack: {self.stack_name}",
            title_extra=self.session_info(),
            compact=True,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                short="Raw",
                callback=lambda: pprint.pprint(self.resources),
            )
        )
        obj.add_option(
            o7m.Option(
                key="d", short="Show Drifters Details", callback=self.menu_drifters
            )
        )

        obj.display_callback = self.display_resources
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_drifters(self):
        """Menu to view and edit stack latest drifters"""

        obj = o7m.Menu(
            exit_option="b",
            title=f"Cloudformation Drifters for Stack: {self.stack_name}",
            title_extra=self.session_info(),
            compact=True,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                short="Raw",
                callback=lambda: pprint.pprint(self.drifters),
            )
        )

        obj.display_callback = self.display_drifters
        obj.loop()


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    Cloudformation(**kwargs).menu_stacks()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    Cloudformation().menu_stacks()

    # Cloudformation().upload_template('/gitcw/red-infra/pipeline-client-test/client-pipeline.yaml')
