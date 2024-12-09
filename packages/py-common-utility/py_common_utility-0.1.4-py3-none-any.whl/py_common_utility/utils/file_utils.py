import glob
import json
import os
import shutil
from pathlib import Path
from typing import Callable, Any

from pathspec import pathspec, PathSpec
import hashlib
from ..obj.comm_logger import get_comm_logger

_HARD_CODE_SKIP_GIT_FILES = ['.git', '.gitignore']
_HARD_CODE_SKIP_DIRS = ["bin" "build" "logs" "out" ".git" ".gradle" ".idea" "init-model" "resources"]

logger = get_comm_logger(__name__)


def ensure_file_exists(file_path):
    # Ensure the directory exists; if not, create it
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # Check if the file exists, if not, create an empty file
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as f:
            pass  # Create an empty file


def ensure_directory_exists(file_path: str):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def delete_folder_and_contents(folder_path: str):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            shutil.rmtree(folder_path)
        except Exception as e:  # work on python 3.x
            logger.error('del fails: ' + str(e))
            _rmdir_unlink(folder_path)
        logger.info(f"Successfully deleted the folder and all its contents: {folder_path}")
    else:
        logger.info(f"The folder does not exist or is not a directory: {folder_path}")


def _rmdir_unlink(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            _rmdir_unlink(item)
        else:
            item.unlink()
    directory.rmdir()


def get_file_extension(filename):
    return Path(filename).suffix.lstrip('.')


def get_filename(file_path: str):
    path = Path(file_path)
    return path.name


def get_relative_path(file_path: str, base_folder_name: str):
    path = Path(file_path)
    try:
        # Find the index of the base folder in the path parts
        base_index = path.parts.index(base_folder_name)
        # Construct the relative path from the base folder
        relative_path = Path(*path.parts[base_index + 1:])
        return str(relative_path)
    except ValueError:
        raise ValueError(f"Base folder '{base_folder_name}' not found in the given path.")


def find_gitignore_spec(folder: str) -> PathSpec | None:
    gitignore_path = os.path.join(folder, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        return pathspec.PathSpec.from_lines('gitwildmatch', gitignore_content.splitlines())
    else:
        return None


class GitAction:
    def __init__(self, root_gitignore_spec: PathSpec | None,
                 folder_gitignore_spec: PathSpec | None,
                 action: Callable[[str, str, str], Any]):
        self.root_gitignore_spec: PathSpec | None = root_gitignore_spec
        self.folder_gitignore_spec: PathSpec | None = folder_gitignore_spec
        self.action: Callable[[str, str, str], Any] = action

    def is_ignore(self, folder: str, file_name: str) -> bool:
        path = os.path.join(folder, file_name).replace("\\", "/")
        if os.path.isdir(path):
            file_name += "/"
        if self.root_gitignore_spec and self.root_gitignore_spec.match_file(file_name):
            print(f"跳過忽略: {file_name}")
            return True
        if self.folder_gitignore_spec and self.folder_gitignore_spec.match_file(file_name):
            print(f"跳過忽略: {file_name}")
            return True
        if self.root_gitignore_spec and self.root_gitignore_spec.match_file(folder):
            print(f"跳過忽略: {folder}")
            return True
        if self.folder_gitignore_spec and self.folder_gitignore_spec.match_file(folder):
            print(f"跳過忽略: {folder}")
            return True
        if self.root_gitignore_spec and self.root_gitignore_spec.match_file(path):
            print(f"跳過忽略: {path}")
            return True
        if self.folder_gitignore_spec and self.folder_gitignore_spec.match_file(path):
            print(f"跳過忽略: {path}")
            return True
        return False


def _action_git_file(action: GitAction, dirpath: str, filename: str):
    file_path = os.path.join(dirpath, filename)
    # 跳過匹配 .gitignore 模式的文件
    if filename in _HARD_CODE_SKIP_GIT_FILES:
        return
    if action.is_ignore(dirpath, filename):
        return
        # 嘗試以文本模式打開文件以檢查其是否為二進制文件
    content = get_content(file_path)
    if content:
        action.action(file_path, filename, content)


def get_content_json(file_path: str) -> dict:
    with open(file_path) as f:
        ans = json.load(f)
        return ans


def get_content_json_or_default(file_path: str, d: dict) -> dict:
    try:
        return get_content_json(file_path)
    except Exception as e:  # work on python 3.x
        logger.info('Failed to get_content_json_or_default: ' + str(e))
        return d


def get_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
            # 將內容與文件名一起保存到數據庫中
    except Exception as e:
        print(f"{e} error skip: {file_path}")
        return ""


# args1 : file_path
# args2 : filename
# args3 : content

def for_each_git_project(folder: str, action: Callable[[str, str, str], Any]):
    root_gitignore_spec = find_gitignore_spec(folder)
    git_action = GitAction(
        root_gitignore_spec=root_gitignore_spec,
        folder_gitignore_spec=None,
        action=action
    )
    _action_git_folder(git_action, folder)
    print("所有文件都已加載到數據庫中並包含文件名信息。")


def _action_git_folder(action: GitAction, folder: str):
    all_files_dirs = os.listdir(folder)
    folder_gitignore_spec = find_gitignore_spec(folder)
    git_action = GitAction(
        root_gitignore_spec=action.root_gitignore_spec,
        folder_gitignore_spec=folder_gitignore_spec,
        action=action.action
    )
    files = [file for file in all_files_dirs if os.path.isfile(os.path.join(folder, file))]
    dirs = [file for file in all_files_dirs if os.path.isdir(os.path.join(folder, file))]
    for file_name in files:
        _action_git_file(git_action, folder, file_name)

    for dir_name in dirs:
        if action.is_ignore(folder, dir_name):
            continue
        if dir_name in _HARD_CODE_SKIP_DIRS:
            continue
        _d_path = os.path.join(folder, dir_name)
        _d_folder_gitignore_spec = find_gitignore_spec(_d_path)
        _d_git_action = GitAction(
            root_gitignore_spec=action.root_gitignore_spec,
            folder_gitignore_spec=_d_folder_gitignore_spec,
            action=action.action
        )
        _action_git_folder(_d_git_action, _d_path)


def action_normal_folder(folder: str, file_cb: Callable[[str, str, str], Any],
                         dir_predicate: Callable[[str], bool] = None):
    """
    file_cb:
        args1 : folder
        args2 : filename
        args3 : file_path
    dir_predicate:
        args1 : dir_path
        return bool > True: scan this folder  |  False: skip this folder
    """
    if dir_predicate and not dir_predicate(folder):
        return
    all_files_dirs = os.listdir(folder)
    files = [file for file in all_files_dirs if os.path.isfile(os.path.join(folder, file))]
    dirs = [file for file in all_files_dirs if os.path.isdir(os.path.join(folder, file))]
    for file_name in files:
        file_path = os.path.join(folder, file_name)
        file_cb(folder, file_name, file_path)

    for dir_name in dirs:
        _d_path = os.path.join(folder, dir_name)
        action_normal_folder(_d_path, file_cb, dir_predicate)


def save_string_to_file(file_path: str, content: str) -> None:
    with open(file_path, 'w') as file:
        file.write(content)


def get_file_sha1(file_path: str) -> str:
    sha1_hash = hashlib.sha1()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha1_hash.update(chunk)
    return sha1_hash.hexdigest()
