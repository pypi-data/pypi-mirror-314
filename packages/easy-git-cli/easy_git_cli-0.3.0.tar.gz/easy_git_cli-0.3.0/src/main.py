#!/usr/bin/env python3
import click
from cli import qc, sc
from utils.helpers import AliasedGroup
from utils.logging import configure_logging, get_logger

logger = get_logger()


@click.group(cls=AliasedGroup)
def cli():
    """easy-git: Simplify your Git workflows."""
    pass


@cli.command()
def quick_commit():
    """
    Interactive add-commit-push cycle.
    You can call this command by running `easy-git quick-commit` or `easy-git qc` for short.
    This will first list all changed files (tracked and untracked), then prompt you to select the files you want to stage.
    After staging the files, you can choose to either make a new commit or amend the last commit.
    Finally, you can choose to push the changes to the remote.
    """
    qc()


@cli.command()
def sync():
    """
    Pull changes from the remote and rebase them.
    You can call this command by running `easy-git sync` or `easy-git s` for short.
    This will first list the branches and prompt you to select the branch you want to sync.
    After selecting the branch, it will pull the changes from the remote and rebase them.
    """
    sc()


if __name__ == "__main__":
    configure_logging()
    logger.info("Starting easy-git...")
    cli()
