import o7cli.ssm_ps


def test_init(mocker):
    obj = o7cli.ssm_ps.SsmPs()
    assert obj.parameters == []
    assert obj.parameter is None
