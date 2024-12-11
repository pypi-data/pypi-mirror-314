from pathlib import Path
from codeassistant.functions_core import shell


def get_git_root(git_directory: Path | str) -> Path | None:
    git_directory = Path(git_directory)

    directory = shell(f"git -C {git_directory} rev-parse --show-toplevel", silent=True)
    if directory:
        output_dir = Path(directory)
    else:
        output_dir = None
    return output_dir


def get_gitignore_path(git_directory: Path | str) -> Path:
    git_directory = Path(git_directory)

    gitignore_path = git_directory / ".gitignore"
    assert gitignore_path.exists()
    assert gitignore_path.is_file()

    return gitignore_path


def get_gitignore_contents(
    git_directory: Path | str,
    remove_comments=True,
    remove_whitespace=True,
    remove_newline=True,
) -> list[str]:
    git_directory = Path(git_directory)
    gitignore_path = get_gitignore_path(git_directory)

    with open(gitignore_path, "r", encoding="utf-8") as f:
        lines: list[str] = f.readlines()

        if remove_comments:
            lines = [x for x in lines if not x.startswith("#")]
        if remove_whitespace:
            lines = [x for x in lines if x != "\n"]
        if remove_newline:
            lines = [x.removesuffix("\n") for x in lines]
    return lines


def get_git_diff(git_directory: Path | str) -> str:
    """git diff --cached (only staged files)"""
    git_directory = Path(git_directory)

    return shell(f'git -C "{git_directory}" diff --cached')


def get_git_merged_branches(git_directory: Path | str, exclude: list) -> list[str]:
    """Get git merged already branches on remote. wont list any remote branches."""
    git_directory = Path(git_directory)

    result: str = shell(
        f'git -C "{git_directory}" branch --merged | grep -Ev "(^\*|^\+|{"|".join(exclude)})"',
        silent=False,
    )

    branches: list[str] = [x.decode("utf-8").strip() for x in result.splitlines()]  # type: ignore
    return branches


def git_remove_branch(git_directory: Path | str, branch: str) -> str:
    """Remove provided branch"""
    git_directory = Path(git_directory)

    if not branch:
        raise TypeError("No branch")

    return shell(
        f'git -C "{git_directory}" branch -d {branch}',
        silent=False,
    )
