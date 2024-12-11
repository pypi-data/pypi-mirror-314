import o7cli.costing


def test_init():
    obj = o7cli.costing.Costing()
    assert obj.filters == []
    assert obj.df_accounts is None
