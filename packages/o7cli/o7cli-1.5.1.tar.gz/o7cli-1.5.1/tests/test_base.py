import os

import pytest
import boto3

import o7cli.base

# from moto import mock_aws

# @patch('o7util.terminal.console_title')
# @patch('boto3.session.Session')

# @pytest.fixture(scope="function")
# def aws_credentials():
#     """Mocked AWS Credentials for moto."""
#     os.environ["AWS_ACCESS_KEY_ID"] = "testing"
#     os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
#     os.environ["AWS_SECURITY_TOKEN"] = "testing"
#     os.environ["AWS_SESSION_TOKEN"] = "testing"
#     os.environ["AWS_DEFAULT_REGION"] = "ca-west-1"
#     os.environ["AWS_PROFILE"] = "tests"

#     print("Set Credentials")


# @pytest.fixture(scope="function")
# def mocked_aws(aws_credentials):
#     """
#     Mock all AWS interactions
#     Requires you to create your own boto3 clients
#     """
#     with mock_aws():
#         yield


# @mock.patch("boto3.session.Session")
# @pytest.fixture(scope="function")
# def mocked_session(mocker, aws_credentials):

#     mocked_object = mocker.MagicMock()
#     mocked_object.configure_mock(region_name='ca-west-1')
#     mocked_object.profile_name.return_value = 'tests'

#     return mocked_object

#     # mock_client = mock.Mock()
#     # mock_client.get_secret_value.return_value = {'SecretString': 'my-secret'}
#     # mock_session_object.client.return_value = mock_client
#     # mock_session_class.return_value = mock_session_object


def test_init():
    obj = o7cli.base.Base()
    assert obj.session is not None
