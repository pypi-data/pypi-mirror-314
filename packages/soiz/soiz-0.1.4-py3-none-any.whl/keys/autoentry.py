from pathlib import Path

import ipaddress
import json
import os
import shutil
import re
from fastapi import FastAPI, File, Request, UploadFile
import fitz
from pydantic import BaseModel
import logging
import colorlog
from starlette.middleware.base import BaseHTTPMiddleware
import torch
import pandas as pd
import time

# Import modules
from keys.modules.file import get_files_info
from keys.modules.llm import gen_llm_local
from keys.modules.ocr import process_file
from keys.modules.pdf import split_pdf_to_one_page


PROMPT = """
Trích xuất thông tin từ nội dung trên theo mẫu: 
{
	"Số và ký hiệu văn bản": "",
    "Cơ quan ban hành": "",
	"Ngày phát hành": "",
	"Loại văn bản": "",
	"Tiêu đề văn bản": "",
}

Yêu cầu:
Bạn là nhân viên nhập liệu chuyên nghiệp đang tiến hành nhập liệu các trường thông tin từ file văn bản. Tất cả các trường thông tin khác bạn cần trích xuất đúng giúp tôi. Cảm ơn bạn rất nhiều.

Hãy trích xuất kết quả từ file văn bản theo mẫu bên dưới và trả về dạng json, không trả về markdown:

**Số và ký hiệu văn bản** (không có thì để trống):

**Cơ quan ban hành**(Tóm tắt tên cơ quan ban hành văn bản, phần đầu của văn bản, không có phần "Cộng hòa xã hội chủ nghĩa Việt Nam" đâu nhé):

**Ngày phát hành** (Ngày phát hành phải theo định dạng: dd/MM/yyyy, không in ra mô tả này ra kết quả):

**Loại văn bản** (Loại văn bản chỉ thuộc 1 trong các loại sau: Nghị quyết, Quyết định ,Chỉ thị, Quy chế, Quy định, Thông cáo, Thông báo, Hướng dẫn, Chương trình, Kế hoạch, Phương án, Đề án, Dự án, Báo cáo, Biên bản, Tờ trình, Hợp đồng, Công văn, Công điện, Bản ghi nhớ, Bản thỏa thuận, Giấy ủy quyền, Giấy mời, Giấy giới thiệu, Giấy nghỉ phép, Phiếu gửi, Phiếu chuyển, Phiếu báo, Thư công, nếu không có thì để Khác):

**Tiêu đề văn bản** (bao gồm Loại văn bản, thông tin ngay sau loại văn bản):

Yêu cầu bắt buộc: tập trung nhận diện thật kỹ, chính xác giúp tôi; trả lời không lòng vòng, không diễn giải, trả lời đúng trọng tâm, không phân tích, mỗi ý của câu trả lời chỉ chứa 1 câu, không cần lưu ý, phân tích. Câu trả lời cần xuất ra theo mẫu, những từ trong () là mô tả của từng ý, cần bám sát để trả lời và không cần in ra trong câu trả lời.
"""

# Configure logging
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

# IP Filtering Configuration
allowed_ip_ranges = [
    ipaddress.ip_network("192.168.1.0/24"),
    ipaddress.ip_network("192.168.101.0/24"),
]


class IPFilterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = ipaddress.ip_address(request.client.host)
        response = await call_next(request)
        return response


class FilePathModel(BaseModel):
    path: str


def cropped_top_right_pdf(file_path):
    # Open PDF file
    doc = fitz.open(file_path)
    output_image_path = "cropped_top_right_page.png"

    # Get first page
    page = doc[0]

    # Get page dimensions
    rect = page.rect
    width = rect.width
    height = rect.height

    # Define crop area
    crop_rect = fitz.Rect(width * 0.8, 0, width, height * 0.05)

    # Extract image from cropped region
    pix = page.get_pixmap(clip=crop_rect)

    # Save image
    pix.save(output_image_path)
    # print(f"Image saved: {output_image_path}")

    # Close PDF
    doc.close()


