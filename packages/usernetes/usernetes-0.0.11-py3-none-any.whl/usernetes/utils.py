import json
import os
import re
import stat
import subprocess
import tempfile
from contextlib import contextmanager

import yaml


def read_json(filename):
    """
    Read json from file
    """
    return json.loads(read_file(filename))


def read_file(filename):
    """
    Read in a file content
    """
    with open(filename, "r") as fd:
        content = fd.read()
    return content


def recursive_find(base, pattern="[.]py"):
    """recursive find will yield python files in all directory levels
    below a base path.

    Arguments:
      - base (str) : the base directory to search
      - pattern: a pattern to match, defaults to *.py
    """
    for root, _, filenames in os.walk(base):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if not re.search(pattern, filepath):
                continue
            yield filepath


def get_tmpfile(tmpdir=None, prefix="", suffix=None):
    """
    Get a temporary file with an optional prefix.
    """
    # First priority for the base goes to the user requested.
    tmpdir = get_tmpdir(tmpdir)

    # If tmpdir is set, add to prefix
    if tmpdir:
        prefix = os.path.join(tmpdir, os.path.basename(prefix))

    fd, tmp_file = tempfile.mkstemp(prefix=prefix, suffix=suffix)
    os.close(fd)

    return tmp_file


def get_tmpdir(tmpdir=None, prefix="", create=True):
    """
    Get a temporary directory for an operation.
    """
    tmpdir = tmpdir or tempfile.gettempdir()
    prefix = prefix or "usernetes"
    prefix = "%s.%s" % (prefix, next(tempfile._get_candidate_names()))
    tmpdir = os.path.join(tmpdir, prefix)

    if not os.path.exists(tmpdir) and create is True:
        os.mkdir(tmpdir)

    return tmpdir


def read_yaml(filename):
    """
    Read yaml from file
    """
    with open(filename, "r") as fd:
        content = yaml.safe_load(fd)
    return content


def write_file(content, filename, executable=False):
    """
    Write content to file
    """
    with open(filename, "w") as fd:
        fd.write(content)
    # Make the file executable
    if executable:
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def write_yaml(obj, filename):
    """
    Read yaml to file
    """
    with open(filename, "w") as fd:
        yaml.dump(obj, fd)


@contextmanager
def workdir(dirname):
    """
    Provide context for a working directory, e.g.,

    with workdir(name):
       # do stuff
    """
    here = os.getcwd()
    os.chdir(dirname)
    try:
        yield
    finally:
        os.chdir(here)


def run_command(cmd, stream=False, check_output=False, return_code=0, envars=None):
    """
    use subprocess to send a command to the terminal.

    If check_output is True, check against an expected return code.
    """
    envars = envars or {}
    env = os.environ.copy()
    env.update(envars)
    stdout = subprocess.PIPE if not stream else None
    output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=stdout, env=env)
    t = output.communicate()[0], output.returncode
    output = {"message": t[0], "return_code": t[1]}

    if isinstance(output["message"], bytes):
        output["message"] = output["message"].decode("utf-8")

    # Check the output and raise an error if not success
    if check_output and t[1] != return_code:
        if output["message"]:
            raise ValueError(output["message"].strip())
        else:
            raise ValueError(f"Failed execution, return code {t[1]}")
    return output
