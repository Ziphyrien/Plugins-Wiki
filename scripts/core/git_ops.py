import os
import subprocess
import datetime

def run_git_cmd(args, cwd):
    """
    Runs a git command in the specified directory.
    args: list of strings, e.g. ["add", "."]
    """
    cmd = ["git"] + args
    try:
        subprocess.check_call(cmd, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def has_changes(cwd):
    """
    Checks if there are uncommitted changes in the directory.
    """
    try:
        # Check for modified files
        subprocess.check_call(["git", "diff", "--quiet"], cwd=cwd)
        # Check for staged changes
        subprocess.check_call(["git", "diff", "--cached", "--quiet"], cwd=cwd)
        # Check for untracked files
        untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=cwd)
        if untracked.strip():
            return True
        return False # No changes if all passed
    except subprocess.CalledProcessError:
        return True # specific exit code implies diffs exist

def commit_and_push(cwd, message):
    """
    Adds all changes, commits, and pushes in the specified directory.
    """
    if not has_changes(cwd):
        print(f"No changes to commit in {cwd}")
        return False

    print(f"Committing changes in {cwd}...")
    run_git_cmd(["add", "."], cwd)
    
    # Check if user is configured, if not set local dummy (helpful in strict CIs, though sync_starlight usually handles this)
    # But usually locally we have usage.
    
    if run_git_cmd(["commit", "-m", message], cwd):
        print(f"Pushing to remote...")
        if run_git_cmd(["push", "origin", "content"], cwd):
            print("pushed successfully.")
            return True
        else:
            print("Failed to push.")
            return False
    else:
        print("Commit failed.")
        return False
