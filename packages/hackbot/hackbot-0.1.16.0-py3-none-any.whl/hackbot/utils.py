import zipfile
import os
import traceback
from typing import Optional, Generator, List
from git import Repo, InvalidGitRepositoryError
from loguru import logger as log
from pathlib import Path
from tomllib import load as toml_load
import importlib.metadata
from termcolor import colored
from enum import Enum
import tempfile


class Endpoint(str, Enum):
    RUN = "run"
    SCOPE = "scope"


def url_format(address: str, port: Optional[int]) -> str:
    """Format the URL for the hackbot service."""
    scheme = address.split(":")[0]
    if len(address.split(":")) > 1:
        rest = ":".join(address.split(":")[1:])
    else:
        # No protocol specified, assume by port number if exists
        rest = ""
        if port is not None:
            if port == 80:
                return f"http://{address}"
            else:
                return f"https://{address}:{port}"
        else:
            return f"http://{address}"
    assert scheme in ["http", "https"], "Invalid URI scheme"
    return f"{scheme}:{rest}:{port}" if (port is not None) else f"{scheme}:{rest}"


def compress_source_code(
    source_path: str,
    zip_path: str,
    size_limit: int = 256 * 1024 * 1024,
    git_info: dict[str, str] | None = None,
) -> None:
    """Compress the source code directory into a zip file.
    If git_info (from get_repo_info) is provided, we only add the files that are tracked by git."""

    def file_iter() -> Generator[Path, None, None]:
        if git_info is not None:
            git_repo = Repo(source_path, search_parent_directories=True)

            # Get staged files (both new and modified)
            staged_files = {item.a_path for item in git_repo.index.diff("HEAD")}
            # Get modified but unstaged files
            modified_files = {item.a_path for item in git_repo.index.diff(None)}

            # First yield all files from the current commit
            for entry in git_repo.commit().tree.traverse():
                file_path = Path(git_repo.working_dir) / Path(entry.path)
                if str(file_path.relative_to(git_repo.working_dir)) not in modified_files:
                    yield file_path

            # Then yield all staged files
            for file_path in staged_files:
                yield Path(git_repo.working_dir) / Path(file_path)
        else:
            for root, _, files in os.walk(source_path):
                for file in files:
                    yield Path(os.path.join(root, file))

    try:
        zip_size = 0
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_iter():  # file: Path
                # Skip .zip files
                if not file_path.name.endswith(".zip"):
                    arcname = file_path.relative_to(source_path)
                    if not file_path.exists():
                        log.warning(
                            f"File not found (probably a broken symlink?), skipping sending to server: {file_path}"
                        )
                        continue
                    if file_path.stat().st_size + zip_size > size_limit:
                        raise RuntimeError(
                            f"Source code archive is too large to be scanned. Must be less than 256MB, but after adding {file_path} it is {(zip_size + file_path.stat().st_size) // 1024 // 1024}MB."
                        )
                    else:
                        zip_size += file_path.stat().st_size
                    zipf.write(str(file_path), str(arcname))
    except Exception:
        raise RuntimeError(f"Failed to compress source code: {traceback.format_exc()}")


def get_repo_info(repo_path: Path | str) -> dict[str, str] | None:
    """Returns the repo info of a github (specifically) repo at repo_path, or None if the repo is not a github repo
    The info includes repo name, commit, repo owner, and branch name.
    Info also includes relative path from the real repo root (since we search parent directories for the repo) to the repo_path
    """
    if isinstance(repo_path, str):
        repo_path = Path(repo_path)
    try:
        repo = Repo(repo_path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        return None
    repo_info = {}
    repo_info["source_root"] = str(repo_path.relative_to(repo.working_dir))
    for remote in repo.remotes:
        if "github.com" in remote.url:
            if "git@" in remote.url:
                mode = "ssh"
            else:
                mode = "http"

            # Example repo url: git@github.com:GatlingX/some_repo.git
            repo_info["repo_name"] = remote.url.split("/")[-1]
            # Remove the .git from the end of the repo name
            repo_info["repo_name"] = repo_info["repo_name"][:-4]

            repo_info["commit_hash"] = repo.head.commit.hexsha

            if mode == "http":
                # Example repo url: https://github.com/GatlingX/some_repo
                repo_info["repo_owner"] = remote.url.split("/")[-2]
            else:
                # Example repo url: git@github.com:GatlingX/some_repo.git
                repo_info["repo_owner"] = remote.url.split(":")[-1].split("/")[0]
            for branch in repo.branches:
                if branch.commit == repo.head.commit:
                    repo_info["branch_name"] = branch.name
                    break
                else:
                    repo_info["branch_name"] = "HEAD"
            break
    else:
        return None
    return repo_info


def get_version() -> str:
    """Get the version of the hackbot package."""
    # In development mode, we use the version from the pyproject.toml file
    try:
        with open(str(Path(__file__).parent.parent.parent / "pyproject.toml"), "rb") as f:
            return toml_load(f)["project"]["version"]
    except FileNotFoundError:
        # In production mode, we use the version from the package metadata

        return importlib.metadata.version("hackbot")


def postprocess_scope_results(
    source_path: Path | str, scope_files: List[str], ambiguous_files: List[str]
) -> None:
    """Postprocess the scope analysis results.

    Takes the scope and ambiguous files from the analysis and writes them to disk.
    If scope files exist, writes them to scope.txt and adds to git if in a repo.
    If ambiguous files exist, writes them to ambiguous.txt for manual review.

    Args:
        source_path: Path to the source code directory
        scope_files: List of files determined to be in scope
        ambiguous_files: List of files that need manual review

    Returns:
        None
    """
    save_scope_files: bool = False
    save_ambiguous_files: bool = False

    if len(scope_files) == 0 or scope_files[0] is None:
        if len(ambiguous_files) == 0 or ambiguous_files[0] is None:
            log.error(colored("❌ No files in scope", "red"))
        else:
            save_ambiguous_files = True
            log.error(
                colored(
                    "❌ No files in scope, but ambiguous files found requiring manual review", "red"
                )
            )
    else:
        save_scope_files = True
        if len(ambiguous_files) == 0 or ambiguous_files[0] is None:
            log.info(colored("✅ Scope analysis completed successfully", "green"))
        else:
            save_ambiguous_files = True
            log.warning(colored("⚠️ Some files are ambiguous and require manual review", "yellow"))

    def check_name_exists(name: str) -> str:
        """Check if a file already exists. If it does, write to a temporary file and return the new name."""
        if os.path.exists(name):
            original_name = name
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                name = f"{name}_{temp_file.name.split('/')[-1]}"
            log.warning(
                colored(
                    f"⚠️ {original_name} already exists, writing to a temporary file {name}",
                    "yellow",
                )
            )
        return name

    if save_scope_files:
        # Check if scope.txt already exists
        scope_file = check_name_exists(Path(source_path) / "scope.txt")
        # Write the scope files to the scope.txt file
        with open(scope_file, "w") as f:
            for file in scope_files[0]:
                f.write(file + "\n")
        repo_info = get_repo_info(source_path)
        if repo_info is not None:
            repo = Repo(source_path, search_parent_directories=True)
            repo.index.add([scope_file])

    if save_ambiguous_files:
        # Check if ambiguous.txt already exists
        ambiguous_file = check_name_exists(Path(source_path) / "ambiguous.txt")
        # Write the ambiguous files to the ambiguous.txt file
        with open(ambiguous_file, "w") as f:
            for file in ambiguous_files[0]:
                f.write(file + "\n")
