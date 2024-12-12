import os
import sys
from typing import Optional

import click
from git import GitCommandError, Remote, Repo

from src.utils.logging import get_logger

logger = get_logger()


def get_git_repo() -> Repo:
    """Return the current Git repository."""
    try:
        logger.info("Getting the current Git repository.")
        logger.debug(f"Current working directory: {os.getcwd()}")
        repo = Repo(os.getcwd())
        return repo
    except Exception as e:
        click.echo("Not a git repository.")
        logger.error(f"Not a git repository: {e}")
        sys.exit(1)


def get_changed_files(repo: Repo) -> list[str]:
    """Return the list of changed files in the repository."""
    logger.info("Getting the list of changed files.")
    changed_files = [item.a_path for item in repo.index.diff(None)]  # Unstaged files
    changed_files += repo.untracked_files  # Untracked files
    logger.debug(changed_files)
    return changed_files


def add_file(repo: Repo, file: str) -> None:
    """Add the given file to the staging area."""
    logger.info(f"Adding {file} to the staging area.")
    repo.git.add(file)


def commit(repo: Repo, message: str, amend: bool) -> None:
    """Commit the staged changes with the given message."""
    logger.info(f"Committing the changes with message: {message}")
    repo.git.commit(m=message) if not amend else repo.git.commit("--amend", "--no-edit")


def push(repo: Repo) -> None:
    """Push the changes to the remote repository."""
    try:
        logger.info("Pushing the changes to the remote repository.")
        repo.git.push()
        click.echo("Pushed to the remote repository.")
    except GitCommandError as e:
        click.echo("Error: Unable to push. Check your remote settings.")
        logger.error(f"Failed to push to the remote repository: {e}")


def get_origin(repo: Repo) -> Remote:
    """Return the origin remote of the repository."""
    logger.info("Getting the origin remote.")
    return repo.remotes.origin


def pull_changes(origin: Remote, branch: Optional[str]) -> None:
    """Pull changes from the remote and rebase them."""
    logger.info(f"Pulling changes from {origin.url}.")
    click.echo(f"Syncing with remote {origin.url}...")
    try:
        origin.pull(rebase=True, refspec=f"{branch}:{branch}")
        click.echo("Sync complete.")
        logger.info("Successfully synced with remote.")
    except Exception as e:
        if "Could not resolve hostname" in str(e):
            logger.warning(
                "Network issue: Could not connect to remote. Check your network connection."
            )
        elif "authentication failed" in str(e):
            logger.warning("Authentication failed. Check your Git credentials.")
        else:
            logger.error(f"Failed to sync with remote: {e}")
