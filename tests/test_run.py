"""Script tests."""
import os
import re

from subprocess import run, PIPE


SCRIPT = 'rstxt.py'


def string_compare(parsed, read):
    """Assert that two strings are the same after stripping characters away."""
    parsed_words = parsed.split()
    read_words = re.sub(r'[^\w\s]', '', read).split()
    assert parsed_words == read_words


def test_headers():
    """Test headers.rst."""
    filepath = 'tests/testdata/headers.rst'
    ret = run(['python', SCRIPT, filepath], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    assert ret.stderr == ''
    string_compare(ret.stdout, open(filepath, 'r').read())
    assert ret.returncode == os.EX_OK


def test_todo():
    """Test todo.rst."""
    filepath = 'tests/testdata/todo.rst'
    ret = run(['python', SCRIPT, filepath], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    assert ret.stderr == ''
    string_compare(ret.stdout, open(filepath, 'r').readlines()[-1])
    assert ret.returncode == os.EX_OK


def test_nofiles():
    """Test no file argument."""
    ret = run(['python', SCRIPT], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    assert ret.stderr == ''
    assert ret.stdout == ''
    assert ret.returncode == os.EX_OK


def test_stdin_headers():
    """Test stdin."""
    filepath = 'tests/testdata/headers.rst'
    ret = run(
        ['python', SCRIPT],
        stdin=open(filepath, 'r'),
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
    )
    assert ret.stderr == ''
    string_compare(ret.stdout, open(filepath, 'r').read())
    assert ret.returncode == os.EX_OK


def test_missing_file():
    """Test missing file."""
    filepath = 'not/here/file.missing'
    assert not os.path.isfile(filepath)
    ret = run(['python', SCRIPT, filepath], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    assert ret.stderr == f'rstxt: {filepath}: no such file\n'
    assert ret.stdout == ''
    assert ret.returncode == os.EX_OK
