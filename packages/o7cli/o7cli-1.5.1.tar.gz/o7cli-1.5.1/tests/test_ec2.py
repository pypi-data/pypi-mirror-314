from copy import deepcopy

from botocore.stub import Stubber, ANY
import botocore

import o7cli.ec2


describe_instances_resp = {
    "Reservations": [
        {
            "Instances": [
                {
                    "InstanceId": "i-1234567890abcdef0",
                    "InstanceType": "t2.micro",
                    "State": {"Name": "running"},
                },
                {
                    "InstanceId": "i-0abcdef1234567890",
                    "InstanceType": "t2.micro",
                    "State": {"Name": "running"},
                    "Tags": [{"Key": "Name", "Value": "MyInstance"}],
                },
            ]
        },
    ]
}
describe_status_resp = {
    "InstanceStatuses": [
        {
            "InstanceId": "i-1234567890abcdef0",
            "InstanceState": {"Name": "running"},
            "InstanceStatus": {"Status": "ok"},
            "SystemStatus": {"Status": "ok"},
        }
    ]
}


def test_init():
    obj = o7cli.ec2.Ec2()
    assert obj.instances == []
    assert obj.instance == {}


def test_load_instances():
    obj = o7cli.ec2.Ec2()

    with botocore.stub.Stubber(obj.ec2) as stubber:
        stubber.add_response("describe_instances", deepcopy(describe_instances_resp))
        stubber.activate()

        obj.load_instances()
        assert len(obj.instances) == 2
        assert obj.instances[0]["InstanceId"] == "i-1234567890abcdef0"
        assert obj.instances[1]["Name"] == "MyInstance"

        stubber.assert_no_pending_responses()
        stubber.deactivate()


def test_menu(monkeypatch):
    inputs = iter(["1", "b", "b", "b"])

    obj = o7cli.ec2.Ec2()
    with botocore.stub.Stubber(obj.ec2) as stubber:
        print(describe_instances_resp)
        print("----------------")
        stubber.add_response("describe_instances", deepcopy(describe_instances_resp))
        stubber.add_response("describe_instances", deepcopy(describe_instances_resp))
        stubber.add_response("describe_instance_status", deepcopy(describe_status_resp))
        stubber.add_response("describe_instances", deepcopy(describe_instances_resp))

        stubber.activate()
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        obj.menu_instances()

    # obj = o7cli.ec2.Ec2()
    # obj.menu_instance(0)
