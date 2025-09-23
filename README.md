# Todo List App - Ứng dụng quản lý công việc

Ứng dụng web quản lý công việc (Todo List) được xây dựng bằng Python FastAPI với giao diện thân thiện và các tính năng đầy đủ.

![Todo List App](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)

## 🌟 Tính năng chính

### 🔐 Xác thực & Quản lý tài khoản
- ✅ Đăng ký tài khoản mới
- ✅ Đăng nhập/Đăng xuất an toàn
- ✅ Quản lý hồ sơ cá nhân (tên, email, mật khẩu)
- ✅ JWT Authentication với cookie

### 📁 Quản lý chủ đề (Subjects)
- ✅ Tạo/Sửa/Xóa chủ đề công việc
- ✅ Phân loại công việc theo chủ đề
- ✅ Xem danh sách tất cả chủ đề

### ✏️ Quản lý công việc (Tasks)
- ✅ Tạo công việc với title, note, hạn chót, nhãn
- ✅ Chỉnh sửa thông tin công việc
- ✅ Xóa công việc
- ✅ Toggle trạng thái (todo ↔ done)
- ✅ Gán chủ đề và nhãn cho công việc

### 🔍 Tìm kiếm & Lọc nâng cao
- ✅ Lọc theo trạng thái (todo/done)
- ✅ Lọc theo chủ đề
- ✅ Lọc theo nhãn
- ✅ Lọc công việc đến hạn hôm nay
- ✅ Lọc công việc quá hạn
- ✅ Tìm kiếm theo từ khóa trong title/note

### 🏷️ Quản lý nhãn (Labels)
- ✅ Tạo nhãn với tên và màu sắc tùy chỉnh
- ✅ Chỉnh sửa và xóa nhãn
- ✅ Gán nhãn cho công việc

### 🔔 Thông báo nhắc việc
- ✅ Hiển thị công việc đến hạn hôm nay
- ✅ Hiển thị công việc quá hạn ≥ 3 ngày
- ✅ Dashboard tổng quan với thống kê

## 🛠️ Công nghệ sử dụng

- **Backend**: Python 3.8+ với FastAPI
- **Database**: SQLite với SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: JWT với bcrypt password hashing
- **Templates**: Jinja2
- **Validation**: Pydantic

## 📦 Cài đặt và chạy

### Yêu cầu hệ thống
- Python 3.8 hoặc cao hơn
- pip (Python package manager)
- Git

### Hướng dẫn cài đặt

1. **Clone repository**
```bash
git clone https://github.com/NagikoPokPok/To-Do-List-Python.git
cd To-Do-List-Python
```

2. **Tạo môi trường ảo**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Cài đặt dependencies**
```bash
pip install -r requirements.txt
```

4. **Chạy ứng dụng**
```bash
python main.py
```

5. **Truy cập ứng dụng**
Mở trình duyệt và vào: http://127.0.0.1:8000

## 📁 Cấu trúc dự án

```
To-Do-List-Python/
├── app/
│   ├── controllers/           # Xử lý logic nghiệp vụ
│   │   ├── auth.py           # Xác thực người dùng
│   │   ├── subjects.py       # Quản lý chủ đề
│   │   ├── tasks.py          # Quản lý công việc
│   │   ├── labels.py         # Quản lý nhãn
│   │   └── notifications.py  # Thông báo & dashboard
│   ├── models/               # Database models
│   │   └── __init__.py       # User, Subject, Task, Label models
│   ├── static/               # File tĩnh
│   │   ├── css/style.css     # CSS tùy chỉnh
│   │   └── js/main.js        # JavaScript
│   ├── templates/            # HTML templates
│   │   ├── auth/            # Templates xác thực
│   │   ├── subjects/        # Templates chủ đề
│   │   ├── tasks/           # Templates công việc
│   │   ├── labels/          # Templates nhãn
│   │   ├── notifications/   # Templates thông báo
│   │   └── base.html        # Layout chính
│   ├── utils/               # Tiện ích
│   │   └── auth.py          # JWT & password utilities
│   ├── database.py          # Cấu hình database
│   ├── schemas.py           # Pydantic schemas
│   └── middleware.py        # Custom middleware
├── venv/                    # Môi trường ảo
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
└── README.md               # File này
```

## 🎨 Giao diện

Ứng dụng sử dụng **màu đỏ tươi** làm màu chủ đạo với:
- Giao diện responsive, thân thiện trên mọi thiết bị
- Bootstrap 5 với custom CSS
- Dark/Light theme tự động theo hệ thống
- Icons từ Bootstrap Icons
- Animations mượt mà

## 🔧 Tùy chỉnh

### Thay đổi màu chủ đạo
Chỉnh sửa biến CSS trong `app/static/css/style.css`:
```css
:root {
    --primary-red: #dc3545;  /* Màu đỏ chính */
    --light-red: #f8d7da;    /* Màu đỏ nhạt */
    --dark-red: #721c24;     /* Màu đỏ đậm */
}
```

### Thêm chức năng mới
1. Tạo controller trong `app/controllers/`
2. Thêm route vào `main.py`
3. Tạo template HTML trong `app/templates/`

## 🔒 Bảo mật

- Mật khẩu được hash bằng bcrypt
- JWT tokens với thời hạn hết hạn
- CSRF protection
- SQL injection prevention với ORM
- XSS protection với template escaping

## 📈 Performance

- SQLite database với indexing
- Lazy loading cho các quan hệ
- CSS/JS minification
- Responsive images
- Efficient queries với SQLAlchemy

## 🧪 Testing

```bash
# Chạy tests (sẽ được bổ sung)
pytest

# Kiểm tra code style
flake8 app/

# Type checking
mypy app/
```

## 📝 API Documentation

Khi ứng dụng đang chạy, truy cập:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Dự án được phát hành dưới [MIT License](LICENSE).

## 👨‍💻 Tác giả

**NagikoPokPok**
- GitHub: [@NagikoPokPok](https://github.com/NagikoPokPok)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine

---

**⭐ Nếu dự án hữu ích, hãy cho một star! ⭐**