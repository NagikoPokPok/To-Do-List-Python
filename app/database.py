# Cấu hình cơ sở dữ liệu SQLite
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Đường dẫn tới file database SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo_app.db"

# Tạo engine kết nối database
# check_same_thread=False cho phép sử dụng database từ nhiều thread
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Tạo SessionLocal để quản lý session database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho tất cả các model
Base = declarative_base()

# Dependency để lấy database session
def get_db():
    """
    Tạo và quản lý database session
    Đảm bảo session được đóng sau khi sử dụng
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()