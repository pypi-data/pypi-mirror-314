import os
from pathlib import Path
import tkinter
from tkinter import filedialog
from typing import Dict, List, Optional, Tuple, Union

from PyPDF2 import PdfReader
from collections import defaultdict
import fnmatch


def get_files_info(
    directory_path: str,
    full_path: bool = True,
    recursive: bool = True,
    return_options: List[str] = ["files"],
    file_filters: Dict = None,
) -> Union[List[str], Dict, int]:
    """
    Quét thư mục và trả về thông tin theo các tùy chọn

    Args:
        directory_path (str): Đường dẫn thư mục cần quét
        full_path (bool): True để trả về đường dẫn đầy đủ, False chỉ trả về tên file
        recursive (bool): True để quét cả thư mục con
        return_options (List[str]): Danh sách các tùy chọn kết quả trả về
            - "files": Danh sách các file
            - "count_by_ext": Số lượng file theo phần mở rộng
            - "pdf_pages": Tổng số trang PDF
        file_filters (Dict): Bộ lọc file với các tùy chọn:
            - "extensions": List[str] - Lọc theo phần mở rộng (vd: ['.txt', '.pdf'])
            - "patterns": List[str] - Lọc theo mẫu (vd: ['*.txt', 'data*'])
            - "exclude_patterns": List[str] - Loại trừ các file theo mẫu
            - "min_size": int - Kích thước tối thiểu (bytes)
            - "max_size": int - Kích thước tối đa (bytes)

    Returns:
        Union[List[str], Dict, int]: Kết quả theo tùy chọn đã chọn
    """

    results = {}
    all_files = []
    file_filters = file_filters or {}

    def should_include_file(file_path: str) -> bool:
        """Kiểm tra xem file có thỏa mãn các điều kiện lọc không"""
        try:
            # Kiểm tra phần mở rộng
            if "extensions" in file_filters:
                ext = Path(file_path).suffix.lower()
                if ext not in file_filters["extensions"]:
                    return False

            # Kiểm tra theo pattern
            if "patterns" in file_filters:
                matched = False
                for pattern in file_filters["patterns"]:
                    if fnmatch.fnmatch(os.path.basename(file_path), pattern):
                        matched = True
                        break
                if not matched:
                    return False

            # Kiểm tra exclude patterns
            if "exclude_patterns" in file_filters:
                for pattern in file_filters["exclude_patterns"]:
                    if fnmatch.fnmatch(os.path.basename(file_path), pattern):
                        return False

            # Kiểm tra kích thước
            if "min_size" in file_filters or "max_size" in file_filters:
                size = os.path.getsize(file_path)
                if "min_size" in file_filters and size < file_filters["min_size"]:
                    return False
                if "max_size" in file_filters and size > file_filters["max_size"]:
                    return False

            return True
        except Exception as e:
            print(f"Lỗi khi kiểm tra file {file_path}: {str(e)}")
            return False

    # Hàm quét files
    def scan_files(path: str) -> None:
        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_file():
                        file_path = entry.path
                        if should_include_file(file_path):
                            all_files.append(file_path if full_path else entry.name)
                    elif entry.is_dir() and recursive:
                        scan_files(entry.path)
        except PermissionError:
            print(f"Không có quyền truy cập thư mục: {path}")
        except Exception as e:
            print(f"Lỗi khi quét thư mục {path}: {str(e)}")

    # Quét files
    scan_files(directory_path)

    # Xử lý các tùy chọn trả về
    for option in return_options:
        if option == "files":
            results["files"] = all_files

        elif option == "count_by_ext":
            ext_count = defaultdict(int)
            for file in all_files:
                ext = Path(file).suffix.lower()
                ext_count[ext or "no_extension"] += 1
            results["count_by_ext"] = dict(ext_count)

        elif option == "pdf_pages":
            total_pages = 0
            for file in all_files:
                if file.lower().endswith(".pdf"):
                    try:
                        full_path = (
                            file if full_path else os.path.join(directory_path, file)
                        )
                        with open(full_path, "rb") as f:
                            pdf = PdfReader(f)
                            total_pages += len(pdf.pages)
                    except Exception as e:
                        print(f"Lỗi khi đọc file PDF {file}: {str(e)}")
            results["pdf_pages"] = total_pages

    # Trả về kết quả phù hợp
    if len(return_options) == 1:
        return results[return_options[0]]
    return results


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
