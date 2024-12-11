import pytest
import o7cli
import o7cli.menu as menu


def test_version_verification():
    menu.version_verification()


def test_command_line_v(capsys):
    # with mocker.patch("sys.exit") as mock_exit:
    with pytest.raises(SystemExit):
        menu.command_line(["-v"])

    out, err = capsys.readouterr()

    version = out.strip().split("\n")[-1]
    assert version == o7cli.__version__
