from botocore.stub import Stubber

import o7cli.organizations


def test_init(mocker):
    mocker.patch("o7cli.organizations.Organizations.load_description", return_value=None)
    obj = o7cli.organizations.Organizations()
    assert obj.enabled_services == []
