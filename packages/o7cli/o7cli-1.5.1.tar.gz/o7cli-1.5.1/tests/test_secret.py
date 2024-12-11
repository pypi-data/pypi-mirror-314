import o7cli.secret


def test_init(mocker):
    obj = o7cli.secret.Secret()
    assert obj.secrets == []
    assert obj.secret_name is None
