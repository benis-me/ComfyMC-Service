import os
import git
import sys
import platform
import subprocess

from .paths import git_script_path

def git_repo_has_updates(path, do_fetch=False):
    # Check if the path is a git repository
    if not os.path.exists(os.path.join(path, '.git')):
        raise ValueError('Not a git repository')

    if platform.system() == "Windows":
        return __win_check_git_update(path, do_fetch)
    else:
        # Fetch the latest commits from the remote repository
        repo = git.Repo(path)

        current_branch = repo.active_branch
        branch_name = current_branch.name

        remote_name = 'origin'
        remote = repo.remote(name=remote_name)

        if do_fetch:
            remote.fetch()

        # Get the current commit hash and the commit hash of the remote branch
        commit_hash = repo.head.commit.hexsha
        remote_commit_hash = repo.refs[f'{remote_name}/{branch_name}'].object.hexsha

        # Compare the commit hashes to determine if the local repository is behind the remote repository
        if commit_hash != remote_commit_hash:
            # Get the commit dates
            commit_date = repo.head.commit.committed_datetime
            remote_commit_date = repo.refs[f'{remote_name}/{branch_name}'].object.committed_datetime

            # Compare the commit dates to determine if the local repository is behind the remote repository
            if commit_date < remote_commit_date:
                return True

    return False


# use subprocess to avoid file system lock by git (Windows)
def __win_check_git_update(path, do_fetch=False):
    if do_fetch:
        command = [sys.executable, git_script_path, "--fetch", path]
    else:
        command = [sys.executable, git_script_path, "--check", path]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode('utf-8').strip()

    if "CUSTOM NODE CHECK: True" in output:
        process.wait()
        return True
    else:
        process.wait()
        return False
