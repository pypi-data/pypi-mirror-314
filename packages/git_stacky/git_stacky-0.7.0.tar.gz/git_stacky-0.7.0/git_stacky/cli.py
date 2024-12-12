#!/usr/bin/env python3

import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Optional

import click

DEBUG = False

Command = str | list[str]


class WorkflowType(Enum):
    BRANCH = "branch"
    FORK = "fork"


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option()
def cli():
    pass


@cli.command("hack")
@click.argument("target", required=False)
@click.option("-c", "--carry", is_flag=True, default=False, help="Carry current changes to the new stack.")
@click.option("-m", "--main", is_flag=True, default=False, help="Stay on main, don't switch back to target.")
@click.option("-n", "--no-update", is_flag=True, default=False, help="Do not update main.")
def hack_cmd(target: str, carry: bool, main: bool, no_update: bool) -> None:
    """
    Update main and optionally create a new stack.

    \b
    Function:
      hack        => update main, stay on starting branch
      hack TARGET => update main, create TARGET from main if it doesn't exist, and switch to it

    \b
    Examples:
      (main)    hack          => update main
      (main)    hack FEATURE  => update main, create+switch to FEATURE
      (FEATURE) hack          => update main
      (FEATURE) hack main     => update main, switch to main
    """
    workflow = workflow_type()
    main_branch = main_branch_name()

    # Validate
    dirty_changes = try_run("git status --porcelain")
    if dirty_changes:
        if carry:
            must_run("git stash push --include-untracked", loud=True)
        else:
            cexit("current branch is dirty, aborting")
    start = current_branch()
    target = target or start or (main_branch if main else None)  # default to current branch, else main if --main
    if not start and not target:
        cexit("start and target branches empty (detached head and no target), aborting")
    validate_branches()
    create_target = validate_target_hack_branch(target, main_branch)

    # Update main
    if start != main_branch:
        must_run(f"git checkout {main_branch}", loud=True)
    if not no_update:
        if workflow == WorkflowType.FORK:
            must_run(f"git pull upstream {main_branch}", loud=True)
            must_run(f"git push origin {main_branch}", loud=True)
        else:
            must_run("git pull", loud=True)

    # Create/switch to stack
    if target != main_branch and not main:
        if create_target:
            must_run(f"git branch {target}_base", loud=True)
            must_run(f"git checkout -b {target}", loud=True)
        else:
            must_run(f"git checkout {target}", loud=True)

    # Carry changes
    if carry:
        must_run("git stash pop", loud=True)


@cli.command("rebase")
@click.argument("target", required=False)
@click.option("-d", "--done", is_flag=True, default=False, help="Finish rebasing a stack.")
def rebase_cmd(target: str, done: bool) -> None:
    """
    Rebase current stack onto main or the specified target.

    \b
    Examples:
      (FEATURE) rebase        => rebase FEATURE onto main
      (FEATURE) rebase TARGET => rebase FEATURE onto TARGET
      (FEATURE) rebase --done => finish rebasing FEATURE, if original rebase was interrupted
    """
    if done:
        rebase_done()
        return

    rebase_only(target)
    rebase_done()


@cli.command("stacks")
@click.option("-l", "--list", "just_list", is_flag=True, default=False, help="List all stacks.")
@click.option("-g", "--graph", is_flag=True, default=False, help="Print a graph of all stacks.")
@click.option("-n", "--max-count", type=int, help="Max commits to show in the graph.")
@click.option("-d", "--delete", multiple=True, help="Delete a stack.")
@click.option("-D", "--delete-force", multiple=True, help="Delete a stack forcefully.")
def stacks_cmd(just_list: bool, graph: bool, max_count: int, delete: tuple[str], delete_force: tuple[str]) -> None:
    """
    Manage and visualize stacks.

    \b
    Examples:
      stacks                     => list all stacks
      stacks --graph             => graph all stacks
      stacks --delete FEATURE    => delete FEATURE stack
    """
    if delete or delete_force:
        if delete:
            delete_stacks(list(delete))
        if delete_force:
            delete_stacks(list(delete_force), force=True)
        return
    if graph:
        try_run(
            [
                "git",
                "log",
                "--graph",
                "--format=format:%C(auto)%h%C(reset) %C(cyan)(%cr)%C(reset)%C(auto)%d%C(reset) %s %C(dim white)- %an%C(reset)",
            ]
            + (["--max-count", str(max_count)] if max_count else [])
            + get_stacks()
            + [main_branch_name()],
            loud=True,
        )
        return
    print_stacks(just_list)


