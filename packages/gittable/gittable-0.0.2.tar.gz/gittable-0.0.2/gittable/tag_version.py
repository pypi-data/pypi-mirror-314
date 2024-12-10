import argparse
import json
import os
import sys
from typing import Dict

try:
    from functools import cache  # type: ignore
except ImportError:
    from functools import lru_cache as cache
from pathlib import Path
from shlex import quote
from shutil import which
from subprocess import CalledProcessError, list2cmdline
from typing import Iterable, Tuple, Union

from gittable._utilities import check_output, get_exception_text


@cache
def _get_env() -> Dict[str, str]:
    """
    Get the environment variables
    """
    env: Dict[str, str] = os.environ.copy()
    env.pop("PIP_CONSTRAINT", None)
    return env


def _get_hatch_version(
    directory: Union[str, Path] = os.path.curdir,
) -> str:
    """
    Get the version of the package using `hatch`, if available
    """
    if isinstance(directory, str):
        directory = Path(directory)
    directory = str(directory.resolve())
    current_directory: str = str(Path.cwd().resolve())
    os.chdir(directory)
    hatch: str = which("hatch") or "hatch"
    output: str = ""
    try:
        # Note: We pass an empty dictionary of environment variables
        # to circumvent configuration issues caused by relative paths
        output = (
            check_output((hatch, "version"), env=_get_env()).strip()
            if hatch
            else ""
        )
    except Exception:
        pass
    finally:
        os.chdir(current_directory)
    return output


def _get_poetry_version(
    directory: Union[str, Path] = os.path.curdir,
) -> str:
    """
    Get the version of the package using `poetry`, if available
    """
    if isinstance(directory, Path):
        directory = str(Path(directory).resolve())
    current_directory: str = str(Path.cwd().resolve())
    os.chdir(directory)
    poetry: str = which("poetry") or "poetry"
    output: str = ""
    try:
        # Note: We pass an empty dictionary of environment variables
        # to prevent configuration issues caused by relative paths
        output = (
            check_output((poetry, "version"), env=_get_env())
            .strip()
            .rpartition(" ")[-1]
            if poetry
            else ""
        )
    except Exception:
        pass
    finally:
        os.chdir(current_directory)
    return output


def _get_pip_version(
    directory: Union[str, Path] = os.path.curdir,
) -> str:
    """
    Get the version of a package using `pip`
    """
    if isinstance(directory, str):
        directory = Path(directory)
    directory = str(directory.resolve())
    command: Tuple[str, ...] = ()
    try:
        command = (
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--no-compile",
            "-e",
            directory,
        )
        env: Dict[str, str] = os.environ.copy()
        env.pop("PIP_CONSTRAINT", None)
        check_output(command, env=env)
        command = (
            sys.executable,
            "-m",
            "pip",
            "list",
            "--format",
            "json",
            "--path",
            directory,
        )
        return json.loads(check_output(command, env=_get_env()))[0]["version"]
    except Exception as error:
        output: str = ""
        if isinstance(error, CalledProcessError):
            output = (error.output or error.stderr or b"").decode().strip()
            if output:
                output = f"{output}\n"
        current_directory: str = str(Path.cwd().resolve())
        raise RuntimeError(
            "Unable to determine the project version:\n"
            f"$ cd {quote(current_directory)} && {list2cmdline(command)}\n"
            f"{output}"
            f"{get_exception_text()}"
        ) from error


def _get_python_project_version(
    directory: Union[str, Path] = "",
) -> str:
    """
    Get a python project's version. Currently supports `hatch`, `poetry`, and
    any build tool compatible with `pip`.
    """
    return (
        _get_hatch_version(directory)
        or _get_poetry_version(directory)
        or _get_pip_version(directory)
    )


def tag_version(
    directory: Union[str, Path] = os.path.curdir, message: str = ""
) -> str:
    """
    Tag your project with the package version number *if* no pre-existing
    tag with that version number exists.

    Parameters:
        directory:
        message:

    Returns:
        The version number
    """
    if isinstance(directory, str):
        directory = Path(directory)
    directory = str(directory.resolve())
    version: str = _get_python_project_version(directory)
    current_directory: str = str(Path.cwd().resolve())
    os.chdir(directory)
    try:
        tags: Iterable[str] = map(
            str.strip,
            check_output(("git", "tag")).strip().split("\n"),
        )
        if version not in tags:
            check_output(
                ("git", "tag", "-a", version, "-m", message or version)
            )
    finally:
        os.chdir(current_directory)
    return version


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="gittable tag-version",
        description=(
            "Tag your repo with the package version, if a tag "
            "for that version doesn't already exist."
        ),
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=os.path.curdir,
        type=str,
        help=(
            "Your project directory. If not provided, the current "
            "directory will be used."
        ),
    )
    parser.add_argument(
        "-m",
        "--message",
        default="",
        type=str,
        help=(
            "The tag message. If not provided, the new version number is "
            "used."
        ),
    )
    arguments: argparse.Namespace = parser.parse_args()
    print(
        tag_version(directory=arguments.directory, message=arguments.message)
    )


if __name__ == "__main__":
    main()
