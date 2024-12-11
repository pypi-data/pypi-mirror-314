import os
from pathlib import Path
import tkinter
from tkinter import filedialog
from typing import Dict, List, Optional, Union


def get_files(
    folder_path: Union[str, Path],
    file_extension: Union[str, List[str]] = "",
    full_path: bool = True,
    recursive: bool = True,
) -> List[str]:

    folder_path = Path(folder_path)
    if not folder_path.is_dir():
        raise ValueError(f"{folder_path} is not a valid directory")

    if isinstance(file_extension, str):
        file_extension = [file_extension]

    pattern = "**/*" if recursive else "*"

    files = []
    for ext in file_extension:
        files.extend(folder_path.glob(f"{pattern}{ext}"))

    if not full_path:
        files = [f.name for f in files]
    else:
        files = [str(f) for f in files]

    return sorted(files)


def browse_folder(self, name_windows: str = "Chọn đường dẫn") -> Optional[str]:
    root = tkinter.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    tempdir = filedialog.askdirectory(
        parent=root, initialdir=self.__folder_path, title=name_windows
    )
    if tempdir:
        self.__folder_path = tempdir
        self.__call__(tempdir)
        return tempdir
    root.quit()
    return None


def check_file_error(
    self,
    folder_path: Union[str, Path],
    size_threshold: int = 0,
    excluded_files: List[str] = ["Thumbs.db"],
    check_permissions: bool = True,
) -> Dict[str, List[str]]:
    folder_path = Path(folder_path)
    error_files = {"empty": [], "excluded": [], "permission_error": []}

    for file in self.get_files(folder_path=folder_path):
        file_path = Path(file)
        try:
            if file_path.stat().st_size <= size_threshold:
                error_files["empty"].append(str(file_path))
            if file_path.name in excluded_files:
                error_files["excluded"].append(str(file_path))
            if check_permissions and not os.access(file_path, os.R_OK):
                error_files["permission_error"].append(str(file_path))
        except OSError as e:
            error_files["permission_error"].append(f"{file_path}: {str(e)}")

    return {k: v for k, v in error_files.items() if v}
