# O7 CLI
A useful tool for O7 Conseils AWS DevOps activities.
This is developed as we need it in our projects. It shared to allow others to use it.

## Installation
Run the following to install:
```bash
pip install o7cli
```
## Usage

```bash
# Help
o7

# See all AWS pipeline in us-east-1
o7 -r us-east-1 pl

# See all AWS Cloudwatch logs for profile ab in us-west2
o7 -p ab -r us-west-2 log
```

## Options & Module
```
usage: o7 [-h] [-p PROFILE] [-r REGION] [-d] [-i] [-v] MODULE ...

Useful CLI and scripts for O7 Conseils DevOps practice

options:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        AWS Profile
  -r REGION, --region REGION
                        AWS Region
  -d, --debug           Enable Debug Traces
  -i, --info            Enable Information Traces
  -v, --version         Print version

O7 Module:
  Select a target module

  MODULE
    report              Conformity report
    cost                Analyse account cost
    org                 Organization Accounts
    sso                 SSO Administration
    sh                  Security Hub
    iam                 IAM Information
    log                 Cloudwatch Logs
    ps                  SSM - Parameter Store
    secret              Secrets Manager
    cm                  Cloud Map
    s3                  S3 (Simple Scalable Storage)
    rds                 Relational DB
    ec2                 Elastic Computing
    ecs                 Elastic Container Service
    lf                  Lambda Functions
    asg                 Auto Scaling Group
    cf                  Cloudformation
    pl                  Code Pipeline
    cb                  Code Build
```