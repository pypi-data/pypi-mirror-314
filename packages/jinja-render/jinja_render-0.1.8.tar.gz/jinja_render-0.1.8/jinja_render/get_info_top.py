import os


def add_repo_info(summary_content):
    repo_and_hash = get_repo_and_hash("develop")
    summary_content.update(repo_and_hash)
    return summary_content


def get_repo_and_hash(branch="HEAD"):
    hash = get_hash_from_branch(branch)
    name = get_repo_name()
    return {"repo": name, "hash": hash}


def get_hash_from_branch(branch):
    command = "git config --global --add safe.directory /workdir"
    run_command(command)
    stream = os.popen(f"git rev-parse {branch}")
    output = stream.read()
    return output.split("\n")[0]


def get_repo_name():
    command = "git config --global --add safe.directory /workdir"
    run_command(command)
    stream = os.popen("basename $(git remote get-url origin) | cut -d '.' -f 1")
    return stream.read().strip()


def run_command(command):
    exit_code = os.system(command)
    assert exit_code == 0
