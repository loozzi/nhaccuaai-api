# NhacCuaAi API (FastAPI Version)

API cho ứng dụng NhacCuaAi, được phát triển với FastAPI và SQLAlchemy.

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd nhaccuaai-api
```

2. Tạo môi trường ảo và kích hoạt:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Cài đặt các thư viện:
```bash
pip install -r requirements.txt
```

4. Thiết lập biến môi trường:
- Sao chép file `.env.example` thành `.env` và cập nhật các thông tin cần thiết

## Chạy ứng dụng

### Phát triển

```bash
python app.py
```

Ứng dụng sẽ chạy tại địa chỉ: `http://localhost:8000`

### Sản xuất

Sử dụng Gunicorn hoặc Uvicorn để chạy ứng dụng trong môi trường sản xuất:

```bash
uvicorn src:app --host 0.0.0.0 --port 8000
```

## Tài liệu API

Sau khi chạy ứng dụng, bạn có thể truy cập tài liệu API tại:

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## Migrations

Để tạo và chạy migrations:

```bash
# Tạo các bảng trong database
python migrate.py --create

# Chạy migrations
python migrate.py
```

## Cấu trúc dự án

```
├── app.py              # File chạy chính
├── migrate.py          # File quản lý migrations
├── requirements.txt    # Danh sách các thư viện
├── src/                # Thư mục chính
│   ├── __init__.py     # Khởi tạo ứng dụng FastAPI
│   ├── api/            # API endpoints
│   ├── controllers/    # Controllers
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   └── utils/          # Utilities
├── migrations/         # Migrations files
└── songs/              # Thư mục chứa các file âm nhạc
```
```
<copilot-edited-file>
```markdown
# NhacCuaAi API (FastAPI Version)

API cho ứng dụng NhacCuaAi, được phát triển với FastAPI và SQLAlchemy.

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd nhaccuaai-api
```

2. Tạo môi trường ảo và kích hoạt:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Cài đặt các thư viện:
```bash
pip install -r requirements.txt
```

4. Thiết lập biến môi trường:
- Sao chép file `.env.example` thành `.env` và cập nhật các thông tin cần thiết

## Chạy ứng dụng

### Phát triển

```bash
python app.py
```

Ứng dụng sẽ chạy tại địa chỉ: `http://localhost:8000`

### Sản xuất

Sử dụng Gunicorn hoặc Uvicorn để chạy ứng dụng trong môi trường sản xuất:

```bash
uvicorn src:app --host 0.0.0.0 --port 8000
```

## Tài liệu API

Sau khi chạy ứng dụng, bạn có thể truy cập tài liệu API tại:

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## Migrations

Để tạo và chạy migrations:

```bash
# Tạo các bảng trong database
python migrate.py --create

# Chạy migrations
python migrate.py
```

## Cấu trúc dự án

```
├── app.py              # File chạy chính
├── migrate.py          # File quản lý migrations
├── requirements.txt    # Danh sách các thư viện
├── src/                # Thư mục chính
│   ├── __init__.py     # Khởi tạo ứng dụng FastAPI
│   ├── api/            # API endpoints
│   ├── controllers/    # Controllers
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   └── utils/          # Utilities
├── migrations/         # Migrations files
└── songs/              # Thư mục chứa các file âm nhạc
```
