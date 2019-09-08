"""Script tests."""
import os


def test_headers(script_runner):
    """Test headers.rst."""
    ret = script_runner.run('spellrst', 'headers.rst', cwd='tests/testdata')
    assert ret.returncode == os.EX_OK


def test_nofiles(script_runner):
    """Test no file argument."""
    ret = script_runner.run('spellrst', cwd='tests/testdata')
    assert ret.returncode == os.EX_USAGE
