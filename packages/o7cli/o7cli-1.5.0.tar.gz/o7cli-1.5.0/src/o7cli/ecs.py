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
"""Module allows to view and access ECS Cluster, Services & Task"""


# How to bash into container
# https://aws.amazon.com/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/
# aws ecs --profile cw execute-command  `
#     --cluster dev-nlsb-service-ecs-cluster `
#     --region ca-central-1 `
#     --task 7f467e5b42d34d4cbfec6f6bb6a7b389 `
#     --container nlsb `
#     --command "/bin/bash" `
#     --interactive
# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.execute_command

# --------------------------------
#
# --------------------------------
import logging
import pprint
import subprocess

import o7util.input as o7i
import o7util.menu as o7m
from o7util.table import ColumnParam, Table, TableParam

from o7cli.base import Base

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class Ecs(Base):
    """Class for ECS for a Profile & Region"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#client

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = self.session.client("ecs")

        self.clusters: list = []
        self.cluster: dict = {}

        self.cluster_services: list = []
        self.cluster_instances: list = []
        self.cluster_tasks: list = []

        self.task: dict = {}

    # *************************************************
    #
    # *************************************************
    def load_clusters(self):
        """Returns all Clusters"""

        logger.info("load_clusters")

        paginator = self.client.get_paginator("list_clusters")
        self.clusters = []
        param = {}

        for page in paginator.paginate(**param):
            clusters_arns = page.get("clusterArns", [])

            if len(clusters_arns) == 0:
                break

            response = self.client.describe_clusters(
                clusters=clusters_arns,
                include=[
                    "ATTACHMENTS",
                    "CONFIGURATIONS",
                    "SETTINGS",
                    "STATISTICS",
                    "TAGS",
                ],
            )
            self.clusters.extend(response.get("clusters", []))

        return self

    # *************************************************
    #
    # *************************************************
    def load_services(self, cluster: str):
        """Returns all services for a Clusters"""

        logger.info(f"load_services for cluster : {cluster}")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_services.html
        paginator = self.client.get_paginator("list_services")
        param = {"cluster": cluster}
        self.cluster_services = []

        for page in paginator.paginate(**param):
            services_arns = page.get("serviceArns", [])

            if len(services_arns) == 0:
                break

            response = self.client.describe_services(
                cluster=cluster, services=services_arns
            )
            self.cluster_services.extend(response.get("services", []))

        return self

    # *************************************************
    #
    # *************************************************
    def load_instances(self, cluster: str):
        """Returns all instances for a clusters"""

        logger.info(f"load_instances for cluster : {cluster}")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_container_instances.html
        paginator = self.client.get_paginator("list_container_instances")
        param = {"cluster": cluster}
        self.cluster_instances = []

        for page in paginator.paginate(**param):
            instance_arns = page.get("containerInstanceArns", [])

            if len(instance_arns) == 0:
                break

            response = self.client.describe_container_instances(
                cluster=cluster, containerInstances=instance_arns
            )
            self.cluster_instances.extend(response.get("containerInstances", []))

        return self

    # *************************************************
    #
    # *************************************************
    def load_tasks(self, cluster: str):
        """Returns all tasks for a clusters"""

        logger.info(f"load_tasks for cluster : {cluster}")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_container_instances.html
        paginator = self.client.get_paginator("list_tasks")
        param = {"cluster": cluster}
        self.cluster_tasks = []

        for page in paginator.paginate(**param):
            task_arns = page.get("taskArns", [])

            if len(task_arns) == 0:
                break

            response = self.client.describe_tasks(cluster=cluster, tasks=task_arns)
            self.cluster_tasks.extend(response.get("tasks", []))

        for task in self.cluster_tasks:
            task["taskId"] = task.get("taskArn", "").split("/")[-1]

        return self

    # *************************************************
    #
    # *************************************************
    def display_clusters(self):
        """Display Clusters"""

        self.load_clusters()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="clusterName"),
                ColumnParam(
                    title="Status", type="str", data_col="status", format="aws-status"
                ),
                ColumnParam(
                    title="Running Task", type="int", data_col="runningTasksCount"
                ),
                ColumnParam(
                    title="Pending Task", type="int", data_col="pendingTasksCount"
                ),
                ColumnParam(title="Services", type="int", data_col="activeServicesCount"),
                ColumnParam(
                    title="Instances",
                    type="int",
                    data_col="registeredContainerInstancesCount",
                ),
            ]
        )
        print()
        Table(params, self.clusters).print()

        return self

    # *************************************************
    #
    # *************************************************
    def display_cluster(self):
        """Display Instances"""

        self.load_services(cluster=self.cluster.get("clusterName"))
        self.load_instances(cluster=self.cluster.get("clusterName"))
        self.load_tasks(cluster=self.cluster.get("clusterName"))

        print("")
        # pprint.pprint(self.cluster)
        # pprint.pprint(self.cluster_instances)

        print(f'Name: {self.cluster.get("clusterName", "")}')
        print(f'Status: {self.cluster["status"]}')
        print(f'Pending Tasks: {self.cluster["pendingTasksCount"]}')

        print("")
        print("List of Services")
        Table(
            TableParam(
                columns=[
                    ColumnParam(title="Name", type="str", data_col="serviceName"),
                    ColumnParam(
                        title="Status",
                        type="str",
                        data_col="status",
                        format="aws-status",
                    ),
                    ColumnParam(title="Desired", type="int", data_col="desiredCount"),
                    ColumnParam(title="Running", type="int", data_col="runningCount"),
                    ColumnParam(title="Pending", type="int", data_col="pendingCount"),
                    ColumnParam(title="Type", type="str", data_col="launchType"),
                ]
            ),
            self.cluster_services,
        ).print()

        print("")
        print("List of Instances")
        Table(
            TableParam(
                columns=[
                    ColumnParam(
                        title="Instance Id", type="str", data_col="ec2InstanceId"
                    ),
                    ColumnParam(
                        title="Status",
                        type="str",
                        data_col="status",
                        format="aws-status",
                    ),
                    ColumnParam(
                        title="Running", type="int", data_col="runningTasksCount"
                    ),
                    ColumnParam(
                        title="Pending", type="int", data_col="pendingTasksCount"
                    ),
                ]
            ),
            self.cluster_instances,
        ).print()

        print("")
        print("List of Tasks")
        Table(
            TableParam(
                columns=[
                    ColumnParam(title="id", type="i", min_width=4),
                    ColumnParam(title="Task Name", type="str", data_col="taskId"),
                    ColumnParam(
                        title="Status",
                        type="str",
                        data_col="lastStatus",
                        format="aws-status",
                    ),
                    ColumnParam(
                        title="Health",
                        type="str",
                        data_col="healthStatus",
                        format="aws-status",
                    ),
                    ColumnParam(title="CPU", type="int", data_col="cpu"),
                    ColumnParam(title="Memory", type="int", data_col="memory"),
                    ColumnParam(title="Stated", type="datetime", data_col="startedAt"),
                    ColumnParam(title="Type", type="str", data_col="launchType"),
                    ColumnParam(title="Zone", type="str", data_col="availabilityZone"),
                    ColumnParam(
                        title="ECS Exec", type="str", data_col="enableExecuteCommand"
                    ),
                ]
            ),
            self.cluster_tasks,
        ).print()

        print()
        print("List of Tags")
        Table(
            TableParam(
                columns=[
                    ColumnParam(title="Key", type="str", data_col="key"),
                    ColumnParam(title="Value", type="str", data_col="value"),
                ]
            ),
            self.cluster.get("tags", []),
        ).print()
        print()

    # *************************************************
    #
    # *************************************************
    def display_task(self):
        """Diplay Instances"""

        print("")
        # pprint.pprint(self.task)

        print("")
        print(f'Group: {self.task["group"]}')
        print(f'Status: {self.task["lastStatus"]}')
        print(f'Health: {self.task["healthStatus"]}')
        print(f'Started At: {self.task["startedAt"]}')

        print("")
        print(f'Launch Type: {self.task["launchType"]}')
        print(f'CPU: {self.task["cpu"]}')
        print(f'Memory: {self.task["memory"]}')

        print("")
        print(f'Availability Zone: {self.task["availabilityZone"]}')
        print(f'Exec Command Enabled: {self.task["enableExecuteCommand"]}')

        print("List of Containers")
        Table(
            TableParam(
                columns=[
                    ColumnParam(title="Name", type="str", data_col="name"),
                    ColumnParam(
                        title="Status",
                        type="str",
                        data_col="lastStatus",
                        format="aws-status",
                    ),
                    ColumnParam(title="Health", type="str", data_col="healthStatus"),
                    ColumnParam(title="Cpu", type="int", data_col="cpu"),
                ]
            ),
            self.task.get("containers", []),
        ).print()

        print("")

    # *************************************************
    #
    # *************************************************
    def command_in(self, task: dict, cmd="/bin/bash"):
        """Start a Shell inside a task contatiner"""

        cluster = task["clusterArn"].split("/")[-1]

        print("List of containers is task")
        containers = task.get("containers", [])
        for i, container in enumerate(containers):
            print(f'{i} -> {container["name"]}')

        key = o7i.input_int("Select container id : ")
        if key is None or key < 0 or key >= len(containers):
            return

        cmds = f"aws --region {self.session.region_name} ecs execute-command"
        cmds += f" --cluster {cluster} --task {task['taskId']} --container {containers[key]['name']}"
        cmds += f" --command {cmd} --interactive"

        print(f"Commands: {cmds}")
        subprocess.call(cmds.split(" "), shell=False)  # noqa: S603

    # *************************************************
    #
    # *************************************************
    def menu_task(self, index):
        """Task Detailed View"""

        if not 0 < index <= len(self.cluster_tasks):
            return self

        self.task = self.cluster_tasks[index - 1]

        obj = o7m.Menu(
            exit_option="b",
            title="ECS Service",
            title_extra=self.session_info(),
            compact=False,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Task",
                callback=lambda: pprint.pprint(self.task),
            )
        )
        obj.add_option(
            o7m.Option(
                key="a",
                name="Bash into a container",
                callback=lambda: self.command_in(task=self.task, cmd="/bin/bash"),
            )
        )
        obj.add_option(
            o7m.Option(
                key="s",
                name="Shell into a container",
                callback=lambda: self.command_in(task=self.task, cmd="/bin/sh"),
            )
        )

        obj.display_callback = self.display_task
        obj.loop()

        return self

    # *************************************************
    #
    # *************************************************
    def menu_cluster(self, index):
        """Single Cluster view"""

        if not 0 < index <= len(self.clusters):
            return self

        self.cluster = self.clusters[index - 1]

        obj = o7m.Menu(
            exit_option="b",
            title=f'ECS Cluster - {self.cluster.get("clusterName","na")}',
            title_extra=self.session_info(),
            compact=False,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Cluster",
                callback=lambda: pprint.pprint(self.cluster),
            )
        )
        obj.add_option(
            o7m.Option(
                key="rs",
                name="Display Raw Service",
                callback=lambda: pprint.pprint(self.cluster_services),
            )
        )
        obj.add_option(
            o7m.Option(
                key="ri",
                name="Display Raw Instances",
                callback=lambda: pprint.pprint(self.cluster_instances),
            )
        )
        obj.add_option(
            o7m.Option(
                key="rt",
                name="Display Raw Tasks",
                callback=lambda: pprint.pprint(self.cluster_tasks),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                name="Details for a Task",
                short="Details",
                callback=self.menu_task,
            )
        )

        obj.display_callback = self.display_cluster
        obj.loop()

        return self

    # *************************************************
    #
    # *************************************************
    def menu_clusters(self):
        """Instances view & edit menu"""

        obj = o7m.Menu(
            exit_option="b",
            title="ECS Clusters",
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.clusters),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                name="Details for a Cluster",
                short="Details",
                callback=self.menu_cluster,
            )
        )

        obj.display_callback = self.display_clusters
        obj.loop()

        return self


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    Ecs(**kwargs).menu_clusters()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    pprint.pprint(Ecs().menu_clusters().clusters)
    # ecs_obj = Ecs().menu_instances()
    # ecs_obj = Ec2().load_instance('i-01ba040ef1b4671da')
    # pprint.pprint(ec2_obj.instance_status)
    # Ec2().MenuInstances()
