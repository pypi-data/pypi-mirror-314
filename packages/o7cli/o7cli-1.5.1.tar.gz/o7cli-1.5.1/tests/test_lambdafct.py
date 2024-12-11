from botocore.stub import Stubber

import o7cli.lambdafct

# p -m unittest tests.test_aws_lambda


def test_load():
    obj = o7cli.lambdafct.Lambda()

    response = {
        "Functions": [
            {"FunctionName": "Function1"},
            {"FunctionName": "Function2"},
        ]
    }
    expected_params = {}

    stubber = Stubber(obj.client)
    stubber.add_response("list_functions", response, expected_params)
    stubber.activate()

    obj.load_functions()

    # print(obj.lambdafcts)
    assert isinstance(obj.lambdafcts, list)
    assert len(obj.lambdafcts) == 2
