# Hướng dẫn cài đặt và chạy Todo List App

## Yêu cầu hệ thống
- Python 3.8 trở lên
- pip (Python package manager)
- Git (để clone repository)

## Bước 1: Clone repository
```bash
git clone https://github.com/NagikoPokPok/To-Do-List-Python.git
cd To-Do-List-Python
```

## Bước 2: Tạo và kích hoạt môi trường ảo (Virtual Environment)

### Trên Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Trên macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Bước 3: Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### Danh sách thư viện chính:
- **FastAPI**: Framework web hiện đại cho Python
- **Uvicorn**: ASGI server để chạy ứng dụng FastAPI
- **SQLAlchemy**: ORM để làm việc với cơ sở dữ liệu
- **Python-multipart**: Xử lý form data và file upload
- **Jinja2**: Template engine cho HTML
- **Python-jose**: Xử lý JWT tokens
- **Passlib**: Mã hóa mật khẩu
- **Python-dotenv**: Quản lý biến môi trường

## Bước 4: Chạy ứng dụng

### Cách 1: Chạy trực tiếp với Python
```bash
python main.py
```

### Cách 2: Chạy với Uvicorn
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## Bước 5: Truy cập ứng dụng
Mở trình duyệt và truy cập: http://127.0.0.1:8000

## Cấu trúc thư mục
```
To-Do-List-Python/
├── app/
│   ├── controllers/        # Các controller xử lý logic
│   ├── models/            # Định nghĩa database models
│   ├── static/            # File tĩnh (CSS, JS, images)
│   ├── templates/         # Template HTML
│   ├── utils/             # Tiện ích và helper functions
│   ├── database.py        # Cấu hình database
│   └── schemas.py         # Pydantic schemas
├── venv/                  # Môi trường ảo (sẽ tạo sau khi setup)
├── main.py               # File chính để chạy ứng dụng
├── requirements.txt      # Danh sách thư viện
└── README.md            # File này
```

## Chức năng chính của ứng dụng

### 1. Xác thực người dùng (Authentication)
- Đăng ký tài khoản mới
- Đăng nhập/Đăng xuất
- Quản lý hồ sơ cá nhân

### 2. Quản lý chủ đề (Subjects)
- Tạo, sửa, xóa chủ đề công việc
- Xem danh sách tất cả chủ đề

### 3. Quản lý công việc (Tasks)
- Tạo công việc mới với title, note, hạn chót, nhãn
- Chỉnh sửa thông tin công việc
- Xóa công việc
- Chuyển đổi trạng thái (todo ↔ done)

### 4. Tìm kiếm và lọc
- Lọc theo trạng thái (todo/done)
- Lọc theo chủ đề
- Lọc theo nhãn
- Lọc công việc đến hạn hôm nay
- Lọc công việc quá hạn
- Tìm kiếm theo từ khóa

### 5. Quản lý nhãn (Labels)
- Tạo nhãn với tên và màu sắc
- Chỉnh sửa và xóa nhãn

### 6. Thông báo (Notifications)
- Hiển thị công việc đến hạn hôm nay
- Hiển thị công việc quá hạn ≥ 3 ngày

## Gỡ lỗi thường gặp

### Lỗi "Module not found"
```bash
pip install -r requirements.txt
```

### Lỗi "Permission denied" trên macOS/Linux
```bash
sudo python3 -m pip install -r requirements.txt
```

### Lỗi port đã được sử dụng
Thay đổi port trong file main.py hoặc chạy:
```bash
uvicorn main:app --port 8001
```

### Database bị lỗi
Xóa file `todo_app.db` và chạy lại ứng dụng để tạo database mới.

## Tùy chỉnh ứng dụng

### Thay đổi màu chủ đạo
Chỉnh sửa file `app/static/css/style.css` và thay đổi biến `--primary-red`.

### Thêm chức năng mới
1. Tạo controller mới trong `app/controllers/`
2. Thêm route vào `main.py`
3. Tạo template HTML trong `app/templates/`

### Cấu hình database khác
Chỉnh sửa `SQLALCHEMY_DATABASE_URL` trong `app/database.py`.

## Đóng góp

Nếu bạn muốn đóng góp vào dự án:
1. Fork repository
2. Tạo branch mới cho feature
3. Commit changes
4. Push và tạo Pull Request

## Liên hệ hỗ trợ

Nếu gặp vấn đề khi cài đặt hoặc sử dụng, vui lòng:
1. Kiểm tra lại các bước cài đặt
2. Xem phần gỡ lỗi ở trên
3. Tạo issue trên GitHub repository

## Giấy phép
Dự án được phát hành dưới giấy phép MIT. Xem file LICENSE để biết chi tiết.

---

**Chúc bạn sử dụng ứng dụng hiệu quả! 🎉**