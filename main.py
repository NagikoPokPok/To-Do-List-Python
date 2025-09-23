# File chính khởi chạy ứng dụng FastAPI
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import database và models
from app.database import SessionLocal, engine
from app.models import Base
from app.utils.auth import get_current_active_user
from app.middleware import CookieAuthMiddleware

# Import các controllers
from app.controllers import auth, subjects, tasks, labels, notifications

# Tạo bảng trong database
Base.metadata.create_all(bind=engine)

# Khởi tạo FastAPI app
app = FastAPI(
    title="Todo List App",
    description="Ứng dụng quản lý công việc đơn giản",
    version="1.0.0"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thêm Cookie Auth Middleware
app.add_middleware(CookieAuthMiddleware)

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Cấu hình Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include các router từ controllers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(subjects.router, tags=["Subjects"])
app.include_router(tasks.router, tags=["Tasks"])
app.include_router(labels.router, tags=["Labels"])
app.include_router(notifications.router, tags=["Notifications"])

@app.get("/")
async def root():
    """
    Trang chủ - chuyển hướng tới login nếu chưa đăng nhập
    """
    return RedirectResponse(url="/login")

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """
    Xử lý lỗi 404 - Không tìm thấy trang
    """
    return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """
    Xử lý lỗi 500 - Lỗi server
    """
    return templates.TemplateResponse("errors/500.html", {"request": request}, status_code=500)

if __name__ == "__main__":
    # Chạy ứng dụng với uvicorn
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,  # Tự động reload khi có thay đổi code
        log_level="info"
    )