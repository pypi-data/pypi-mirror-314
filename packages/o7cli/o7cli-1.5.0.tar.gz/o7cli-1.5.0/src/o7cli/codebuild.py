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
"""Module allows to view and access Codebuild"""

# --------------------------------
#
# --------------------------------
import logging
import pprint

import o7util.format as o7f
import o7util.input as o7i
import o7util.menu as o7m
import o7util.terminal as o7t
from o7util.table import ColumnParam, Table, TableParam

import o7cli.logstream
import o7cli.s3
from o7cli.base import Base

logger = logging.getLogger(__name__)

COLOR_HEADER = "\033[5;30;47m"
COLOR_END = "\033[0m"


# *************************************************
#
# *************************************************
class CodeBuild(Base):
    """Class for Codebuil for a Profile & Region"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#cloudformation

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.client = self.session.client("codebuild")

        self.projects = []
        self.project = None
        self.builds = []
        self.build = None

    # *************************************************
    #
    # *************************************************
    def load_projects(self):
        """Returns all LoadCodeBuilds for this Session"""

        logger.info("load_projects")

        self.projects = []
        param = {}

        paginator = self.client.get_paginator("list_projects")
        for page in paginator.paginate(**param):
            resp = self.client.batch_get_projects(names=page.get("projects", []))
            self.projects.extend(resp["projects"])

    # *************************************************
    #
    # *************************************************
    def refresh_project(self):
        """refresht the project details"""

        logger.info("refresh_project")

        resp = self.client.batch_get_projects(names=[self.project["name"]])
        self.project = resp["projects"][0]

    # *************************************************
    #
    # *************************************************
    def load_builds(self, max_builds=25):
        """Returns Details for Past Builds"""

        logger.info(f"load_builds {max_builds=}")

        self.builds = []

        param = {"projectName": self.project["name"], "sortOrder": "DESCENDING"}
        paginator = self.client.get_paginator("list_builds_for_project")
        for page in paginator.paginate(**param):
            left = max_builds - len(self.builds)
            # print(page)
            ids = page.get("ids", [])
            if len(ids) == 0:
                break

            resp = self.client.batch_get_builds(ids=ids[:left])
            self.builds.extend(resp["builds"])

            if len(self.builds) >= max_builds:
                break

        for build in self.builds:
            if "startTime" in build:
                if "endTime" in build:
                    build["diffTime"] = build["endTime"] - build["startTime"]
                else:
                    build["diffTime"] = build["startTime"]

    # *************************************************
    #
    # *************************************************
    def refresh_build_details(self):
        """Returns Execution Details of a Buiild"""

        exec_id = self.build["id"]
        logger.info(f"refresh_build_details {exec_id=}")

        param = {"ids": [exec_id]}
        response = self.client.batch_get_builds(**param)
        # pprint.pprint(response)

        if "builds" not in response:
            return None

        if len(response["builds"]) < 1:
            return None

        build = response["builds"][0]
        for phase in build.get("phases", []):
            phase["contextMessage"] = phase.get("contexts", [{}])[0].get("message", "")

        if "endTime" in build:
            build["diffTime"] = build["endTime"] - build["startTime"]

        self.build = build

    # *************************************************
    #
    # *************************************************
    def start_build(self):
        """Start a New Build"""

        if not o7i.is_it_ok("Confirm you want to start a new build"):
            return

        name = self.project["name"]
        logger.info(f"Start_builds {name=}")
        param = {"projectName": name}
        response = self.client.start_build(**param)
        pprint.pprint(response)

    # *************************************************
    #
    # *************************************************
    def update_env_variable(self, var_name, var_value):
        """Initialize the drift verification for a stack"""

        logger.info(f"update_env_variable: {var_name=} {var_value=}")

        environment = self.project.get("environment", {})
        found = False
        # Modify Env structure
        for env_var in environment.get("environmentVariables", []):
            if env_var["name"] == var_name:
                env_var["value"] = var_value
                found = True

        if found is False:
            logger.error(f"Update_env_variable: Variable: {var_name} was not found")
            return None

        param = {"name": self.project["name"], "environment": environment}
        # pprint.pprint(param)
        self.client.update_project(**param)
        # pprint.pprint(resp)

    # *************************************************
    #
    # *************************************************
    def edit_env_variable(self):
        """Edit Environment Variable"""

        env_id = o7i.input_int("Enter Env. Variable Id to Edit -> ")
        env_vars = self.project.get("environment", {}).get("environmentVariables", [])
        if env_id is None or len(env_vars) < env_id <= 0:
            print("Invalid Env Variable Id")
            return

        env_var = env_vars[env_id - 1]
        new_value = o7i.input_string(f'Enter new value for {env_var["name"]} -> ')

        if o7i.is_it_ok(f'Confirm that {env_var["name"]} -> {new_value}'):
            self.update_env_variable(env_var["name"], new_value)

    # *************************************************
    #
    # *************************************************
    def view_in_logstream(self):
        """View the logstream of the build"""

        logs = self.build.get("logs", {})
        o7cli.logstream.Logstream(
            log_group_name=logs.get("groupName", None),
            log_stream_name=logs.get("streamName", None),
            session=self.session,
        ).menu()

    # *************************************************
    #
    # *************************************************
    # def view_artifacts(self):
    #     """ View the artifacts of the build"""
    #     artifact_store = self.build.get('artifacts',{}).get('location',None)
    #     if artifact_store.startswith('arn:aws:s3:::'):
    #         artifact_store = artifact_store[len('arn:aws:s3:::'):]
    #         bucket = artifact_store.split('/')[0]
    #         folder = artifact_store[len(bucket)+1:]
    #         # o7cli.s3.S3(session = self.session).menu_folder(bucket=bucket, folder=folder)
    #     else:
    #         print('Artifacts is not an S3 bucket')
    #         o7i.wait_input()

    # *************************************************
    #
    # *************************************************
    def display_projects(self):
        """Displays a summary of Projects in a Table Format"""

        self.load_projects()

        print("")
        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="name"),
                ColumnParam(title="Creation", type="date", data_col="created"),
                ColumnParam(title="Description", type="str", data_col="description"),
            ]
        )
        Table(params, self.projects).print()

    # *************************************************
    #
    # *************************************************
    def display_project_details(self):
        """Displays the details of a project"""

        self.refresh_project()
        self.load_builds()

        # General Information
        print(f'Description: {self.project.get("description", "NA")}')
        print(f'Created: {self.project.get("created", None):%Y-%m-%d %H:%M:%S}')
        print(f'Modified: { o7f.elapse_time(self.project.get("lastModified", None))} ago')
        print(f'Tags: { self.project.get("tags", "None")}')

        print("")
        env = self.project.get("environment", {})
        print(f'Type: {env.get("type", "")}')
        print(f'Compute Type: {env.get("computeType", "")}')
        print(f'Image: {env.get("image", "")}')

        # Env Var
        print("Environment Variables")
        envvar_params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Type", type="str", data_col="type"),
                ColumnParam(title="Name", type="str", data_col="name"),
                ColumnParam(title="Value", type="str", data_col="value"),
            ]
        )
        Table(envvar_params, env.get("environmentVariables", [])).print()
        print("")
        print(f'Service Role: {self.project.get("serviceRole", "")}')
        print("")
        print(f"Last {len(self.builds)} builds")
        # Env Var
        past_build_params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Started", type="datetime", data_col="startTime"),
                ColumnParam(
                    title="Status",
                    type="str",
                    data_col="buildStatus",
                    format="aws-status",
                ),
                ColumnParam(title="Phase", type="str", data_col="currentPhase"),
                ColumnParam(title="Duration", type="since", data_col="diffTime"),
            ]
        )
        Table(past_build_params, self.builds).print()

    # *************************************************
    #
    # *************************************************
    def display_build_details(self):
        """Displays the details of a builds"""

        self.refresh_build_details()

        # General Information
        print(f'Project Name: {self.build.get("projectName", "NA")}')
        print(f'Start Time: {self.build.get("startTime", None):%Y-%m-%d %H:%M:%S}')
        print(f'Duration: {o7f.elapse_time(self.build.get("diffTime", None))}')
        print(f'Status: { o7t.format_aws_status(self.build.get("buildStatus", "NA"))}')
        print(f'Artifacts: {self.build.get("artifacts", {}).get("location", "")}')
        print("")
        env = self.build.get("environment", {})
        print(f'Type: {env.get("type", "")}   Compute: {env.get("computeType", "") }')

        # Env Var
        envvar_params = TableParam(
            title="Environment Variables",
            columns=[
                ColumnParam(title="Type", type="str", data_col="type"),
                ColumnParam(title="Name", type="str", data_col="name"),
                ColumnParam(title="Value", type="str", data_col="value"),
            ],
        )
        Table(envvar_params, env.get("environmentVariables", [])).print()

        print("")
        # Phases Status
        phase_params = TableParam(
            title="Build Phases",
            columns=[
                ColumnParam(title="Type", type="str", data_col="phaseType"),
                ColumnParam(title="Started", type="datetime", data_col="startTime"),
                ColumnParam(title="Sec.", type="str", data_col="durationInSeconds"),
                ColumnParam(
                    title="Status",
                    type="str",
                    data_col="phaseStatus",
                    format="aws-status",
                ),
                ColumnParam(title="Message", type="str", data_col="contextMessage"),
            ],
        )
        Table(phase_params, self.build.get("phases", [])).print()

        print("")
        # Phases Status
        export_params = TableParam(
            title="Exported Environment Variables",
            columns=[
                ColumnParam(title="id", type="i"),
                ColumnParam(title="Name", type="str", data_col="name"),
                ColumnParam(title="Value", type="str", data_col="value"),
            ],
        )
        Table(export_params, self.build.get("exportedEnvironmentVariables", [])).print()

    # *************************************************
    #
    # *************************************************
    def menu_build_details_exec_id(self, exec_id):
        """Menu to view details of a build"""

        self.builds = [{"id": exec_id}]
        self.menu_build_details(1)

    # *************************************************
    #
    # *************************************************
    def menu_build_details(self, index):
        """Menu to view details of a build"""

        if not 0 < index <= len(self.builds):
            return self

        self.build = self.builds[index - 1]

        obj = o7m.Menu(
            exit_option="b",
            title=f"Codebuild Build Detail for id : - {self.build['id']}",
            title_extra=self.session_info(),
            compact=True,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                short="Raw",
                callback=lambda: pprint.pprint(self.build),
            )
        )
        obj.add_option(
            o7m.Option(
                key="l",
                short="Logstream",
                callback=self.view_in_logstream,
            )
        )
        obj.add_option(
            o7m.Option(
                key="v",
                short="Build Spec",
                callback=lambda: print(
                    self.build.get("source", {}).get("buildspec", "NA")
                ),
            )
        )
        # obj.add_option(
        #     o7m.Option(
        #         key="a",
        #         short="Artifacts",
        #         callback=self.view_artifacts
        #     )
        # )
        obj.display_callback = self.display_build_details
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_project_details(self, index):
        """Menu to view details of a build"""

        if not 0 < index <= len(self.projects):
            return self

        self.project = self.projects[index - 1]

        obj = o7m.Menu(
            exit_option="b",
            title=f"Codebuild Project : - {self.project['name']}",
            title_extra=self.session_info(),
            compact=True,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                short="Raw",
                callback=lambda: pprint.pprint(self.project),
            )
        )
        obj.add_option(
            o7m.Option(
                key="v",
                short="Build Spec",
                callback=lambda: print(
                    self.project.get("source", {}).get("buildspec", "NA")
                ),
            )
        )
        obj.add_option(
            o7m.Option(
                key="e",
                short="Edit Var.",
                callback=self.edit_env_variable,
            )
        )
        obj.add_option(
            o7m.Option(
                key="s",
                short="Start",
                callback=self.start_build,
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                short="Build Details",
                callback=self.menu_build_details,
            )
        )
        obj.display_callback = self.display_project_details
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_projects(self):
        """Menu to view and edit all codebuild projects in current region"""

        obj = o7m.Menu(
            exit_option="b",
            title="CodeBuild Projects",
            title_extra=self.session_info(),
            compact=True,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                short="Raw",
                callback=lambda: pprint.pprint(self.projects),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                short="Execution Details",
                callback=self.menu_project_details,
            )
        )
        obj.display_callback = self.display_projects
        obj.loop()


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    CodeBuild(**kwargs).menu_projects()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    CodeBuild().menu_projects()
