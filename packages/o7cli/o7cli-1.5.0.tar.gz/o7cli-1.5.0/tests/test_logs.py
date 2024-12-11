import o7cli.logs


def test_init():
    obj = o7cli.logs.Logs()

    assert obj.log_groups == []
    assert obj.log_streams == []
    assert obj.log_group is None
