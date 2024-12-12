import os
import sys
import click
import signal

from utils.logging import get_logger

logger = get_logger()


def is_git_repository() -> bool:
    """Check if the current directory is a Git repository."""
    logger.info("Checking if the current directory is a Git repository.")
    return os.path.isdir(".git")


def handle_kill_signal(signal_number, frame):
    """Handle kill signals"""
    if signal_number in [signal.SIGINT, signal.SIGTERM]:
        click.echo("\nReceived interrupt signal. Exiting...")
        sys.exit(0)
    logger.critical(f"Received unknown signal: {signal_number}")
    sys.exit(1)


# Register signal handlers
signal.signal(signal.SIGINT, handle_kill_signal)
signal.signal(signal.SIGTERM, handle_kill_signal)


aliases = {
    "c": "quick-commit",
    "s": "sync",
    "h": "help",
}


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if aliases.get(cmd_name) == x]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        logger.error(f"Too many matches: {', '.join(sorted(matches))}")
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

    def resolve_command(self, ctx, args):
        # always return the full command name
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name if cmd is not None else "", cmd, args
