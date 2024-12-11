"""AWS RDS Module"""

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

# --------------------------------
#
# --------------------------------
import datetime
import logging
import pprint

import o7util.menu as o7m
from o7util.table import ColumnParam, Table, TableParam

from o7cli.base import Base

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class Rds(Base):
    """Class to manage RDS"""

    #  https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#rds

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = self.session.client("rds")

        self.db_instances: list = []
        self.db_instance: dict = {}

    # *************************************************
    #
    # *************************************************
    def load_db_instances(self):
        """Load DB Instances"""

        logger.info("load_db_instances")

        paginator = self.client.get_paginator("describe_db_instances")
        self.db_instances = []
        param = {}

        for page in paginator.paginate(**param):
            self.db_instances.extend(page.get("DBInstances", []))

        return self

    # *************************************************
    #
    # *************************************************
    def load_db_instance(self, db_instance_id: str):
        """Load a specific instance"""

        logger.info(f"load_db_instance: {db_instance_id}")

        response = self.client.describe_db_instances(DBInstanceIdentifier=db_instance_id)
        self.db_instance = response["DBInstances"][0]

        return self

    # *************************************************
    #
    # *************************************************
    def view_cpu_utilization(self):
        """View CPU Utilization"""

        db_id = self.db_instance.get("DBInstanceIdentifier")

        cloudwatch = self.session.resource("cloudwatch")
        metric = cloudwatch.Metric("AWS/RDS", "CPUUtilization")
        metric.load()

        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(days=14)

        param = {
            "Dimensions": [{"Name": "DBInstanceIdentifier", "Value": db_id}],
            "Statistics": ["Average", "Minimum", "Maximum"],
            "StartTime": start,
            "EndTime": end,
            "Period": 3600 * 24,
        }

        logger.info(f"LoadCpuUtilization: param: {param}")

        resp = metric.get_statistics(**param)

        # pprint.pprint(resp)

        data_point = resp.get("Datapoints", [])

        params = TableParam(
            columns=[
                ColumnParam(title="Date / Time", type="datetime", data_col="Timestamp"),
                ColumnParam(title="Average", type="str", data_col="Average"),
                ColumnParam(title="Maximum", type="str", data_col="Maximum"),
            ]
        )
        print()
        Table(params, data_point).print()

    # *************************************************
    #
    # *************************************************
    def display_db_instances(self):
        """Display Instances"""

        self.load_db_instances()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(
                    title="Instance Id", type="str", data_col="DBInstanceIdentifier"
                ),
                ColumnParam(title="Name", type="str", data_col="DBName"),
                ColumnParam(title="Class", type="str", data_col="DBInstanceClass"),
                ColumnParam(title="Env. V", type="str", data_col="EngineVersion"),
                ColumnParam(title="AZ", type="str", data_col="AvailabilityZone"),
                ColumnParam(title="Multi-AZ", type="str", data_col="MultiAZ"),
                ColumnParam(
                    title="State",
                    type="str",
                    data_col="DBInstanceStatus",
                    format="aws-state",
                ),
            ]
        )
        print()
        Table(params, self.db_instances).print()

        return self

    # *************************************************
    #
    # *************************************************
    def display_db_instance(self):
        """Display Instances"""

        self.load_db_instance(self.db_instance.get("DBInstanceIdentifier", "na"))

        print("")

        print(f'Cluster Id: {self.db_instance.get("DBClusterIdentifier", "")}')
        print(f'Instance Id: {self.db_instance.get("DBInstanceIdentifier", "")}')
        print(f'Status: {self.db_instance.get("DBInstanceStatus", "")}')
        print()
        print(f'Engine Version: {self.db_instance.get("EngineVersion", "")}')
        print(f'Engine: {self.db_instance.get("Engine", "")}')
        print(f'Class: {self.db_instance.get("DBInstanceClass", "")}')
        print(f'Storage Type: {self.db_instance.get("StorageType", "")}')
        print()
        print(f'DB Name: {self.db_instance.get("DBName", "")}')
        print(f'Multi-AZ: {self.db_instance.get("MultiAZ", "")}')

        print()
        print(f'Endpoint: {self.db_instance.get("Endpoint", {}).get("Address", "")}')
        print(f'Port: {self.db_instance.get("Endpoint", {}).get("Port", "")}')
        print()
        print(f'CA Certificate: {self.db_instance.get("CACertificateIdentifier","na")}')

        print()
        Table(
            TableParam(
                title="Tags",
                columns=[
                    ColumnParam(title="Key", type="str", data_col="Key"),
                    ColumnParam(title="Value", type="str", data_col="Value"),
                ],
            ),
            self.db_instance.get("TagList", []),
        ).print()
        print()

    # *************************************************
    #
    # *************************************************
    def menu_db_instance(self, index):
        """DB Instances view & edit menu"""

        if not 0 < index <= len(self.db_instances):
            return self

        self.db_instance = self.db_instances[index - 1]

        obj = o7m.Menu(
            exit_option="b",
            title=f'DB Instance - {self.db_instance.get("DBName","na")}',
            title_extra=self.session_info(),
            compact=False,
        )
        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                callback=lambda: pprint.pprint(self.db_instance),
            )
        )
        obj.add_option(
            o7m.Option(key="c", name="CPU Usage", callback=self.view_cpu_utilization)
        )

        obj.display_callback = self.display_db_instance
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_db_instances(self):
        """DB Instances view & edit menu"""

        obj = o7m.Menu(
            exit_option="b",
            title="RDS DB Instances",
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.db_instances),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                name="Details for an Instance",
                short="Details",
                wait=True,
                callback=self.menu_db_instance,
            )
        )

        obj.display_callback = self.display_db_instances
        obj.loop()

        return self


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    Rds(**kwargs).menu_db_instances()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    the_obj = Rds().menu_db_instances()

    # pprint.pprint(the_obj.db_instances)
