import o7cli.costexplorer


def test_init():
    obj = o7cli.costexplorer.CostExplorer()
    assert obj.filters == []
    assert obj.df_accounts is None
