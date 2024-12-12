import os
from typing import List
import colorlog
import fitz
import logging

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s: \t  %(asctime)s\t%(log_color)s%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
)
logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def count_pages_in_pdf(pdf_file_path):
    try:
        with fitz.open(pdf_file_path) as f:
            return f.page_count
    except (FileNotFoundError, IOError) as e:
        print(f"Không thể đọc file {pdf_file_path}: {e}")
    except Exception as e:
        print(f"Có lỗi xảy ra với file {pdf_file_path}: {e}")
    return 0


def split_pdf_to_one_page(input_path: str, output_dir: str = "split_pdfs") -> List[str]:
    try:
        # Tạo thư mục output nếu chưa tồn tại
        os.makedirs(output_dir, exist_ok=True)

        # Lấy tên file gốc (không bao gồm extension)
        base_filename = os.path.splitext(os.path.basename(input_path))[0]

        # Mở file PDF
        doc = fitz.open(input_path)
        output_paths = []

        # Duyệt qua từng trang
        for page_num in range(len(doc)):
            # Tạo một document PDF mới
            new_doc = fitz.open()

            # Chèn trang từ file gốc vào file mới
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

            # Tạo tên file cho trang hiện tại
            output_path = os.path.join(
                output_dir, f"{base_filename}_page_{page_num + 1}.pdf"
            )

            # Lưu file
            new_doc.save(output_path)
            new_doc.close()

            output_paths.append(output_path)
            logger.info(f"Created: {output_path}")

        # Đóng file PDF gốc
        doc.close()

        return output_paths

    except Exception as e:
        logger.error(f"Error splitting PDF {input_path}: {str(e)}")
        raise e
