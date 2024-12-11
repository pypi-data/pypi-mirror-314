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
"""Module for O7 Command Line Interface"""

# --------------------------------
#
# --------------------------------
import argparse
import logging
import sys

import botocore
import o7util.pypi
import o7util.terminal as o7t

import o7cli
import o7cli.asg
import o7cli.cloudformation
import o7cli.cloudmap
import o7cli.codebuild
import o7cli.codepipeline
import o7cli.costing
import o7cli.ec2
import o7cli.ecs
import o7cli.iam
import o7cli.lambdafct
import o7cli.logs
import o7cli.organizations
import o7cli.rds
import o7cli.reports
import o7cli.s3
import o7cli.secret
import o7cli.securityhub
import o7cli.ssm_ps
import o7cli.ssoadmin

# import o7lib.aws.cloudformation
# import o7lib.aws.pipeline
# import o7lib.aws.codebuild
# import o7lib.aws.codecommit


logger = logging.getLogger(__name__)


# *************************************************
#
# *************************************************
def credential_help():
    """Print help about credential issues"""
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration
    print("There are different way to configure your AWS credentials")
    print(
        "ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration"
    )
    print("")
    print("- If you have the AWS CLI install, use -> aws configure")
    print("- Else, create your own credential file (see ref link)")
    print("")
    print("Note: o7 supports the usage of multiple profile, option -p")
    print("")


# *************************************************
#
# *************************************************
def version_verification():
    """Verify if runngin latest version and notify accordingly"""

    lastest_version = o7util.pypi.Pypi(project="o7cli").get_latest_version()

    if o7cli.__version__ == "LOCAL_VERSION":
        print(
            o7t.format_warning(
                f"You are using a LOCAL VERSION, latest release is {lastest_version}"
            )
        )

    elif lastest_version is not None:
        if lastest_version != o7cli.__version__:
            part1 = f"You are using version o7cli {o7cli.__version__},"
            part2 = f"however, version {lastest_version} is available."
            print(o7t.format_warning(f"{part1} {part2}"))
            print(
                o7t.format_warning(
                    "Please consider upgrading via the 'pip install --upgrade o7cli' command."
                )
            )


# *************************************************
#
# *************************************************
def command_line(argv):  # pylint: disable=too-many-statements,too-many-locals
    """Main Menu for CLI"""

    version_verification()

    parser = argparse.ArgumentParser(
        prog="o7",
        description="Useful CLI and scripts for O7 Conseils DevOps practice",
        epilog=f"version: {o7cli.__version__}",
    )

    parser.add_argument("-p", "--profile", dest="profile", help="AWS Profile")
    parser.add_argument("-r", "--region", dest="region", help="AWS Region")
    parser.add_argument(
        "-d", "--debug", dest="debug", help="Enable Debug Traces", action="store_true"
    )
    parser.add_argument(
        "-i",
        "--info",
        dest="info",
        help="Enable Information Traces",
        action="store_true",
    )
    parser.add_argument(
        "-v", "--version", dest="version", help="Print version", action="store_true"
    )

    subparsers = parser.add_subparsers(
        title="O7 Module",
        description="Select a target module",
        metavar="MODULE",
        help=None,
        required=False,
    )

    parser_report = subparsers.add_parser("report", help="Conformity report")
    parser_report.set_defaults(func=o7cli.reports.run_conformity)

    parser_cost = subparsers.add_parser("cost", help="Analyse account cost")
    parser_cost.set_defaults(func=o7cli.costing.menu)

    parser_org = subparsers.add_parser("org", help="Organization Accounts")
    parser_org.set_defaults(func=o7cli.organizations.menu)

    parser_sso = subparsers.add_parser("sso", help="SSO Administration")
    parser_sso.set_defaults(func=o7cli.ssoadmin.menu)

    parser_shub = subparsers.add_parser("sh", help="Security Hub")
    parser_shub.set_defaults(func=o7cli.securityhub.menu)

    parser_iam = subparsers.add_parser("iam", help="IAM Information")
    parser_iam.set_defaults(func=o7cli.iam.menu)

    parser_log = subparsers.add_parser("log", help="Cloudwatch Logs")
    parser_log.set_defaults(func=o7cli.logs.menu)

    parser_ps = subparsers.add_parser("ps", help="SSM - Parameter Store")
    parser_ps.set_defaults(func=o7cli.ssm_ps.menu)

    parser_secret = subparsers.add_parser("secret", help="Secrets Manager")
    parser_secret.set_defaults(func=o7cli.secret.menu)

    parser_cm = subparsers.add_parser("cm", help="Cloud Map")
    parser_cm.set_defaults(func=o7cli.cloudmap.menu)

    parser_s3 = subparsers.add_parser("s3", help="S3 (Simple Scalable Storage)")
    parser_s3.set_defaults(func=o7cli.s3.menu)

    parser_rds = subparsers.add_parser("rds", help="Relational DB")
    parser_rds.set_defaults(func=o7cli.rds.menu)

    parser_ec2 = subparsers.add_parser("ec2", help="Elastic Computing")
    parser_ec2.set_defaults(func=o7cli.ec2.menu)

    parser_ecs = subparsers.add_parser("ecs", help="Elastic Container Service")
    parser_ecs.set_defaults(func=o7cli.ecs.menu)

    parser_lf = subparsers.add_parser("lf", help="Lambda Functions")
    parser_lf.set_defaults(func=o7cli.lambdafct.menu)

    parser_asg = subparsers.add_parser("asg", help="Auto Scaling Group")
    parser_asg.set_defaults(func=o7cli.asg.menu)

    parser_cfn = subparsers.add_parser("cf", help="Cloudformation")
    parser_cfn.set_defaults(func=o7cli.cloudformation.menu)

    parser_pl = subparsers.add_parser("pl", help="Code Pipeline")
    parser_pl.set_defaults(func=o7cli.codepipeline.menu)

    parser_cb = subparsers.add_parser("cb", help="Code Build")
    parser_cb.set_defaults(func=o7cli.codebuild.menu)

    args = parser.parse_args(argv)
    param = {"profile": args.profile, "region": args.region}

    if args.debug:
        print("Setting debug mode")
        logging.basicConfig(
            level=logging.DEBUG, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
        )

    if args.info:
        print("Setting info mode")
        logging.basicConfig(
            level=logging.INFO, format="[%(levelname)-5.5s] [%(name)s] %(message)s"
        )

    if args.version:
        print(f"{o7cli.__version__}")
        sys.exit(0)

    if not hasattr(args, "func"):
        parser.print_usage()
        sys.exit(0)

    try:
        args.func(**param)

    except botocore.exceptions.NoRegionError:
        print(o7t.format_alarm("ERROR! No AWS default region found"))
        print("")
        print(
            "use -r option OR set an AWS Default Region ('export AWS_DEFAULT_REGION=ca-central-1') "
        )

    except botocore.exceptions.NoCredentialsError:
        print(o7t.format_alarm("ERROR! No AWS credential found"))
        print("")
        credential_help()

    except botocore.exceptions.ProfileNotFound:
        print(o7t.format_alarm("ERROR! Profile do not exist"))

    except KeyboardInterrupt:
        print(f"{o7t.Colors.ENDC}\nGoodbye...")


# *************************************************
#
# *************************************************
def main():
    """Callable from Script"""
    command_line(sys.argv[1:])


# *************************************************
#
# *************************************************
if __name__ == "__main__":
    command_line(sys.argv[1:])