def parse_json(json_str: str):
    try:
        json_str = json_str.strip()
        json_match = re.search(r"json\s*(.*?)\s*", json_str, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        return json.loads(json_str)
    except (json.JSONDecodeError, AttributeError):
        raise ValueError("Invalid JSON string")


def standardize_result(result):
    """Chuẩn hóa và sắp xếp các trường trong kết quả."""
    if result is None:
        return None

    standard_fields = {
        "Cơ quan ban hành": "",
        "Loại văn bản": "",
        "Ngày phát hành": "",
        "Số và ký hiệu văn bản": "",
        "Trang số": "",
        "Trích yếu nội dung": "",
    }

    for key in standard_fields.keys():
        if key in result:
            standard_fields[key] = result[key]

    return standard_fields


# FastAPI app setup
app = FastAPI()
app.add_middleware(IPFilterMiddleware)


@app.post("/upload")
def upload_file(uploaded_file: UploadFile = File(...)):
    path = f"files/{uploaded_file.filename}"
    with open(path, "w+b") as file:
        shutil.copyfileobj(uploaded_file.file, file)

    file_path_model = FilePathModel(path=path)
    logger.info(f'Upload: "{path}"')
    return auto_entry(file_path_model)


@app.post("/")
def auto_entry(file_path: FilePathModel):
    file = file_path.path
    logger.info(f'Processing: "{file}"')
    cropped_top_right_pdf(file)

    polygons, labels, layout_img, pred, bboxes = process_file(
        file,
        None,
        ["vi"],
        "layout",
        True,
        False,
        r"upload",
    )

    section_polygon = [bbox for label, bbox in zip(labels, bboxes)]

    _, _, ocr_trang_so_text = process_file(
        filepath=r"cropped_top_right_page.png",
        languages=["vi"],
        operation="ocr",
        use_pdf_boxes=True,
        output_dir="files",
    )

    trang_so = gen_llm_local(
        prompt=f"{ocr_trang_so_text}\n Số trong chuỗi là gì? Chỉ trả về kết quả, không diễn giải"
    )

    _, _, data_text = process_file(
        filepath=file,
        languages=["vi"],
        operation="ocr",
        use_pdf_boxes=True,
        output_dir="files",
    )

    count = 0
    while count < 3:
        try:
            result = parse_json(gen_llm_local(prompt=f"{data_text}\n{PROMPT}"))
            result["Trang số"] = trang_so
            if result is not None and "Tiêu đề văn bản" in result:
                result["Trích yếu nội dung"] = result.pop("Tiêu đề văn bản")
                print(result)
                return result

        except Exception as e:
            logger.error(f"auto_entry - Failed to load data! {e}")
        finally:
            count += 1

    torch.cuda.empty_cache()


def main(folder_path: str):
    all_files = get_files_info(
        directory_path=folder_path,
        recursive=False,
        file_filters={"extensions": [".pdf"]},
        return_options=["files"],
    )

    for pdf_file_full_path in all_files:
        start_time = time.time()
        results = []
        base_filename_file = Path(pdf_file_full_path).stem
        folder_output = os.path.join(folder_path, base_filename_file)
        Path(folder_output).mkdir(parents=True, exist_ok=True)

        # Chia file pdf thành các file pdf 1 trang
        for file in split_pdf_to_one_page(
            input_path=pdf_file_full_path, output_dir=folder_output
        ):

            pdf_path = os.path.join(folder_path, file)
            try:
                result = auto_entry(file_path=FilePathModel(path=pdf_path))
                standardized_result = standardize_result(result)
                if standardized_result:
                    results.append(standardized_result)
                    # print(f"Processed {file} successfully")
                    logger.info(f"Done: {file}")

            except Exception as e:
                print(f"Error reading {file}: {str(e)}")
            finally:
                print(f"{file} - {time.time() - start_time}")

        columns = [
            "Cơ quan ban hành",
            "Loại văn bản",
            "Ngày phát hành",
            "Số và ký hiệu văn bản",
            "Trang số",
            "Trích yếu nội dung",
        ]
        df = pd.DataFrame(results, columns=columns)

        output_file = f"{folder_output}.xlsx"
        df.to_excel(output_file, index=False)
        # shutil.rmtree(folder_output)
        print(f"File saved successfully at: {output_file}")
