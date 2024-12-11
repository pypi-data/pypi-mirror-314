import o7cli.asg


def test_init():
    obj = o7cli.asg.Asg()
    assert obj.autoscaling is not None
