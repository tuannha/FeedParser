import os
import re
import sys
import subprocess
from fabric.operations import local

from django.utils.encoding import force_text


MODIFIED_FILE_RE = re.compile('^(?:M|A)(\s+)(?P<name>.*)')
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[33m'


def run_process_asynchronous(command):
    return local(command)


def run_process(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    return out, err


def matches_file(file_name, files):
    return any(re.compile(item).match(file_name) for item in files)


def get_list_commit_files():
    files = []
    out, err = run_process("git status --porcelain")
    for line in out.splitlines():
        line = force_text(line)
        match = MODIFIED_FILE_RE.match(line)
        if not match:
            continue
        files.append(match.group('name'))

    return files


def get_stage_files():
    out, _ = run_process("git diff --name-only")
    return [force_text(file) for file in out.splitlines()]


def get_changed_files():
    out, _ = run_process("git status --short")
    lines = out.splitlines()
    files = [item.strip().split()[-1] for item in lines]
    files = [force_text(file) for file in files]
    return files


def ask_user_to_add_all_files_to_commit(files):
    files = [force_text(file) for file in files]
    sys.stdin = open('/dev/tty', 'r')

    print("List changed file but not to commit")
    print("%s%s%s" % (
        RED, '\n'.join(files), RESET))

    var = input("Do you want to add them to commit? [[no]/yes/quit] ")  # NOQA
    if var == "yes":
        run_process("git add .")
        return True
    if var == "quit":
        sys.exit(1)


def check_virtual_env():
    if 'VIRTUAL_ENV' not in os.environ:
        print("You must run source venv/bin/active first !!!")
        sys.exit(1)
