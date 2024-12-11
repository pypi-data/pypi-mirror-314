import o7cli.ecs


def test_init():
    obj = o7cli.ecs.Ecs()
    assert obj.clusters == []
    assert obj.cluster == {}
