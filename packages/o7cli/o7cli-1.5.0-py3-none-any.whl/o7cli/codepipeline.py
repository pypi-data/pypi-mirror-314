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
"""Module allows to view and access Pipelines"""

# --------------------------------
#
# --------------------------------
import logging
import pprint

import botocore
import o7util.input as o7i
import o7util.menu as o7m
import o7util.terminal as o7t
from o7util.table import ColumnParam, Table, TableParam

import o7cli.codebuild
from o7cli.base import Base

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class CodePipeline(Base):
    """Class for Pipelines for a Profile & Region"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#cloudformation

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.client = self.session.client(
            "codepipeline",
            config=botocore.config.Config(connect_timeout=5, retries={"max_attempts": 0}),
        )

        self.pipelines = []

        self.pipeline_name = None
        self.pipeline = None

        self.executions = []
        self.execution_id = None
        self.execution = None

        self.action = None

        # https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html

    # *************************************************
    #
    # *************************************************
    def load_pipelines(self):
        """Returns all Pipelines for this Session"""

        logger.info("LoadPipelines")

        self.pipelines = []
        param = {}

        paginator = self.client.get_paginator("list_pipelines")
        for page in paginator.paginate(**param):
            self.pipelines.extend(page.get("pipelines", []))

        # Reformat some data
        # and get details
        for pipeline in self.pipelines:
            # Get status of the last Excution
            last_exec = self.get_executions(pipeline["name"], max_exec=1)
            pipeline["execStart"] = last_exec[0].get("startTime", "NA")
            pipeline["execStatus"] = last_exec[0].get("status", "NA")

    # *************************************************
    #
    # *************************************************
    def load_pipeline_details(self):
        """Returns Details for a Pipeline"""

        logger.info("load_pipeline_details")

        param = {"name": self.pipeline_name}
        resp_pl = self.client.get_pipeline(**param)
        resp_state = self.client.get_pipeline_state(**param)
        # pprint.pprint(resp_state)

        if "pipeline" not in resp_pl:
            return None

        if "stageStates" not in resp_state:
            return resp_pl["pipeline"]

        action_id = 1

        # Merge Stage & Action State
        for stage in resp_pl["pipeline"]["stages"]:
            # print(f'processing stage {stage["name"]}')
            stage["status"] = "na"

            for stage_state in resp_state["stageStates"]:
                if stage_state["stageName"] == stage["name"]:
                    # FOUND Stage
                    # print(f'  fOUND stage state->'); pprint.pprint(stage_state)

                    # LoadExecutionDetail

                    stage["latestExecution"] = stage_state.get("latestExecution", {})
                    stage["status"] = stage["latestExecution"].get("status", "")
                    stage["inboundTransitionState"] = stage_state.get(
                        "inboundTransitionState", {}
                    )

                    exec_id = stage["latestExecution"].get("pipelineExecutionId", None)
                    stage["latestExecutionDetails"] = self.get_execution_detail(
                        pl_name=self.pipeline_name, exec_id=exec_id
                    )

                    for action in stage["actions"]:
                        # print(f'  processing action {action["name"]}')
                        action["status"] = "na"
                        action["id"] = action_id
                        action_id += 1

                        for action_state in stage_state["actionStates"]:
                            if action_state["actionName"] == action["name"]:
                                # Found Action
                                action["latestExecution"] = action_state.get(
                                    "latestExecution", {}
                                )
                                action["status"] = action["latestExecution"].get(
                                    "status", "-"
                                )
                                action["statusDate"] = action["latestExecution"].get(
                                    "lastStatusChange", None
                                )
                                action["statusMsg"] = (
                                    action["latestExecution"]
                                    .get("errorDetails", {})
                                    .get("message", "")
                                )

        self.pipeline = resp_pl["pipeline"]

    # *************************************************
    #
    # *************************************************
    def load_execution_details(self):
        """Returns Details for a Pipeline Execution"""

        logger.info(f"LoadExecutionDetails {self.pipeline_name=} {self.execution_id=}")

        resp_exec = self.client.get_pipeline_execution(
            pipelineName=self.pipeline_name, pipelineExecutionId=self.execution_id
        )
        # pprint.pprint(resp_exec)

        if "pipelineExecution" not in resp_exec:
            return None

        details = resp_exec["pipelineExecution"]
        details["actions"] = []

        param = {
            "pipelineName": self.pipeline_name,
            "filter": {"pipelineExecutionId": self.execution_id},
        }

        resp_actions = self.client.list_action_executions(**param)
        # pprint.pprint(resp_actions)

        if "actionExecutionDetails" not in resp_actions:
            return details

        action_id = 1

        # # Merge Actions with summary
        for action in reversed(resp_actions["actionExecutionDetails"]):
            logger.info(f'{action_id}. {action["stageName"]=} {action["actionName"]=}')

            action["id"] = action_id
            action_id += 1
            details["actions"].append(action)

        self.execution = details

    # *************************************************
    #
    # *************************************************
    def get_executions(self, pl_name, max_exec=None):
        """Returns Execution Summaries for a Pipeline"""

        logger.info(f"get_executions for {pl_name} {max_exec=}")

        summaries = []
        param = {"pipelineName": pl_name}
        if max_exec is not None:
            param["maxResults"] = max_exec

        paginator = self.client.get_paginator("list_pipeline_executions")
        for page in paginator.paginate(**param):
            summaries.extend(page.get("pipelineExecutionSummaries", []))

            if len(summaries) >= max_exec:
                break

        # Reformat some data
        for summary in summaries:
            summary["sourceSummary"] = "No Source"
            source_revisions = summary.get("sourceRevisions", [])
            if len(source_revisions) >= 1:
                summary["sourceSummary"] = source_revisions[0].get(
                    "revisionSummary", "NA"
                )

            summary["sourceSummary"] = summary["sourceSummary"].replace("\n", " ").strip()

        return summaries

    # *************************************************
    #
    # *************************************************
    def set_approval_result(
        self, pl_name, stage_name, action_name, token, approved=False, reason=""
    ):
        """Set approval for a pending action"""

        logger.info(f"set_approval_result for {pl_name}")

        param = {
            "pipelineName": pl_name,
            "stageName": stage_name,
            "actionName": action_name,
            "result": {"summary": reason},
            "token": token,
        }

        if approved:
            param["result"]["status"] = "Approved"
        else:
            param["result"]["status"] = "Rejected"

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.put_approval_result
        response = self.client.put_approval_result(**param)

        return response.get("approvedAt", None)

    # *************************************************
    #
    # *************************************************
    def retry_fail_stage(self, pl_name, stage_name, exec_id):
        """Retry Falied Actin in a stage"""

        logger.info(f"retry_fail_stage for {pl_name=} {stage_name=} {exec_id=}")

        param = {
            "pipelineName": pl_name,
            "stageName": stage_name,
            "pipelineExecutionId": exec_id,
            "retryMode": "FAILED_ACTIONS",
        }

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.retry_stage_execution
        response = self.client.retry_stage_execution(**param)

        return response.get("pipelineExecutionId", None)

    # *************************************************
    #
    # *************************************************
    def start_execution(self):
        """Start a new Excution with the latest commit"""

        answer = o7i.is_it_ok("Confirm you want to start a Execution")
        if answer is False:
            return

        logger.info(f"start_execution for {self.pipeline_name}")
        param = {"name": self.pipeline_name}

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.retry_stage_execution
        response = self.client.start_pipeline_execution(**param)

        pprint.pprint(response.get("pipelineExecutionId", None))

    # *************************************************
    #
    # *************************************************
    def get_execution_detail(self, pl_name, exec_id=None):
        """Returns Execution Details"""

        logger.info(f"get_execution_detail: {pl_name=} {exec_id=}")

        if exec_id is None:
            return {}

        params = {"pipelineName": pl_name, "pipelineExecutionId": exec_id}

        try:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_pipeline_execution
            response = self.client.get_pipeline_execution(**params)
            # pprint.pprint(response)
        except self.client.exceptions.PipelineExecutionNotFoundException:
            return {}

        logger.info(f"get_execution_detail: {response=}")

        if "pipelineExecution" not in response:
            return {}

        return response["pipelineExecution"]

    # *************************************************
    #
    # *************************************************
    def display_pipelines(self):
        """Displays a summary of Pipelines in a Table Format"""

        self.load_pipelines()

        params = TableParam(
            # title= f"Pipelines List - {self.title_line()}",
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="name"),
                ColumnParam(title="Version", type="str", data_col="version"),
                ColumnParam(title="Creation", type="date", data_col="created"),
                ColumnParam(title="Updated", type="since", data_col="updated"),
                ColumnParam(title="Last Execution", type="since", data_col="execStart"),
                ColumnParam(
                    title="Status",
                    type="str",
                    data_col="execStatus",
                    format="aws-status",
                ),
            ]
        )
        Table(params, self.pipelines).print()

    # *************************************************
    #
    # *************************************************
    def display_pipeline_details(self):
        """Displays a summary of Pipelines in a Table Format"""

        self.load_pipeline_details()

        print(f'Version: {self.pipeline.get("version", "NA")}')
        print(f'Role: {self.pipeline.get("roleArn", "NA")}')

        artifact_store = self.pipeline.get("artifactStore", {})
        str_location = f'Location: {artifact_store.get("location", "NA")}'
        print(
            f'Artifact Store Type: {artifact_store.get("type", "NA")}  -> {str_location}'
        )

        stages = self.pipeline.get("stages", [])
        stage_params = TableParam(
            columns=[
                ColumnParam(data_col="id", title="id", type="int", fix_width=4),
                ColumnParam(data_col="name", title="Name", type="str"),
                ColumnParam(data_col="runOrder", title="Order", type="int"),
                ColumnParam(
                    data_col="status", title="Status", type="str", format="aws-status"
                ),
                ColumnParam(
                    data_col="statusDate",
                    title="Updated",
                    type="since",
                    format="aws-status",
                ),
                ColumnParam(
                    data_col="statusMsg",
                    title="Message",
                    type="str",
                    format="aws-status",
                ),
            ]
        )

        for stage in stages:
            # Check if Inbound Allowed
            if "inboundTransitionState" in stage:
                allowed = stage["inboundTransitionState"].get("enabled", True)
                if allowed:
                    print(" | ")
                else:
                    reason = stage["inboundTransitionState"].get("disabledReason", "NA")
                    print(f" X  Disable Reason: {reason}")

            status = o7t.format_aws_status(stage.get("status", "-"))
            exec_id = stage.get("latestExecution", {}).get("pipelineExecutionId", "-")

            rev_summry = []
            for rev in stage.get("latestExecutionDetails", {}).get(
                "artifactRevisions", []
            ):
                rev_summry.append(rev.get("revisionSummary", "NA").split("\n")[0].strip())
            rev_summry = " / ".join(rev_summry)

            print(
                f"Stage: {stage.get('name', '-')}  Execution ID: {exec_id} ({rev_summry})"
            )
            print(f"Status: {status} ")

            Table(stage_params, stage.get("actions", [])).print()

    # *************************************************
    #
    # *************************************************
    def display_executions(self):
        """Displays a summary of Pipelines Executions in a Table Format"""

        self.executions = self.get_executions(self.pipeline_name, max_exec=25)

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(
                    title="Execution Id", type="str", data_col="pipelineExecutionId"
                ),
                ColumnParam(
                    title="Status", type="str", data_col="status", format="aws-status"
                ),
                ColumnParam(title="Started", type="datetime", data_col="startTime"),
                ColumnParam(title="Updated", type="since", data_col="lastUpdateTime"),
                ColumnParam(title="Summary", type="str", data_col="sourceSummary"),
            ]
        )
        Table(params, self.executions).print()

    # *************************************************
    #
    # *************************************************
    def display_execution_details(self):
        """Displays a Details of a pipeline execution"""

        self.load_execution_details()

        print(f'ExecId : {self.execution.get("pipelineExecutionId", "-")}')

        status = o7t.format_aws_status(self.execution.get("status", "-"))
        print(f'Status: {status} ({self.execution.get("statusSummary", "-")})')
        print(f'Version: {self.execution.get("pipelineVersion", "NA")}')

        print("Artefacts")

        artefact_params = TableParam(
            columns=[
                ColumnParam(data_col="name", title="Name", type="str"),
                ColumnParam(
                    data_col="revisionSummary", title="Revision Summary", type="str"
                ),
            ]
        )
        Table(artefact_params, self.execution.get("artifactRevisions", [])).print()

        print("")
        print("Actions")
        actions = self.execution.get("actions", [])

        # Compile for Action variables
        output_variables = []
        for action in actions:
            action["fullName"] = (
                f"{action.get('stageName', '')}.{action.get('actionName', '')}"
            )

            action["diffTime"] = None
            if "startTime" in action and "lastUpdateTime" in action:
                action["diffTime"] = action["lastUpdateTime"] - action["startTime"]

            namespace = action.get("input", {}).get("namespace", "")

            action_output = action.get("output", {}).get("outputVariables", {})
            for output_key in action_output.keys():
                output_variables.append(
                    {
                        "action": action["actionName"],
                        "name": f"{namespace}.{output_key}",
                        "value": action_output[output_key],
                    }
                )

        action_params = TableParam(
            columns=[
                ColumnParam(data_col="id", title="id", type="int", fix_width=4),
                ColumnParam(data_col="fullName", title="Name", type="str"),
                ColumnParam(
                    data_col="status",
                    title="Status",
                    type="str",
                    fix_width=10,
                    format="aws-status",
                ),
                ColumnParam(data_col="startTime", title="Started", type="datetime"),
                ColumnParam(data_col="diffTime", title="Duration", type="since"),
                ColumnParam(
                    data_col="lastUpdateTime", title="Last Updated", type="since"
                ),
            ]
        )
        Table(action_params, actions).print()

        print("")
        print("Output Variables")
        outvar_params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", fix_width=4),
                ColumnParam(data_col="action", title="Action", type="str"),
                ColumnParam(data_col="name", title="Name", type="str"),
                ColumnParam(data_col="value", title="Value", type="str"),
            ]
        )
        Table(outvar_params, output_variables).print()

    # *************************************************
    #
    # *************************************************
    def menu_pipelines(self):
        """Menu to view and edit all pipelines in current region"""

        obj = o7m.Menu(
            exit_option="b",
            title="Pipelines List",
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                short="Raw",
                callback=lambda: pprint.pprint(self.pipelines),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                short="Details",
                callback=self.menu_pipeline_details,
            )
        )

        obj.display_callback = self.display_pipelines
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_action_details(self, index):
        """Menu to view and act on a Action"""

        self.action = None

        # Find Action
        for stage in self.pipeline.get("stages", []):
            for action in stage.get("actions", []):
                if action["id"] == index:
                    stage_name = stage.get("name", "")
                    pipeline_exec_id = stage.get("latestExecution", {}).get(
                        "pipelineExecutionId", "na"
                    )
                    self.action = action

        if self.action is None:
            return

        print("--- Action Details ---")
        print(f"Pipeline Exec ID: {pipeline_exec_id}")
        pprint.pprint(self.action)

        status = self.action.get("status", "")
        action_cat = self.action.get("actionTypeId", {}).get("category", "")
        action_provider = self.action.get("actionTypeId", {}).get("provider", "")

        external_execution_id = self.action.get("latestExecution", {}).get(
            "externalExecutionId", None
        )

        if (
            action_provider == "Manual"
            and status == "InProgress"
            and action_cat == "Approval"
        ):
            key = o7i.input_string("Option -> Approve(a) Reject(r) Back (any other) :")
            if key != "a" and key != "r":
                return

            txt = "Rejection"
            approved = False
            if key == "a":
                txt = "Approval"
                approved = True

            reason = o7i.input_string(f"Reason for {txt} :")
            if len(reason) < 1:
                return

            token = self.action.get("latestExecution", {}).get("token", "")
            self.set_approval_result(
                pl_name=self.pipeline_name,
                stage_name=stage_name,
                action_name=self.action.get("name", ""),
                token=token,
                approved=approved,
                reason=reason,
            )

        if status == "Failed":
            if action_provider == "CodeBuild":
                key = o7i.input_string("Option -> Retry(r) Details(d) Back (any) :")
            else:
                key = o7i.input_string("Option -> Retry(r) Back (any) :")

            if key == "r":
                self.retry_fail_stage(
                    pl_name=self.pipeline_name,
                    stage_name=stage_name,
                    exec_id=pipeline_exec_id,
                )
            elif key == "d":
                o7cli.codebuild.CodeBuild(
                    session=self.session
                ).menu_build_details_exec_id(exec_id=external_execution_id)

        elif action_provider == "CodeBuild":
            key = o7i.input_string("Option -> Details(d) Back (any) :")
            if key == "d":
                o7cli.codebuild.CodeBuild(
                    session=self.session
                ).menu_build_details_exec_id(exec_id=external_execution_id)

    # *************************************************
    #
    # *************************************************
    def print_execution_details_raw(self, index):
        """Print raw details of an action in an execution"""
        if not 0 < index <= len(self.execution["actions"]):
            return

        pprint.pprint(self.execution["actions"][index - 1])
        o7i.wait_input()

    # *************************************************
    #
    # *************************************************
    def menu_execution_details(self, index):
        """Menu to view details of a pipeline execution"""

        if not 0 < index <= len(self.executions):
            return self

        self.execution_id = self.executions[index - 1]["pipelineExecutionId"]

        obj = o7m.Menu(
            exit_option="b",
            title=f"Execution Details for Pipeline {self.pipeline_name}",
            title_extra=self.session_info(),
            compact=True,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                short="Raw",
                callback=lambda: pprint.pprint(self.execution),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                short="Raw Action",
                callback=self.print_execution_details_raw,
            )
        )
        obj.display_callback = self.display_execution_details
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_executions(self):
        """Menu to view execution list of a pipeline"""

        obj = o7m.Menu(
            exit_option="b",
            title=f"Pipeline Executions History - {self.pipeline_name}",
            title_extra=self.session_info(),
            compact=True,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                short="Raw",
                callback=lambda: pprint.pprint(self.executions),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                short="Execution Details",
                callback=self.menu_execution_details,
            )
        )
        obj.display_callback = self.display_executions
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_pipeline_details(self, index):
        """Menu to view and edit a specific pipeline"""

        if not 0 < index <= len(self.pipelines):
            return self

        self.pipeline_name = self.pipelines[index - 1]["name"]

        obj = o7m.Menu(
            exit_option="b",
            title=f"Pipeline - {self.pipeline_name}",
            title_extra=self.session_info(),
            compact=True,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                short="Raw",
                callback=lambda: pprint.pprint(self.pipeline),
            )
        )
        obj.add_option(
            o7m.Option(key="e", short="Executions List", callback=self.menu_executions)
        )
        obj.add_option(o7m.Option(key="s", short="Start", callback=self.start_execution))
        obj.add_option(
            o7m.Option(
                key="int",
                short="Action Details",
                callback=self.menu_action_details,
            )
        )
        obj.display_callback = self.display_pipeline_details
        obj.loop()


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    CodePipeline(**kwargs).menu_pipelines()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    CodePipeline().menu_pipelines()
