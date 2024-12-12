import os
import fitz
import img2pdf

def jpg_to_pdf(input_path, output_path):
    # Mở file ảnh JPG và chuyển đổi sang PDF
    # jpg dpi bao nhiêu thì khi convert sẽ giữ nguyên
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(input_path))


def pdf_to_jpg(input_path, output_folder):
    # Mở tài liệu PDF
    document = fitz.open(input_path)

    # Lặp qua từng trang trong tài liệu
    for page_number in range(document.page_count):
        # Lấy trang hiện tại
        page = document.load_page(page_number)

        # Chuyển đổi trang sang hình ảnh
        pix = page.get_pixmap(dpi=300)

        # Tạo tên file cho từng trang
        output_path = f"{output_folder}/page_{page_number + 1}.jpg"

        # Lưu hình ảnh dưới dạng JPG
        if not os.path.exists(output_path):
            pix.save(output_path)

        print(f"Đã lưu {output_path}")

    # Đóng tài liệu
    document.close()


def multiple_jpgs_to_pdf(input_jpg_paths, output_pdf_path):
    # Mở tất cả các tệp JPG và lưu dưới dạng một tệp PDF
    with open(output_pdf_path, "wb") as pdf_file:
        pdf_file.write(img2pdf.convert(input_jpg_paths))