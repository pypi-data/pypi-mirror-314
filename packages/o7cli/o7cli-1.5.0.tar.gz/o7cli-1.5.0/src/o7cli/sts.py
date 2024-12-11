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
"""Module for AWS Security Token Service (STS)"""

# --------------------------------
#
# --------------------------------
import logging

from o7cli.base import Base

logger = logging.getLogger(__name__)

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html


# *************************************************
#
# *************************************************
class Sts(Base):
    """Class for AWS Security Token Service (STS)"""

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sts = self.session.client("sts")

    # *************************************************
    #
    # *************************************************
    def get_account_id(self):
        """Get the account id"""

        resp = self.sts.get_caller_identity()
        ret = resp.get("Account")
        return ret
