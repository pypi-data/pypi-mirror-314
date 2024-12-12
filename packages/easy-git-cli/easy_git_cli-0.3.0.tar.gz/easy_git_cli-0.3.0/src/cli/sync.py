import questionary
from git_utils import get_git_repo, get_origin, pull_changes


def sync() -> None:
    """
    Pull changes from the remote and rebase them.
    You can call this command by running `easy-git sync` or `easy-git s` for short.
    This will first list the branches and prompt you to select the branch you want to sync.
    After selecting the branch, it will pull the changes from the remote and rebase them.
    """
    repo = get_git_repo()

    origin = get_origin(repo)

    branch = questionary.select(
        "Select the branch to sync with the remote",
        choices=[branch.name for branch in repo.branches],
        use_jk_keys=True,
    ).ask()

    pull_changes(origin, branch)
