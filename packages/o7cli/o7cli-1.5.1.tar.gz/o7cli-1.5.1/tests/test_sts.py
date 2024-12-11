import o7cli.sts


def test_init(mocker):
    obj = o7cli.sts.Sts()
    assert obj.sts is not None
