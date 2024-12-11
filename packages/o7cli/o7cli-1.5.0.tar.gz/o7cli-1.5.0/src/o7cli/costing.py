"""Module to explore AWS costs"""

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
import os

import botocore.exceptions
import o7util.input as o7i  # noqa: F401
import o7util.menu as o7m
import o7util.pandas as o7p
import o7util.report as o7r  # noqa: F401
import o7util.terminal as o7t
import pandas as pd

# import o7cli.cloudwatch
import o7cli.organizations as o7org
from o7cli.base import Base

try:
    import o7pdf.report_aws_cost as o7rac
except ImportError:
    # warnings.warn(f'Error importing o7pdf.report_security_hub_standard: {exept}')
    _has_o7pdf = False
else:
    _has_o7pdf = True

pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class Costing(Base):
    """Class to Explore AWS costs"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.client = self.session.client(
            "ce",
            config=botocore.config.Config(connect_timeout=5, retries={"max_attempts": 0}),
        )

        self.df_accounts = None
        self.tags = None
        self.common_filter = {
            "And": [
                {
                    "Not": {
                        "Dimensions": {
                            "Key": "RECORD_TYPE",
                            "Values": ["Credit", "Refund"],
                            "MatchOptions": ["EQUALS"],
                        }
                    }
                },
                {
                    "Not": {
                        "Dimensions": {
                            "Key": "SERVICE",
                            "Values": ["Tax"],
                            "MatchOptions": ["EQUALS"],
                        }
                    }
                },
            ]
        }

        self.cost_metric = "NetAmortizedCost"
        self.granularity = "DAILY"
        self.periods = 30
        self.group_type: str = "DIMENSION"
        self.group_key: str = "LINKED_ACCOUNT"
        self.filters: list = []

        self._last_update_hash = None

        self.show_day_summary = True

        self.df_costs_totals: pd.DataFrame = None
        self.df_usage_details: pd.DataFrame = None
        self.df_usage_summary: pd.DataFrame = None

    # *************************************************
    #
    # *************************************************
    def get_cost_from_aws(
        self, group_by: list = None, filters: dict = None
    ) -> pd.DataFrame:
        """Get all pages of Cost and Usage"""

        now = datetime.datetime.now()

        days = self.periods + 0.5
        days = days * 31 if self.granularity == "MONTHLY" else days
        date_start = (now - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        date_end = now.strftime("%Y-%m-%d")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_cost_and_usage.html
        params = {
            "Granularity": self.granularity,
            "TimePeriod": {"Start": date_start, "End": date_end},
            "Metrics": [self.cost_metric],
        }

        if group_by:
            params["GroupBy"] = group_by

        if filters:
            params["Filter"] = filters

        logger.info(f"Getting AWS Total Cost from {date_start} to {date_end}")

        results = []

        while True:
            response = self.client.get_cost_and_usage(**params)
            results.extend(response["ResultsByTime"])

            if "NextPageToken" in response:
                params["NextPageToken"] = response["NextPageToken"]
            else:
                break

        # pprint.pprint(results)

        # Process all entries to store in Pandas dataframe
        costs = []
        for result in results:
            dt_date = datetime.date.fromisoformat(result["TimePeriod"]["Start"])
            for group in result.get("Groups", []):
                record = {
                    "date": dt_date,
                    "amount": float(group["Metrics"][self.cost_metric]["Amount"]),
                    "unit": group["Metrics"][self.cost_metric].get("Unit", "USD"),
                }
                for i, grp in enumerate(group_by):
                    record[grp["Key"]] = (
                        group["Keys"][i].removeprefix(f"{self.group_key}$")
                        if self.group_type == "TAG"
                        else group["Keys"][i]
                    )

                costs.append(record)

            total = result.get("Total", {}).get(self.cost_metric, None)
            if total:
                record = {
                    "date": dt_date,
                    "total": float(total["Amount"]),
                    "unit": total.get("Unit", "USD"),
                }

                costs.append(record)

        df = pd.DataFrame(data=costs)
        return df

    # *************************************************
    #
    # *************************************************
    def load_accounts(self):
        """Get list of accounts"""

        if self.df_accounts is None:
            try:
                self.df_accounts = pd.DataFrame(
                    o7org.Organizations(session=self.session).load_accounts().accounts
                )
            except botocore.exceptions.ClientError:
                logger.info("Not allowed to list accounts for organization")

                self.df_accounts = pd.DataFrame(
                    [
                        {
                            "Id": self.session.client("sts")
                            .get_caller_identity()
                            .get("Account"),
                            "Name": "Current Account",
                            "Status": "ACTIVE",
                        }
                    ]
                )

            for col in self.df_accounts:
                if pd.api.types.is_datetime64tz_dtype(self.df_accounts[col]):
                    self.df_accounts[col] = self.df_accounts[col].dt.tz_localize(None)

        return self.df_accounts

    # *************************************************
    #
    # *************************************************
    def load_tags(self):
        """Load cost of tags"""

        if self.tags is not None:
            return self.tags

        # print(f"Getting AWS Cost Tags")
        now = datetime.datetime.now()
        date_start = (now - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        date_end = now.strftime("%Y-%m-%d")

        self.tags = []
        param = {
            "TimePeriod": {"Start": date_start, "End": date_end},
        }
        response = self.client.get_tags(**param)

        self.tags.extend(response.get("Tags", []))

        return self.tags

    # *************************************************
    #
    # *************************************************
    def load_cost_totals(self) -> pd.DataFrame:
        """Get Cost information without grouping"""

        df = self.get_cost_from_aws(
            group_by=[{"Type": "DIMENSION", "Key": "RECORD_TYPE"}],
            filters={
                "Not": {
                    "Dimensions": {
                        "Key": "SERVICE",
                        "Values": ["Tax"],
                        "MatchOptions": ["EQUALS"],
                    }
                }
            },
        )
        # df = df.set_index(["date"])
        self.df_costs_totals = df.tail(self.periods)

        print(self.df_costs_totals)

        return self

    # *************************************************
    #
    # *************************************************
    def load_usage_details(self) -> pd.DataFrame:
        """Get Cost information without grouping"""

        group_by = [{"Type": self.group_type, "Key": self.group_key}]

        df = self.get_cost_from_aws(group_by=group_by, filters=self.get_specific_filter())

        # Set the group_key as a column
        df = df.set_index(["date", self.group_key])
        df = df["amount"].unstack(level=-1)
        # df = df.fillna(0.0).groupby("Date").sum()
        df = df.fillna(0.0)

        # Sort columns by total cost
        sorted_columns = df.sum().sort_values(ascending=False).index
        self.df_usage_details = df[sorted_columns].tail(self.periods)

        return self

    # *************************************************
    #
    # *************************************************
    def update_usage(self) -> pd.DataFrame:
        # self.load_cost_totals()

        update_hash = hash(
            str(
                [
                    self.cost_metric,
                    self.granularity,
                    self.periods,
                    self.group_type,
                    self.group_key,
                    self.filters,
                ]
            )
        )

        # Only update if needed
        if self._last_update_hash != update_hash:
            self.load_usage_details()
            self._last_update_hash = update_hash

        # Process the details to get a summary
        self.df_usage_summary = self.summarize_usage(self.df_usage_details)

        # For Linked Account, add the account name
        if self.group_key == "LINKED_ACCOUNT":
            df_accounts = self.load_accounts()
            self.df_usage_summary = pd.merge(
                left=self.df_usage_summary,
                left_on="LINKED_ACCOUNT",
                right=df_accounts[["Id", "Name"]],
                right_on="Id",
                how="left",
            )
            self.df_usage_summary = self.df_usage_summary.drop("Id", axis=1)

            # Set account name in the 2nd colum
            columns = self.df_usage_summary.columns.tolist()
            last_column = columns.pop(-1)
            columns.insert(1, last_column)
            self.df_usage_summary = self.df_usage_summary[columns]

    # *************************************************
    # {'Dimensions': {'Key': 'LINKED_ACCOUNT', 'Values': ['625257959362'], 'MatchOptions': ['EQUALS']}}
    # {'Tags':        {'Key': 'Project', 'Values': ['dev'], 'MatchOptions': ['EQUALS']}}
    # *************************************************
    def filters_str(self) -> str:
        """Return a string that represent the filters"""

        if len(self.filters) == 0:
            return "All"

        rets = []
        for _filter in self.filters:
            if "Dimensions" in _filter:
                rets.append(
                    f"{_filter['Dimensions']['Key']}={_filter['Dimensions']['Values'][0]}"
                )
            if "Tags" in _filter:
                rets.append(f"{_filter['Tags']['Key']}={_filter['Tags']['Values'][0]}")

        return ",".join(rets)

    # *************************************************
    #
    # *************************************************
    def get_specific_filter(self) -> dict:
        """Return a copy of the filter (commons and added by user)"""

        ret = self.common_filter.copy()
        ret["And"].extend(self.filters.copy())
        return ret

    # *************************************************
    #
    # *************************************************
    def summarize_usage(self, df_usage: pd.DataFrame) -> pd.DataFrame:
        """Compile cost by group"""

        # -----------------------
        # Max number of days
        # -----------------------
        days = (datetime.date.today() - df_usage.index.min()).days
        # print(f"Compile for {days} days")

        columns = {
            "Total": f"{days} Day Sum",
            "Avr": f"{days} Day Avr",
            "Max": f"{days} Day Max",
        }
        sort_key = f"{days} Day Sum"

        df_daily = df_usage.stack().reset_index()
        df_daily.columns = ["date", self.group_key, "cost"]
        df_daily.set_index("date", inplace=True)
        # print(df_daily)

        # -----------------------
        # Compile on full range
        # -----------------------
        day_30_costs = df_daily.groupby(self.group_key).agg(
            Total=("cost", "sum"), Max=("cost", "max"), Avr=("cost", "mean")
        )
        day_30_costs = day_30_costs.rename(columns=columns)
        # print(day_30_costs)

        # -----------------------
        # Compile on 7 days
        # -----------------------
        day7 = datetime.date.today() - datetime.timedelta(days=8)
        columns = {"Total": "7 Day Sum", "Avr": "7 Day Avr"}

        day_7_costs = df_daily.loc[day7:]
        day_7_costs = day_7_costs.groupby(self.group_key).agg(
            Total=("cost", "sum"), Avr=("cost", "mean")
        )
        day_7_costs = day_7_costs.rename(columns=columns)
        # print(day_7_costs)

        # -----------------------
        # Compile on last day
        # -----------------------
        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        columns = {"Total": "Yesterday"}
        yesterday_costs = df_daily.loc[yesterday:]
        yesterday_costs = (
            yesterday_costs.groupby(self.group_key)
            .agg(Total=("cost", "sum"))
            .rename(columns=columns)
        )
        # print(yesterday_costs)

        summarized_costs = pd.concat(
            [day_30_costs, day_7_costs, yesterday_costs], axis=1, join="outer"
        )
        summarized_costs = summarized_costs.sort_values(by=[sort_key], ascending=False)
        summarized_costs = summarized_costs.reset_index()

        return summarized_costs

    # *************************************************
    #
    # *************************************************
    def set_group_dimension(self, dimension: str):
        self.group_type = "DIMENSION"
        self.group_key = dimension
        return self

    # *************************************************
    #
    # *************************************************
    def to_excel(self):
        filename = (
            f"aws-cost-{datetime.datetime.now().isoformat()[0:19].replace(':','-')}.xlsx"
        )
        dfs = {
            "Parameters": pd.DataFrame(
                [
                    {"Parameter": "Cost Metric", "Value": self.cost_metric},
                    {"Parameter": "Granularity", "Value": self.granularity},
                    {"Parameter": "Periods", "Value": self.periods},
                    {"Parameter": "Group Type", "Value": self.group_type},
                    {"Parameter": "Group Key", "Value": self.group_key},
                    {"Parameter": "Filters", "Value": self.filters_str()},
                ]
            ),
            # "Costs": self.df_costs_totals,
            "Usage": self.df_usage_details,
            "Summary": self.df_usage_summary,
        }
        o7p.dfs_to_excel(dfs, filename)
        print(f"File {filename} created")

    # *************************************************
    #
    # *************************************************
    def get_report_data(self):
        self.granularity = "MONTHLY"
        self.periods = 12

        df_totals = self.get_cost_from_aws(
            group_by=[
                {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"},
                {"Type": "DIMENSION", "Key": "RECORD_TYPE"},
            ],
        )

        df_usage = self.get_cost_from_aws(
            group_by=[
                {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"},
                {"Type": "DIMENSION", "Key": "SERVICE"},
            ],
            filters={
                "Dimensions": {
                    "Key": "RECORD_TYPE",
                    "Values": ["Usage"],
                    "MatchOptions": ["EQUALS"],
                }
            },
        )

        dfs = {
            "accounts": self.load_accounts(),
            "totals": df_totals,
            "usage": df_usage,
        }

        # filename = f"aws-cost-report-{datetime.datetime.now().isoformat()[0:19].replace(':','-')}.xlsx"
        # o7p.dfs_to_excel(dfs, filename)
        # print(f"File {filename} created")

        return dfs

    # *************************************************
    #
    # *************************************************
    def write_pdf_report(self, folder: str = None) -> str:
        """Save HTML report for standards"""

        if _has_o7pdf is False:
            print("fpdf2 is not installed  (pip install o7cli[pdf])")
            return None

        folder = folder if folder is not None else "."

        filename = f"aws-cost-report-{datetime.datetime.now().isoformat()[0:19].replace(':','-')}.pdf"
        filename = os.path.join(folder, filename)

        dfs = self.get_report_data()

        report = o7rac.ReportAwsCost(filename=filename)
        report.generate(dfs=dfs).save()

        return filename

    # *************************************************
    #
    # *************************************************
    def display_usage(self):
        print(f"Granularity: {self.granularity} - Periods: {self.periods}")
        print(f"Grouping by {self.group_type} : {self.group_key}")
        print(f"Filters      : {self.filters_str()}")
        print("-" * o7t.get_width())

        self.update_usage()

        if self.show_day_summary:
            print(self.df_usage_summary)
        else:
            print(self.df_usage_details)

    # *************************************************
    #
    # *************************************************
    def add_item_filter(self, index: int):
        if not self.show_day_summary:
            print("Filter only available when showing the summary view")
            return

        if not 0 <= index < len(self.df_usage_summary.index):
            return self

        value = self.df_usage_summary.iloc[index][self.group_key]

        print(f"Filtering on {self.group_key} = {value}")

        if self.group_type == "TAG":
            new_filter = {
                "Tags": {
                    "Key": self.group_key,
                    "Values": [value],
                    "MatchOptions": ["EQUALS"],
                }
            }
        else:
            new_filter = {
                "Dimensions": {
                    "Key": self.group_key,
                    "Values": [value],
                    "MatchOptions": ["EQUALS"],
                }
            }

        self.filters.append(new_filter)

    # *************************************************
    #
    # *************************************************
    def menu_tag(self) -> str:
        """Return a selected tag"""

        tags = self.load_tags()

        while True:
            self.console_title(left="Avalable Costing Tags")
            print("-----------------------------")
            print("Avalable Costing Tags")
            print("-----------------------------")
            for i, tag in enumerate(tags):
                print(f"{i + 1}. {tag}")

            key = o7i.input_multi("Option -> Back(b) Select(int): ")

            if isinstance(key, str) and key.lower() == "b":
                break

            if isinstance(key, int) and 0 < key <= len(tags):
                self.group_type = "TAG"
                self.group_key = tags[key - 1]
                break

    # *************************************************
    #
    # *************************************************
    def menu_dimension(self) -> str:
        """Return a selected dimension"""

        dimensions = [
            "AZ",
            "INSTANCE_TYPE",
            "LINKED_ACCOUNT",
            "OPERATION",
            "PURCHASE_TYPE",
            "SERVICE",
            "USAGE_TYPE",
            "PLATFORM",
            "TENANCY",
            "RECORD_TYPE",
            "LEGAL_ENTITY_NAME",
            "INVOICING_ENTITY",
            "DEPLOYMENT_OPTION",
            "DATABASE_ENGINE",
            "CACHE_ENGINE",
            "INSTANCE_TYPE_FAMILY",
            "REGION",
            "BILLING_ENTITY",
            "RESERVATION_ID",
            "SAVINGS_PLANS_TYPE",
            "SAVINGS_PLAN_ARN",
            "OPERATING_SYSTEM",
        ]

        while True:
            self.console_title(left="Avalable Costing Dimensions")
            print("Avalable Costing Dimensions")
            for i, dimension in enumerate(dimensions):
                print(f"{i + 1}. {dimension}")

            key = o7i.input_multi("Option -> Back(b) Select(int): ")

            if isinstance(key, str) and key.lower() == "b":
                return None

            if isinstance(key, int) and 0 < key <= len(dimensions):
                self.group_type = "DIMENSION"
                self.group_key = dimensions[key - 1]
                break

    # *************************************************
    #
    # *************************************************
    def menu_cost(self):
        self.group_type = "DIMENSION"
        self.group_key = "LINKED_ACCOUNT"
        self.filters = []
        self.show_day_summary = True

        # Format for Pandas
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", o7t.get_width())
        pd.set_option("display.max_colwidth", None)
        pd.set_option(
            "display.float_format", "{:,.4f}".format
        )  # https://docs.python.org/2/library/string.html#formatstrings

        obj = o7m.Menu(
            exit_option="b",
            title="Cost by Days - Summary",
            title_extra=self.session_info(),
            compact=False,
        )

        obj.add_option(
            o7m.Option(
                key="v",
                name="Toggle View (Summary or all Periods)",
                short="View",
                wait=False,
                callback=lambda: self.__setattr__(
                    "show_day_summary", not self.show_day_summary
                ),
            )
        )

        obj.add_option(
            o7m.Option(
                key="a",
                name="Group by Account",
                short="account",
                wait=False,
                callback=lambda: self.set_group_dimension("LINKED_ACCOUNT"),
            )
        )
        obj.add_option(
            o7m.Option(
                key="s",
                name="Group by Service",
                short="usage",
                wait=False,
                callback=lambda: self.set_group_dimension("SERVICE"),
            )
        )
        obj.add_option(
            o7m.Option(
                key="u",
                name="Group by Usage Type",
                short="usage",
                wait=False,
                callback=lambda: self.set_group_dimension("USAGE_TYPE"),
            )
        )
        obj.add_option(
            o7m.Option(
                key="d",
                name="Group by Other Dimension",
                short="Dimension",
                wait=False,
                callback=self.menu_dimension,
            )
        )
        obj.add_option(
            o7m.Option(
                key="t",
                name="Group by Cost Allocation Tag",
                short="Tag",
                wait=False,
                callback=self.menu_tag,
            )
        )
        obj.add_option(
            o7m.Option(
                key="x",
                name="Write Data to Excel",
                short="Excel",
                wait=True,
                callback=self.to_excel,
            )
        )
        obj.add_option(
            o7m.Option(
                key="report",
                name="Cost Report",
                short="Report",
                wait=True,
                callback=self.write_pdf_report,
            )
        )

        obj.add_option(
            o7m.Option(
                key="int",
                name="Filter on a Item",
                short="Filter",
                callback=self.add_item_filter,
            )
        )
        obj.display_callback = self.display_usage
        obj.loop()

        return self


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    Costing(**kwargs).menu_cost()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    the_obj = Costing()

    the_obj.menu_cost()

    # the_obj.granularity = "MONTHLY"
    # the_obj.periods = 12
    # the_obj.group_key = "RECORD_TYPE"

    # the_obj.periods = 30
    # print(the_obj.get_cost_from_aws( [
    #     {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT" },
    #     {"Type": "DIMENSION", "Key": "SERVICE" }
    # ]))

    # print(the_obj.get_cost_from_aws( ))

    # the_obj.load_cost_totals()
    # print(the_obj.df_costs_totals)

    # the_obj.load_usage_details()
    # print(the_obj.df_usage_details)

    # print(the_obj.summarize_usage(the_obj.df_usage_details))

    # CostExplorer().conformity_report()
    # print(f'List of tags: {the_ce.list_tags()}')

    # the_accounts = the_ce.load_accounts()

    # print(the_accounts[['Id', 'Name', 'Status', 'Email']])
    # costs = the_ce.load_costs(tag_key='Project'
