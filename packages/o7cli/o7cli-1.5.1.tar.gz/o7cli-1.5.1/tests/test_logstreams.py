import o7cli.logstream


def test_init():
    obj = o7cli.logstream.Logstream(
        log_group_name="log_group_name",
        log_stream_name="log_stream_name",
    )

    assert obj.log_group_name == "log_group_name"
    assert obj.log_stream_name == "log_stream_name"
    assert obj.events == []
