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


# --------------------------------
#
# --------------------------------
import logging

import pandas as pd

from o7cli.base import Base

logger = logging.getLogger(__name__)

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html


# *************************************************
#
# *************************************************
class Sns(Base):
    """Class for SNS"""

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sns = self.session.client("sns")

    # *************************************************
    #
    # *************************************************
    def load_subcriptions(self, arn):
        """Load all subcriptions for a given topic ARN"""

        # print(f"Getting Subcription for Arn: {arn}")

        paginator = self.sns.get_paginator("list_subscriptions_by_topic")
        subs = []
        param = {"TopicArn": arn}

        for page in paginator.paginate(**param):
            subs.extend(page.get("Subscriptions", []))

        return pd.DataFrame(
            data=subs,
            columns=["Endpoint", "Owner", "Protocol", "SubscriptionArn", "TopicArn"],
        )


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", 40)

    the_subs = Sns().load_subcriptions(
        "arn:aws:sns:ca-central-1:038338722884:CES_GuardDuty"
    )
    print(the_subs)