@cli.command("absorb")
def absorb_cmd() -> None:
    """
    Automatically absorb changes into the stack.

    Requires git-absorb to be installed.
    """
    if not try_run("git absorb -h"):
        cexit("ERROR: git-absorb not installed, aborting")
    current = current_branch()
    if not current:
        cexit("current branch not found (detached head), aborting")
    if current not in get_stacks():
        cexit("current branch is not a stack, aborting")
    must_run(
        [
            "git",
            "-c",
            "sequence.editor=:",
            "-c",
            "absorb.autoStageIfNothingStaged=true",
            "absorb",
            "--and-rebase",
            "--base",
            f"{current}_base",
        ],
        loud=True,
    )


def rebase_only(target: str) -> None:
    """Rebase a stack onto the target."""
    br = must_run("git branch --show-current", "current branch not found, aborting")
    br_base = f"{br}_base"

    if try_run("git status --porcelain"):
        cexit("current branch is dirty, aborting")
    if not branch_exists(br):
        cexit(f"current branch '{br}' does not exist, aborting")
    if not branch_exists(br_base):
        cexit(f"stack may not be tracked by stacky: base branch '{br_base}' does not exist, aborting")
    if target and not branch_exists(target):
        log(f"target branch '{target}' does not exist, aborting")
    if not target:
        target = main_branch_name()
    if target == br:
        cexit("target branch is the same as current branch, aborting")
    if target == br_base:
        cexit("target branch is the same as base branch, aborting")

    save_rebase_args([target, br_base, br])

    out, err, errcode = run(["git", "rebase", "--onto", target, br_base, br], loud=True)
    if errcode:
        click.echo()
        click.echo(err)
        click.echo()
        click.echo("WARNING: rebase failed")
        click.echo("RUN: 'git stack rebase --done' to complete rebase, after resolving conflicts")
        exit(1)


def rebase_done() -> None:
    """Finish rebasing a stack."""
    args = load_rebase_args()
    if len(args) != 3:
        cexit("rebase arguments not found, aborting")
    target, br_base, br = args

    if not branch_exists(br):
        cexit(f"branch '{br}' does not exist, aborting")
    if not branch_exists(br_base):
        cexit(f"base branch '{br_base}' does not exist, aborting")

    must_run(f"git checkout {br_base}", loud=True)
    must_run(f"git reset --hard {target}", loud=True)
    must_run(f"git checkout {br}", loud=True)

    clear_rebase_args()


def save_rebase_args(args: list[str]) -> None:
    """Save null-separated rebase arguments to ~/.stacky/rebase_args."""
    stacky_dir = Path.home() / ".stacky"
    rebase_args_file = stacky_dir / "rebase_args"
    stacky_dir.mkdir(parents=True, exist_ok=True)
    rebase_args_file.write_text("\0".join(args))


def load_rebase_args() -> list[str]:
    """Load null-separated rebase arguments from ~/.stacky/rebase_args."""
    rebase_args_file = Path.home() / ".stacky" / "rebase_args"
    if not rebase_args_file.exists():
        return []
    return rebase_args_file.read_text().split("\0")


def clear_rebase_args() -> None:
    """Clear rebase arguments."""
    rebase_args_file = Path.home() / ".stacky" / "rebase_args"
    if rebase_args_file.exists():
        rebase_args_file.unlink()


def delete_stacks_all(force: bool = False) -> None:
    """Delete all stacks."""
    ss = get_stacks()
    ss = [s for s in ss if s if not s == current_branch()]
    delete_stacks(ss, force)


def delete_stacks(delete: list[str], force: bool = False) -> None:
    """Delete stacks."""
    delete = set(delete).intersection(get_stacks())
    delete = [s for s in delete] + [f"{s}_base" for s in delete]
    if not delete:
        log("no stacks to delete")
        return

    _, err, errcode = run(["git", "branch", "-D" if force else "-d"] + list(delete), loud=True)
    if errcode:
        click.echo()
        click.echo(err)
        click.echo()
        log("ERROR: delete failed")
        return


def print_stacks(just_list: bool = False) -> None:
    """List all tracked stacks."""
    ss = get_stacks() if just_list else [f"* {s}" if s == current_branch() else f"  {s}" for s in get_stacks()]
    if not ss:
        return
    click.echo("\n".join(ss))


def get_stacks() -> list[str]:
    """Return a list of tracked stacks."""
    branches = get_branches()
    ss = [b for b in branches if f"{b}_base" in branches]
    return ss


def get_branches() -> list[str]:
    """Return a list of branches."""
    return must_run("git branch --format='%(refname:short)'").split()


def main_branch_name() -> str:
    """Return the name of the main branch."""
    name = try_run("git symbolic-ref refs/remotes/origin/HEAD")
    if name:
        return name.split("/")[-1]

    name = try_run("git config --get init.defaultBranch")
    if name:
        return name

    return "master"


def workflow_type() -> WorkflowType:
    """Return the type of Git workflow."""
    if try_run("git remote get-url upstream"):
        return WorkflowType.FORK
    return WorkflowType.BRANCH


def branch_exists(target: str) -> bool:
    """Check if a branch exists."""
    return bool(try_run(f"git show-ref refs/heads/{target}"))


def current_branch() -> str:
    """Return the name of the current branch, or an empty string if detached."""
    return try_run("git branch --show-current")


def validate_branches(target: str = "") -> None:
    """Validate branch names."""
    bs = get_branches()
    ss = get_stacks()
    for b in bs:
        if b.endswith("_base_base"):
            log(f"WARNING: potentially colliding base branch '{b}' detected")
        if b.endswith("_base") and strip_suffix(b, "_base") not in ss:
            log(f"WARNING: potentially orphaned base branch '{b}' detected")


def validate_target_hack_branch(target: str, main_branch: str) -> bool:
    """Validate the target branch for the hack command. Returns True iff the target needs to be created."""
    if target == main_branch:
        return False

    target_exists = branch_exists(target)
    target_base_exists = branch_exists(f"{target}_base")

    if not target_exists and not target_base_exists:
        return True
    if target_exists and not target_base_exists:
        cexit(f"ERROR: target branch '{target}' exists, but base branch '{target}_base' does not, aborting")
    if not target_exists and target_base_exists:
        cexit(f"ERROR: base branch '{target}_base' exists, but target branch '{target}' does not, aborting")
    return False


def strip_suffix(s: str, suffix: str) -> str:
    """Strip a suffix from a string."""
    if s.endswith(suffix):
        return s[: -len(suffix)]
    return s


def run(command: Command, loud: bool = False) -> tuple[str, str, int]:
    """Run a shell command and return the output."""
    if DEBUG:
        click.echo(f"DEBUG: {command}")
    shell = isinstance(command, str)
    if loud:
        res = subprocess.run(command, shell=shell)
        return "", "", res.returncode
    else:
        res = subprocess.run(command, shell=shell, text=True, capture_output=True)
        return res.stdout.strip(), res.stderr.strip(), res.returncode


def must_run(command: Command, fail_msg: Optional[str] = None, loud: bool = False) -> str:
    """Run a shell command and return the output, or exit on error."""
    out, err, errcode = run(command, loud=loud)
    if errcode:
        msg = fail_msg or f"ERROR: failed to run command '{command}'"
        if loud:
            msg = fail_msg or f"ERROR: failed to run command '{command}'\n\n{out}\n\n{err}"
        cexit(msg)
    return out


def try_run(command: Command, loud: bool = False) -> Optional[str]:
    """Run a shell command and return the output, or return None on error."""
    out, _, errcode = run(command, loud)
    if errcode:
        return ""
    return out


def cexit(msg: str) -> None:
    """Print an error message and exit."""
    log(msg)
    sys.exit(1)


def log(msg: str) -> None:
    """Print a message."""
    click.echo(fmt_log(msg))


def fmt_log(msg: str) -> str:
    """Capitalize the first letter of a log message."""
    if not msg:
        return msg
    return msg[0].upper() + msg[1:]


if __name__ == "__main__":
    cli()
