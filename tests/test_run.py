import os

def test_headers(script_runner):
    ret = script_runner.run('spellrst', 'headers.rst', cwd='tests/testdata')
    assert ret.returncode == os.EX_OK

def test_nofiles(script_runner):
    ret = script_runner.run('spellrst', cwd='tests/testdata')
    assert ret.returncode == os.EX_NOINPUT
