import o7cli.s3


def test_init(mocker):
    obj = o7cli.s3.S3()
    assert obj.buckets == []
    assert obj.bucket == ""
