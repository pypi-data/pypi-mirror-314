from PIL import Image
from typing import List
from pathlib import Path

import ipaddress
import json
import os
import shutil
import re
import PyPDF2
from fastapi import FastAPI, File, Request, UploadFile
import fitz
from pydantic import BaseModel
import logging
import colorlog
from starlette.middleware.base import BaseHTTPMiddleware
import torch
import pandas as pd
import numpy as np
import cv2
import time

# Import modules
from modules.file import get_files
from modules.llm import gen_llm_local
from modules.ocr import process_file


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


def cropped_top_left_pdf(file_path):
    output_image_path = "cropped_top_left_page.png"
    doc = fitz.open(file_path)
    page = doc[0]
    rect = page.rect
    width = rect.width
    height = rect.height
    crop_rect = fitz.Rect(0, 0, width * 0.46, height * 0.11)
    pix = page.get_pixmap(clip=crop_rect)
    pix.save(output_image_path)
    print(f"Image saved: {output_image_path}")
    doc.close()


def cropped_image(section_polygons, file_path, zoom=2):
    output_image_path = "cropped_image.png"
    doc = fitz.open(file_path)
    page = doc[0]
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    pdf_width, pdf_height = page.rect.width, page.rect.height
    scaled_polygons = [
        [
            (int(point[0] * zoom), int((pdf_height - point[1]) * zoom))
            for point in section_polygons
        ]
    ]
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    mask = np.zeros_like(img_cv[:, :, 0])
    cv2.fillPoly(mask, np.array(scaled_polygons, dtype=np.int32), 255)
    masked_img = cv2.bitwise_and(img_cv, img_cv, mask=mask)
    x_coords = [point[0] for point in scaled_polygons[0]]
    y_coords = [point[1] for point in scaled_polygons[0]]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    cropped_img = masked_img[y_min:y_max, x_min:x_max]
    cv2.imwrite(output_image_path, cropped_img)
    print(f"Image saved: {output_image_path}")
    doc.close()
    return output_image_path


def crop_image_from_bbox(image_path, bbox, output_path=None):
    try:
        with Image.open(image_path) as img:
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            cropped_img = img.crop(bbox)
            if output_path is None:
                filename = image_path.rsplit(".", 1)[0]
                output_path = f"{filename}_cropped.png"
            cropped_img.save(output_path, "PNG")
            return output_path
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None


def get_left_region(coordinates):
    return min(coordinates, key=lambda coord: (coord[1], coord[0]))


def find_header_region(boxes):
    min_y = float("inf")
    leftmost_top_box = None
    for box in boxes:
        x1, y1 = box[0], box[1]
        if y1 <= min_y and x1 < 150:
            min_y = y1
            leftmost_top_box = box
    return leftmost_top_box

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

    layout_img.save("cqbh.png")

    top_left = find_header_region(section_polygon)
    output_file = crop_image_from_bbox("cqbh.png", top_left)

    # ocr_co_quan_ban_hanh, _, _ = process_file(
    #     r"cqbh_cropped.png",
    #     None,
    #     ["vi"],
    #     "ocr",
    #     True,
    #     False,
    #     r"files",
    # )

    # co_quan_ban_hanh = gen_llm_local(
    #     prompt=f"{ocr_co_quan_ban_hanh}\n Tên cơ quan là gì, chuẩn hóa lại tên cơ quan sao cho có nghĩa trong tiếng việt, không sinh ra? Chỉ trả lời, không diễn giải"
    # )

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
            # result["Cơ quan ban hành"] = str(co_quan_ban_hanh).split("-")[-1]
            if result is not None and "Tiêu đề văn bản" in result:
                result["Trích yếu nội dung"] = result.pop("Tiêu đề văn bản")
                print(result)
                return result

        except Exception as e:
            logger.error(f"auto_entry - Failed to load data! {e}")
        finally:
            count += 1

    torch.cuda.empty_cache()


def count_pdf_pages(directory):
    total_pages = 0
    pdf_files = 0

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".pdf"):
                pdf_files += 1
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, "rb") as file:
                        reader = PyPDF2.PdfReader(file)
                        total_pages += len(reader.pages)
                except Exception as e:
                    print(f"count_pdf_pages - Lỗi khi đọc file {file_path}: {str(e)}")

    return total_pages, pdf_files


def split_pdf(input_path: str, output_dir: str = "split_pdfs") -> List[str]:
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


def main():
    folder_path = r"C:\Users\vanna\Downloads"

    # Lấy tất cả đường dẫn file pdf trong thư mục và các thư mục con (nếu có)
    for pdf_file_full_path in get_files(
        folder_path=folder_path, file_extension="pdf", full_path=True, recursive=False
    ):
        start_time = time.time()
        results = []
        base_filename_file = os.path.splitext(os.path.basename(pdf_file_full_path))[0]
        folder_output = os.path.join(folder_path, base_filename_file)
        Path(folder_output).mkdir(parents=True, exist_ok=True)

        # Chia file pdf thành các file pdf 1 trang
        for file in split_pdf(input_path=pdf_file_full_path, output_dir=folder_output):

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


# if __name__ == "__main__":
#     uvicorn.run(app=app, host="192.168.1.15", port=5921, workers=True)

main()
