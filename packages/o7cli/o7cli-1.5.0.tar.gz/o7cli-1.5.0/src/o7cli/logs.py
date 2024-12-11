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
"""Module allows to view and access Cloudwatch Logs"""

# --------------------------------
#
# --------------------------------
import logging
import pprint

import o7util.menu as o7m
from o7util.table import ColumnParam, Table, TableParam

import o7cli.logstream
from o7cli.base import Base

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class Logs(Base):
    """Class for Cloudwatch Logs for a Profile & Region"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = self.session.client("logs")

        self.log_groups: list = []

        self.log_group: dict = None
        self.log_streams: list = []

    # *************************************************
    #
    # *************************************************
    def load_log_groups(self):
        """Returns all Logs for this Session"""

        logger.info("load_log_groups")

        paginator = self.client.get_paginator("describe_log_groups")
        self.log_groups = []
        param = {}

        for page in paginator.paginate(**param):
            self.log_groups.extend(page.get("logGroups", []))

        return self

    # *************************************************
    #
    # *************************************************
    def load_log_streams(self, max_stream=25):
        """Returns all Logs Stream for the log groups"""

        logger.info("load_log_streams")

        paginator = self.client.get_paginator("describe_log_streams")
        self.log_streams = []
        param = {
            "logGroupName": self.log_group["logGroupName"],
            "orderBy": "LastEventTime",
            "descending": True,
        }

        for page in paginator.paginate(**param):
            self.log_streams.extend(page.get("logStreams", []))
            if max_stream and len(self.log_streams) >= max_stream:
                self.log_streams = self.log_streams[:max_stream]
                break

        return self

    # *************************************************
    #
    # *************************************************
    def display_log_groups(self):
        """Display Log Groups"""

        self.load_log_groups()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="logGroupName"),
                ColumnParam(title="Retention", type="str", data_col="retentionInDays"),
                ColumnParam(title="Stored Bytes", type="bytes", data_col="storedBytes"),
                ColumnParam(title="Created", type="datetime", data_col="creationTime"),
            ]
        )
        print()
        Table(params, self.log_groups).print()

        return self

    # *************************************************
    #
    # *************************************************
    def display_log_streams(self):
        """Display Log Groups"""

        self.load_log_streams()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="logStreamName"),
                ColumnParam(
                    title="First Event", type="datetime", data_col="firstEventTimestamp"
                ),
                ColumnParam(
                    title="Last Event", type="since", data_col="lastIngestionTime"
                ),
                ColumnParam(title="Stored Bytes", type="bytes", data_col="storedBytes"),
            ]
        )
        print()
        Table(params, self.log_streams).print()

        return self

    # *************************************************
    #
    # *************************************************
    def show_log_stream(self, index):
        """Show the content of a log stream"""

        if not 0 < index <= len(self.log_streams):
            return self

        log_stream = self.log_streams[index - 1]

        obj = o7cli.logstream.Logstream(
            log_group_name=self.log_group["logGroupName"],
            log_stream_name=log_stream["logStreamName"],
            session=self.session,
        )
        obj.menu()

    # *************************************************
    #
    # *************************************************
    def menu_log_streams(self, index=None, log_group_name=None):
        """Log Stream view"""

        if log_group_name:
            self.log_group = {"logGroupName": log_group_name}
        else:
            if not 0 < index <= len(self.log_groups):
                return self

            self.log_group = self.log_groups[index - 1]

        obj = o7m.Menu(
            exit_option="b",
            title=f'Log Stream - {self.log_group["logGroupName"]}',
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.log_streams),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                name="Details for a Log Stream",
                short="Details",
                callback=self.show_log_stream,
            )
        )

        obj.display_callback = self.display_log_streams
        obj.loop()

        return self

    # *************************************************
    #
    # *************************************************
    def menu_log_groups(self):
        """Instances view & edit menu"""

        obj = o7m.Menu(
            exit_option="b",
            title="Log Groups",
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.log_groups),
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                name="Details for a Log Group",
                short="Details",
                callback=self.menu_log_streams,
            )
        )

        obj.display_callback = self.display_log_groups
        obj.loop()

        return self


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    Logs(**kwargs).menu_log_groups()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    the_obj = Logs().menu_log_groups()

    # pprint.pprint(the_obj.log_groups)
