# Thư Viện Xử Lý File Python

Thư viện Python hỗ trợ xử lý và chuyển đổi file với nhiều tính năng.

## Cấu Trúc Thư Mục

```:
├── modules/
│   ├── __init__.py
│   ├── convert.py      - Chuyển đổi định dạng file
│   ├── file.py         - Xử lý file cơ bản
│   ├── image.py        - Xử lý hình ảnh
│   ├── llm.py          - Tích hợp mô hình ngôn ngữ
│   ├── ocr.py          - Nhận dạng ký tự quang học
│   └── pdf.py          - Xử lý file PDF
├── autoentry.py        - Dự án trích xuất dữ liệu
├── tests/              - Thư mục chứa các file test
├── poetry.lock         - File khóa phiên bản package
├── pyproject.toml      - Cấu hình project
└── README.md           - Tài liệu hướng dẫn
```

## Mô Tả Các Module

### convert.py

Module hỗ trợ chuyển đổi qua lại giữa các định dạng file khác nhau.

- Chuyển đổi hình ảnh sang PDF
- Chuyển đổi giữa các định dạng hình ảnh
- Kiểm tra tính tương thích của các định dạng

### file.py

Module xử lý các thao tác cơ bản với file.

- Đọc và ghi file
- Quản lý thông tin file
- Các thao tác với hệ thống file

### image.py

Module chuyên về xử lý hình ảnh.

- Chỉnh sửa kích thước ảnh
- Tối ưu hóa hình ảnh
- Xử lý metadata của ảnh
- Các thao tác cơ bản với hình ảnh

### llm.py

Module tích hợp mô hình ngôn ngữ.

- Xử lý văn bản
- Phân tích ngôn ngữ
- Chuyển đổi văn bản

### ocr.py

Module nhận dạng ký tự từ hình ảnh.

- Trích xuất text từ ảnh
- Quét và xử lý văn bản
- Hỗ trợ nhiều ngôn ngữ

### pdf.py

Module làm việc với file PDF.

- Tạo và chỉnh sửa PDF
- Ghép và tách file PDF
- Trích xuất text từ PDF
- Quản lý thông tin PDF

### autoentry.py

Dự án trích xuất dữ liệu.

## Cài Đặt

Dự án sử dụng Poetry để quản lý package. Để cài đặt:

```bash
poetry install
```

## Yêu Cầu Hệ Thống

- Python 3.10 trở lên
- Poetry
- Các thư viện phụ thuộc được liệt kê trong pyproject.toml

## Phát Triển

1. Clone repository về máy
2. Cài đặt Poetry
3. Chạy `poetry install` để cài đặt dependencies
4. Chạy `poetry shell` để kích hoạt môi trường ảo

## Kiểm Thử

```bash
poetry run pytest
```

## Bảo Mật

- Kiểm tra đầu vào cho mọi thao tác file
- Xử lý file an toàn
- Không thực thi mã không đáng tin cậy
- Xử lý đường dẫn file an toàn

## Giấy Phép

Dự án được phân phối dưới Giấy phép MIT.
