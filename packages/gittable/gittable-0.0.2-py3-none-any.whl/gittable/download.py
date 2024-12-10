import argparse
import os
from glob import iglob
from itertools import chain
from shutil import move, rmtree
from subprocess import check_call
from tempfile import mkdtemp
from typing import Iterable, Iterator, List, Tuple

from ._utilities import update_url_user_password


def _iglob_recursive(pathname: str) -> Iterator[str]:
    return iglob(pathname, recursive=True)


def download(
    repo: str,
    files: Iterable[str] = ("**",),
    directory: str = "",
    branch: str = "",
    user: str = "",
    password: str = "",
) -> List[str]:
    """
    Download files from a git repository and return a list of the files
    downloaded.

    Parameters:
        repo: A git URL, as you would pass to `git clone`
        files: One or more
            [glob patterns](https://docs.python.org/3/library/glob.html)
            or relative file paths
        directory: The target directory (if not provided, the current
            directory is used)
        branch: A branch from which to retrieve (if not provided,
            files will be retrieved from HEAD)
        user:
        password:
    """
    if isinstance(files, str):
        files = (files,)
    if not directory:
        directory = os.path.curdir
    if user or password:
        repo = update_url_user_password(repo, user, password)
    directory = os.path.abspath(directory)
    # Shallow clone into a temp directory
    temp_directory: str = mkdtemp(prefix="git_download_")
    check_call(
        ("git", "clone", "-q", "--depth", "1", "--single-branch")
        + (("-b", branch) if branch else ())
        + (repo, temp_directory)
    )
    # Remove the git directory, so those files aren't accidentally matched
    rmtree(os.path.join(temp_directory, ".git"), ignore_errors=True)
    current_directory: str = os.path.abspath(os.path.curdir)
    path: str
    try:
        os.chdir(temp_directory)
        matched_files: Tuple[str, ...] = tuple(
            filter(
                os.path.isfile,
                (
                    os.path.join(
                        temp_directory,
                        path,
                    )
                    for path in chain(*map(_iglob_recursive, files))
                ),
            )
        )
    finally:
        os.chdir(current_directory)
    downloaded_paths: List[str] = []
    new_path: str
    for path in matched_files:
        relative_path: str = os.path.relpath(path, temp_directory)
        new_path = os.path.join(directory, relative_path)
        if os.path.sep in relative_path:
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
        print(new_path)
        move(path, new_path)
        downloaded_paths.append(new_path)
    rmtree(temp_directory, ignore_errors=True)
    return downloaded_paths


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="gittable download",
        description=(
            "Download files from a git repository matching one or more "
            "specified file names or glob patterns"
        ),
    )
    parser.add_argument(
        "-b",
        "--branch",
        default="",
        type=str,
        help="Retrieve files from BRANCH instead of the remote's HEAD",
    )
    parser.add_argument(
        "-d",
        "--directory",
        default="",
        type=str,
        help=(
            "The directory under which to save matched files. "
            "If not provided, files will be saved under the current "
            "directory."
        ),
    )
    parser.add_argument(
        "-u",
        "--user",
        default="",
        type=str,
        help="A username for accessing the repository",
    )
    parser.add_argument(
        "-p",
        "--password",
        default="",
        type=str,
        help="A password for accessing the repository",
    )
    parser.add_argument("repo", type=str, help="Reference repository")
    parser.add_argument(
        "file",
        nargs="*",
        type=str,
        help=(
            "One or more `glob` pattern(s) indicating a specific file or "
            "files to include. If not provided, all files "
            "in the repository will be included."
        ),
    )
    namespace: argparse.Namespace = parser.parse_args()
    download(
        namespace.repo,
        files=namespace.file or ("**",),
        directory=namespace.directory,
        branch=namespace.branch,
        user=namespace.user,
        password=namespace.password,
    )


if __name__ == "__main__":
    main()
