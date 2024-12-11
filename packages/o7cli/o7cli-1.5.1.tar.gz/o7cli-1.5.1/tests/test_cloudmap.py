import o7cli.cloudmap


def test_init():
    obj = o7cli.cloudmap.CloudMap()
    assert obj.namespaces == []
