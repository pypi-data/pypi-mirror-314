import o7cli.rds


def test_init(mocker):
    obj = o7cli.rds.Rds()
    assert obj.db_instances == []
    assert obj.db_instance == {}
