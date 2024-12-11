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
"""Module to manage S3 function"""

# --------------------------------
#
# --------------------------------
import ast
import json
import logging
import os
import pprint

import o7util.file_explorer as o7fe
import o7util.format as o7f
import o7util.input as o7i
import o7util.menu as o7m
import o7util.terminal as o7t
from o7util.table import ColumnParam, Table, TableParam

from o7cli.base import Base

logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
class S3(Base):
    """Class to manage S3 operations"""

    #  https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

    # *************************************************
    #
    # *************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.client = self.session.client("s3")

        self.buckets: list = []

        self.bucket: str = ""
        self.with_buckets_details: bool = False
        self.prefix: str = ""
        self.key: str = ""

        self.objects: list = []
        self.s3_object: dict = {}

    # *************************************************
    #
    # *************************************************
    def verify_ssl_requests_only(self, bucket: str, statements: list) -> bool:
        """Verify if the bucket policy enforces SSL requests only"""
        logger.info("verify_ssl_requests_only")

        bucket_arn = f"arn:aws:s3:::{bucket}"
        bucket_arn_with_wildcard = f"{bucket_arn}/*"

        for statement in statements:
            # pprint.pprint(statement)

            if statement.get("Effect", "") != "Deny":
                continue

            resources = statement.get("Resource", [])
            if not isinstance(resources, list):
                resources = [resources]

            if (bucket_arn not in resources) or (
                bucket_arn_with_wildcard not in resources
            ):
                continue

            condition = statement.get("Condition", {})
            if (
                "Bool" in condition
                and condition["Bool"].get("aws:SecureTransport") == "false"
            ):
                return True

        return False

    # *************************************************
    #
    # *************************************************
    def set_ssl_requests_only(self):
        """Set the bucket policy to enforce SSL requests only"""

        bucket = self.bucket
        policies = self.get_bucket_policies(bucket=bucket)
        policies.append(
            {
                "Effect": "Deny",
                "Principal": "*",
                "Action": "*",
                "Resource": [
                    f"arn:aws:s3:::{bucket}",
                    f"arn:aws:s3:::{bucket}/*",
                ],
                "Condition": {"Bool": {"aws:SecureTransport": "false"}},
            }
        )

        policy = {"Version": "2012-10-17", "Statement": policies}

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_policy
        response = self.client.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))

        return response

    # *************************************************
    #
    # *************************************************
    def set_basic_lifecycle_fule(self):
        """Configure a basic lifecycle rule"""

        bucket = self.bucket
        rules = self.get_lifecycle_rules(bucket=bucket)
        rules.append(
            {
                "ID": "RemovedNonCurrentAfter1Year",
                "Status": "Enabled",
                "Filter": {"Prefix": ""},
                "NoncurrentVersionExpiration": {"NoncurrentDays": 365},
                "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 14},
            }
        )
        config = {"Rules": rules}

        print(f"Config: {config}")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_bucket_lifecycle_configuration.html
        response = self.client.put_bucket_lifecycle_configuration(
            Bucket=bucket, LifecycleConfiguration=config
        )

        return response

    # *************************************************
    #
    # *************************************************
    def get_bucket_region(self, bucket: str):
        """Get the region of a bucket"""

        try:
            response = self.client.get_bucket_location(Bucket=bucket)
        except self.client.exceptions.NoSuchBucket:
            return "Deleted"

        region = response.get("LocationConstraint", "NA")

        if region is None:
            region = "us-east-1"

        return region

    # *************************************************
    #
    # *************************************************
    def get_bucket_policies(self, bucket: str):
        """Load additional information for a bucket"""

        try:
            response = self.client.get_bucket_policy(Bucket=bucket)
        except self.client.exceptions.from_code("NoSuchBucketPolicy"):
            return []

        policy = response.get("Policy", "")
        return ast.literal_eval(policy).get("Statement", [])

    # *************************************************
    #
    # *************************************************
    def get_lifecycle_rules(self, bucket: str):
        """Load LifeCycle rules for a bucket"""

        try:
            response = self.client.get_bucket_lifecycle_configuration(Bucket=bucket)
        except self.client.exceptions.from_code("NoSuchBucketPolicy"):
            return []

        return response.get("Rules", [])

    # *************************************************
    #
    # *************************************************
    def get_bucket_versioning(self, bucket: str):
        """Load additional information for a bucket"""

        try:
            response = self.client.get_bucket_versioning(Bucket=bucket)
        except self.client.exceptions.from_code("NoSuchBucketPolicy"):
            return []

        return {
            "Status": response.get("Status", "Disabled"),
            "MFADelete": response.get("MFADelete", "Disabled"),
        }

    # *************************************************
    #
    # *************************************************
    def get_bucket_object_lock(self, bucket: str):
        """Load additional information for a bucket"""

        try:
            response = self.client.get_object_lock_configuration(Bucket=bucket)
        except self.client.exceptions.from_code("NoSuchBucketPolicy"):
            return "Disabled"

        return response.get("ObjectLockConfiguration", {}).get(
            "ObjectLockEnabled", "Disabled"
        )

    # *************************************************
    #
    # *************************************************
    def get_bucket_details(self, bucket) -> dict:
        """get details for a bucket"""

        ret = {}
        ret["Region"] = self.get_bucket_region(bucket=bucket)
        ret["Policies"] = self.get_bucket_policies(bucket=bucket)
        ret["IsSSL"] = self.verify_ssl_requests_only(
            bucket=bucket, statements=ret["Policies"]
        )
        ret["Versioning"] = self.get_bucket_versioning(bucket=bucket)
        ret["VersioningStatus"] = ret["Versioning"].get("Status", "Disabled")
        ret["LifecycleRules"] = self.get_lifecycle_rules(bucket=bucket)
        ret["LifecycleRulesCount"] = len(ret["LifecycleRules"])
        ret["ObjectLock"] = self.get_bucket_object_lock(bucket=bucket)

        return ret

    # *************************************************
    #
    # *************************************************
    def load_buckets(self):
        """Load all Buckets in account"""

        logger.info("load_buckets")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets
        resp = self.client.list_buckets()
        # pprint.pprint(resp)

        self.buckets = resp.get("Buckets", [])
        logger.info(f"LoadBuckets: Number of Bucket found: {len(self.buckets)}")

        if self.with_buckets_details:
            for bucket in self.buckets:
                bucket.update(self.get_bucket_details(bucket=bucket["Name"]))

        return self

    # *************************************************
    #
    # *************************************************
    def load_buckets_extra(self):
        """Load additional information for all buckets"""
        self.with_buckets_details = True
        return self

    # *************************************************
    #
    # *************************************************
    def load_bucket(self):
        """Load information about a bucket"""

        logger.info("load_bucket")
        bucket = self.bucket
        self.bucket_info = self.get_bucket_details(bucket=bucket)
        return self

    # *************************************************
    #
    # *************************************************
    def load_folder(self):
        """Load all content of a bucket and prefix"""

        logger.info("load_folder")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2
        paginator = self.client.get_paginator("list_objects_v2")
        contents = []
        common_prefixes = []
        param = {"Bucket": self.bucket, "Prefix": self.prefix, "Delimiter": "/"}

        for page in paginator.paginate(**param):
            contents.extend(page.get("Contents", []))
            common_prefixes.extend(page.get("CommonPrefixes", []))

        # To all commonPrefixes, add the attribute Key
        for common_prefixe in common_prefixes:
            common_prefixe["Key"] = common_prefixe["Prefix"]

        self.objects = common_prefixes + contents

        # To all objects, set a name without the prefix
        for obj in self.objects:
            obj["_Name"] = obj["Key"].replace(self.prefix, "", 1)

        return self

    # *************************************************
    #
    # *************************************************
    def load_object(self):
        """Load all content of a bucket and prefix"""

        logger.info("load_folder")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/get_object_attributes.html
        self.s3_object = self.client.get_object_attributes(
            Bucket=self.bucket,
            Key=self.key,
            ObjectAttributes=[
                "ETag",
                "Checksum",
                "ObjectParts",
                "StorageClass",
                "ObjectSize",
            ],
        )

        return self

    # *************************************************
    #
    # *************************************************
    def get_presigned_url(self):
        """Get a presigned URL for the object"""

        expiration = o7i.input_int("Expiration (seconds) :")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/generate_presigned_url.html#S3.Client.generate_presigned_url
        url = self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": self.key},
            ExpiresIn=expiration,
        )

        print(f"Presigned URL: {url}")

    # *************************************************
    #
    # *************************************************
    def upload_file(self):
        """Upload a file to a bucket"""

        logger.info(f"UploadFile to {self.bucket}/{self.prefix}")

        file_path = o7fe.FileExplorer(cwd=".").select_file()
        file_key = os.path.basename(file_path)

        if not o7i.is_it_ok(f"Upload {file_key} to {self.bucket}/{self.prefix} ?"):
            return self

        if self.prefix:
            file_key = f"{self.prefix}/{file_key}"

        response = self.client.upload_file(file_path, self.bucket, file_key)
        pprint.pprint(response)

        return self

    # *************************************************
    #
    # *************************************************
    def upload_file_obj(self, bucket: str, key: str, file_path: str):
        """Upload a file to a bucket, used by other module"""

        logger.info(f"UploadFile {bucket=} {key=} {file_path=}")

        ret = None

        with open(file_path, "rb") as fileobj:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_fileobj
            resp = self.client.upload_fileobj(
                fileobj,
                Bucket=bucket,
                Key=key,
            )
            logger.info(f"UploadFile: Done {resp=}")
            ret = f"https://s3-external-1.amazonaws.com/{bucket}/{key}"

        return ret

    # *************************************************
    #
    # *************************************************
    def display_object(self):
        """Display the active object"""

        self.load_object()

        print()
        print(f"Bucket: {self.bucket}")
        print(f"Prefix: {self.prefix}")
        print(f"Name  : {self.key}")
        print()
        print(f'Last Modified: {self.s3_object.get("LastModified", "-")}')
        print(f'Storage Class: {self.s3_object.get("StorageClass", "-")}')
        print(f'ETag: {self.s3_object.get("ETag", "-")}')
        print(f'Size: {o7f.to_bytes(self.s3_object.get("ObjectSize", "-"))}')

        print()

    # *************************************************
    #
    # *************************************************
    def display_buckets(self):
        """Display the list buckets"""

        self.load_buckets()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="Name"),
                ColumnParam(title="Created", type="date", data_col="CreationDate"),
                ColumnParam(title="Region", type="str", data_col="Region"),
                ColumnParam(
                    title="SSL",
                    type="str",
                    data_col="IsSSL",
                    normal=True,
                    alarm=False,
                ),
                ColumnParam(
                    title="Versioning",
                    type="str",
                    data_col="VersioningStatus",
                    normal="Enabled",
                ),
                ColumnParam(
                    title="LifeCycles",
                    type="str",
                    data_col="LifecycleRulesCount",
                    alarm_lo=0,
                ),
                ColumnParam(
                    title="Obj.Lock",
                    type="str",
                    data_col="ObjectLock",
                    normal="Enabled",
                ),
            ]
        )

        print()
        Table(params, self.buckets).print()

        return self

    # *************************************************
    #
    # *************************************************
    def display_bucket(self):
        """Display the list buckets"""

        self.load_bucket()

        print("")
        print(f"Bucket: {self.bucket}")
        print("")
        print("---- Policies ->")
        pprint.pprint(self.bucket_info["Policies"])
        print("-----------------")
        print("")

        print("---- Lifecyle Rules ->")
        pprint.pprint(self.bucket_info["LifecycleRules"])
        print("-----------------")
        print("")

        if self.bucket_info["IsSSL"]:
            print(o7t.format_normal("SSL Request: Enforced"))
        else:
            print(o7t.format_alarm("SSL Request: NOT Enforced"))
        print(f"Versioning: {self.bucket_info['Versioning']['Status']}")
        print(f"MFADelete: {self.bucket_info['Versioning']['MFADelete']}")
        print("")

    # *************************************************
    #
    # *************************************************
    def display_folder(self):
        """Display the list buckets"""

        print("")
        print(f"Bucket: {self.bucket}")
        print(f"Prefix: {self.prefix}")

        self.load_folder()

        params = TableParam(
            columns=[
                ColumnParam(title="id", type="i", min_width=4),
                ColumnParam(title="Name", type="str", data_col="_Name"),
                ColumnParam(title="Size", type="bytes", data_col="Size"),
                ColumnParam(
                    title="Last Modified", type="datetime", data_col="LastModified"
                ),
                ColumnParam(title="Storage", type="str", data_col="StorageClass"),
            ]
        )
        print()
        Table(params, self.objects).print()

    # *************************************************
    #
    # *************************************************
    def menu_object(self, index: int):
        """S3 Folder menu"""

        if not 0 < index <= len(self.objects):
            return self

        s3_object = self.objects[index - 1]

        if "ETag" not in s3_object:
            self.prefix = s3_object["Key"]
            return self

        self.key = s3_object["Key"]

        obj = o7m.Menu(
            exit_option="b",
            title=f"S3 Folder - {self.bucket}",
            title_extra=self.session_info(),
            compact=False,
        )
        obj.add_option(
            o7m.Option(
                key="r", name="Raw", callback=lambda: pprint.pprint(self.s3_object)
            )
        )
        obj.add_option(
            o7m.Option(key="p", name="Presigned ", callback=self.get_presigned_url)
        )

        obj.display_callback = self.display_object
        obj.loop()

        return self

    # *************************************************
    #
    # *************************************************
    def menu_folder(self):
        """S3 Folder menu"""

        self.prefix = ""
        self.key = ""

        obj = o7m.Menu(
            exit_option="b",
            title=f"S3 Folder - {self.bucket}",
            title_extra=self.session_info(),
            compact=True,
        )
        obj.add_option(
            o7m.Option(key="r", name="Raw", callback=lambda: pprint.pprint(self.objects))
        )
        obj.add_option(o7m.Option(key="u", name="Upload", callback=self.upload_file))
        obj.add_option(o7m.Option(key="int", name="Details", callback=self.menu_object))

        obj.display_callback = self.display_folder
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_bucket(self, index: int):
        """S3 Folder menu"""

        if not 0 < index <= len(self.buckets):
            return self

        self.bucket = self.buckets[index - 1]["Name"]
        self.prefix = ""
        self.key = ""

        obj = o7m.Menu(
            exit_option="b",
            title=f"S3 Bucket - {self.bucket}",
            title_extra=self.session_info(),
            compact=False,
        )
        obj.add_option(
            o7m.Option(
                key="r", name="Raw", callback=lambda: pprint.pprint(self.bucket_info)
            )
        )
        obj.add_option(o7m.Option(key="f", name="See Files", callback=self.menu_folder))
        obj.add_option(
            o7m.Option(
                key="set-ssl",
                name="Set SSL Request Policy",
                callback=self.set_ssl_requests_only,
            )
        )
        obj.add_option(
            o7m.Option(
                key="add-lcr",
                name="Add Basic Lifecycle Rule (delete non current after 1 year)",
                callback=self.set_basic_lifecycle_fule,
            )
        )
        obj.display_callback = self.display_bucket
        obj.loop()

    # *************************************************
    #
    # *************************************************
    def menu_buckets(self):
        """S3 main menu"""

        obj = o7m.Menu(
            exit_option="b",
            title="S3 Bucket",
            title_extra=self.session_info(),
            compact=True,
        )

        obj.add_option(
            o7m.Option(
                key="r",
                name="Display Raw Data",
                short="Raw",
                callback=lambda: pprint.pprint(self.buckets),
            )
        )
        obj.add_option(
            o7m.Option(
                key="l",
                name="Load Details",
                short="Load Details",
                wait=False,
                callback=self.load_buckets_extra,
            )
        )
        obj.add_option(
            o7m.Option(
                key="int",
                name="Details for a bucket",
                short="Details",
                callback=self.menu_bucket,
            )
        )

        obj.display_callback = self.display_buckets
        obj.loop()

        return self


# *************************************************
#
# *************************************************
def menu(**kwargs):
    """Run Main Menu"""
    S3(**kwargs).menu_buckets()


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    # the_s3 = S3().menu_buckets()

    the_s3 = S3()
    # the_s3.bucket = "my-bucket"
    # the_s3.prefix = ""
    # the_s3.key = "my-file.zip"
    # the_s3.display_folder()

    # the_s3.display_object()

    # theS3.MenuBuckets()
