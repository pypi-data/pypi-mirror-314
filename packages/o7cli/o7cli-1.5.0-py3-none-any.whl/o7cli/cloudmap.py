"""Cloud Map Module"""

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
import logging
import pprint

import o7util.menu as o7m
from o7util.table import ColumnParam, Table, TableParam

from o7cli.base import Base

logger = logging.getLogger(__name__)

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html


# *************************************************
#
# *************************************************
class CloudMap(Base):
    """Class to get Cloud Map Details"""

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = self.session.client("servicediscovery")

        self.namespaces = []
        self.namespace = []

        self.services = []
        self.service = []

        self.instances = []

    # *************************************************
    #
    # *************************************************
    def load_namespaces(self):
        """Load all namespaces in Region"""

        logger.info("load_namespaces")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stacks
        paginator = self.client.get_paginator("list_namespaces")
        self.namespaces = []
        param = {}

        for page in paginator.paginate(**param):
            self.namespaces.extend(page.get("Namespaces", []))

        logger.info(f"load_namespaces: Number of Namespace found {len(self.namespaces )}")

        return self

    # *************************************************
    #
    # *************************************************
    def load_services(self):
        """Load all services for active namespace"""

        logger.info("load_services")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stacks
        paginator = self.client.get_paginator("list_services")
        self.services = []
        param = {
            "Filters": [
                {
                    "Name": "NAMESPACE_ID",
                    "Values": [self.namespace.get("Id")],
                    "Condition": "EQ",
                }
            ]
        }

        for page in paginator.paginate(**param):
            self.services.extend(page.get("Services", []))

        logger.info(f"load_services: Number of Services found {len(self.services )}")

        return self

    # *************************************************
    #
    # *************************************************
    def load_instances(self):
        """Load all instances for a service"""

        logger.info("load_instances")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stacks
        paginator = self.client.get_paginator("list_instances")
        self.instances = []
        param = {"ServiceId": self.service.get("Id")}

        for page in paginator.paginate(**param):
            self.instances.extend(page.get("Instances", []))

        logger.info(f"load_services: Number of Instances found {len(self.instances )}")

        return self

    # *************************************************
    #
    # *************************************************
    def display_namespaces(self):
        """Display Instances"""

        self.load_namespaces()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="Name"),
                ColumnParam(title="Type", type="str", data_col="Type"),
                ColumnParam(title="ID", type="str", data_col="Id"),
                ColumnParam(title="Description", type="str", data_col="Description"),
            ]
        )
        print()
        Table(params, self.namespaces).print()

        return self

    # *************************************************
    #
    # *************************************************
    def display_services(self):
        """Display Services"""

        self.load_services()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="Name"),
                ColumnParam(title="Type", type="str", data_col="Type"),
                ColumnParam(title="ID", type="str", data_col="Id"),
                ColumnParam(title="Description", type="str", data_col="Description"),
            ]
        )
        print()
        Table(params, self.services).print()

        return self

    # *************************************************
    #
    # *************************************************
    def display_instances(self):
        """Display Instances"""

        self.load_instances()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="ID", type="str", data_col="Id"),
                ColumnParam(title="Attributes", type="str", data_col="Attributes"),
            ]
        )
        print()
        Table(params, self.instances).print()

        return self

    # *************************************************
    #
    # *************************************************
    def menu_instances(self, index):
        """Instances menu"""

        if not 0 < index <= len(self.services):
            return self

        self.service = self.services[index - 1]

        obj = o7m.Menu(
            exit_option="b",
            title=f'Instances for {self.service.get("Name","na")}',
            title_extra=self.session_info(),
            compact=False,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.instances),
            )
        )

        obj.display_callback = self.display_instances
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_services(self, index):
        """Services menu"""

        if not 0 < index <= len(self.namespaces):
            return self

        self.namespace = self.namespaces[index - 1]

        obj = o7m.Menu(
            exit_option="b",
            title=f'Services for {self.namespace.get("Name","na")}',
            title_extra=self.session_info(),
            compact=False,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.services),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                name="Instances for Service",
                short="Instances",
                callback=self.menu_instances,
            )
        )

        obj.display_callback = self.display_services
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_namespaces(self):
        """Namespaces  menu"""

        obj = o7m.Menu(
            exit_option="b",
            title="Namespaces",
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.namespaces),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                name="Services of a Namespace",
                short="Serivces",
                callback=self.menu_services,
            )
        )

        obj.display_callback = self.display_namespaces
        obj.loop()

        return self


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    CloudMap(**kwargs).menu_namespaces()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    # print(CloudMap().load_namespaces().namespaces)
    the_obj = CloudMap().menu_namespaces()
