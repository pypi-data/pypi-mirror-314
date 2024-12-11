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
"""Module allows to view and access Cloudwatch Logs"""

# --------------------------------
#
# --------------------------------
import datetime
import logging
import pprint

import o7util.input as o7i
import o7util.menu as o7m

from o7cli.base import Base

logger = logging.getLogger(__name__)

# https://i.stack.imgur.com/6otvY.png
COLOR_HEADER = "\033[5;30;47m"
COLOR_LINE_NUMBER = "\033[0;30;46m"
COLOR_TIMESTAMP = "\033[0;36;40m"
COLOR_END = "\033[0m"


# *************************************************
#
# *************************************************
class Logstream(Base):
    """Class to access a Cloudwatch Logstream"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html

    # *************************************************
    #
    # *************************************************
    def __init__(self, log_group_name: str, log_stream_name: str, **kwargs):
        super().__init__(**kwargs)

        self.client = self.session.client("logs")

        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name

        self.events = []
        self.max_per_load = 2500
        self.from_head = True
        self.current = 0
        self.next_token = None
        self.prev_token = None
        self.is_last = False

        self.display_timestamp = False
        self.display_line_number = True

    # *************************************************
    #
    # *************************************************
    def load_logs_events(self):
        """Returns Log Events for Stream"""

        logger.info("Load_logs_events")

        param = {
            "logGroupName": self.log_group_name,
            "logStreamName": self.log_stream_name,
            "startFromHead": self.from_head,
        }

        if self.max_per_load is not None:
            param["limit"] = self.max_per_load

        done = False
        count = 0
        while not done:
            if self.from_head and self.next_token is not None:
                param["nextToken"] = self.next_token
            if not self.from_head and self.prev_token is not None:
                param["nextToken"] = self.prev_token

            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_log_events
            response = self.client.get_log_events(**param)
            # pprint.pprint(response)

            if "nextForwardToken" in response:
                self.next_token = response["nextForwardToken"]

            if "nextBackwardToken" in response:
                self.prev_token = response["nextBackwardToken"]

            # check if max per request is reach
            count += len(response["events"])
            if self.max_per_load is not None and count >= self.max_per_load:
                done = True

            # check if no more events are available
            if len(response["events"]) == 0:
                done = True

            logger.info(
                f'LoadLogsEvents: Number of events found {len(response["events"])}'
            )
            if self.from_head:
                self.events += response["events"]
            else:
                self.events = response["events"] + self.events

    # *************************************************
    # {'ingestionTime': 1632528987638,
    # 'message': '[Container] 2021/09/25 00:16:25 Entering phase POST_BUILD\n',
    # 'timestamp': 1632528987635},
    # {'ingestionTime': 1632528987638,
    # 'message': '[Container] 2021/09/25 00:16:25 Running command echo Test '
    #             'completed on `date`\n',
    # 'timestamp': 1632528987635},
    # {'ingestionTime': 1632528987638,
    # 'message': 'Test completed on Sat Sep 25 00:16:25 UTC 2021\n',
    # 'timestamp': 1632528987635},
    # *************************************************
    def dislay_events(self):
        """Convert Logs Event to Text"""

        number_width = len(str(len(self.events)))

        print(
            f"{COLOR_HEADER} Log Group: {self.log_group_name} --->> Log Stream: {self.log_stream_name} {COLOR_END}"
        )

        for i, event in enumerate(self.events):
            txt = ""

            if self.display_line_number:
                txt += f'{COLOR_LINE_NUMBER} {str(i + 1).ljust(number_width, " ")} {COLOR_END} '

            if self.display_timestamp:
                timestamp = datetime.datetime.fromtimestamp(
                    event.get("timestamp", 0) / 1000.0
                )
                txt += f"{COLOR_TIMESTAMP}[{timestamp:%Y-%m-%d %H:%M:%S}]{COLOR_END} "

            txt += event.get("message", "").strip()
            print(txt)

    # *************************************************
    #
    # *************************************************
    def log_stream_information(self):
        """Display informatio  about the Logs Event"""

        direction = ""
        if self.from_head is True:
            direction = f"First to {len(self.events)}"
        else:
            direction = f"{len(self.events)} to Last"

        return f"{COLOR_HEADER}{direction} | Max per Load: {self.max_per_load}{COLOR_END}"

    # *************************************************
    #
    # *************************************************
    def display_event_menu(self):
        """Display Menu for Events"""

        self.dislay_events()
        print(self.log_stream_information())

    def toggle_display_timestamp(self):
        """Toggle display timestamp"""
        self.display_timestamp = not self.display_timestamp

    def toggle_display_line_number(self):
        """Toggle display timestamp"""
        self.display_line_number = not self.display_line_number

    def set_max_per_load(self):
        """Set max per load"""
        self.max_per_load = o7i.input_int("Maximum Events per Load:")

    # *************************************************
    #
    # *************************************************
    def menu(self, fist_load=True):
        """Instances view & edit menu"""

        if fist_load:
            self.load_logs_events()

        obj = o7m.Menu(
            exit_option="b",
            title="Events !!! ",
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.events),
            )
        )

        obj.add_option(
            o7m.Option(
                key="l",
                name="Load More",
                short="Load More",
                wait=False,
                callback=self.load_logs_events,
            )
        )
        obj.add_option(
            o7m.Option(
                key="t",
                name="Timestamp",
                short="Timestamp",
                wait=False,
                callback=self.toggle_display_timestamp,
            )
        )
        obj.add_option(
            o7m.Option(
                key="n",
                name="Numbers",
                short="Numbers",
                wait=False,
                callback=self.toggle_display_line_number,
            )
        )
        obj.add_option(
            o7m.Option(
                key="m",
                name="Max",
                short="Max",
                wait=False,
                callback=self.set_max_per_load,
            )
        )

        obj.display_callback = self.display_event_menu
        obj.loop()

        return self


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )
