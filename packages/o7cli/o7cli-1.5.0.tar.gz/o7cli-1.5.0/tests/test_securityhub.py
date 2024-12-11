import o7cli.securityhub


def test_init(mocker):
    obj = o7cli.securityhub.SecurityHub()
    assert obj.df_standards is None
