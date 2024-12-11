import o7cli.ssoadmin


def test_init(mocker):
    obj = o7cli.ssoadmin.SsoAdmin()
    assert obj.accounts == []
