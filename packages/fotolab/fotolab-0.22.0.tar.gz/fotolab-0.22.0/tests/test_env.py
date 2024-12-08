# pylint: disable=C0114,C0116

from fotolab import __version__


def test_env_output(cli_runner):
    ret = cli_runner("env")
    assert f"fotolab: {__version__}" in ret.stdout
    assert "python: " in ret.stdout
    assert "platform: " in ret.stdout
