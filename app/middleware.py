# Middleware để xử lý cookie authentication
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from jose import JWTError, jwt
from app.utils.auth import SECRET_KEY, ALGORITHM
from app.database import SessionLocal
from app.models import User

class CookieAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware để xử lý authentication qua cookie
    """
    
    # Danh sách các path không cần authentication
    PUBLIC_PATHS = {
        "/", "/login", "/register", "/static", "/docs", "/redoc", "/openapi.json"
    }
    
    async def dispatch(self, request: Request, call_next):
        # Kiểm tra nếu path không cần authentication
        path = request.url.path
        if any(path.startswith(public_path) for public_path in self.PUBLIC_PATHS):
            return await call_next(request)
        
        # Lấy token từ cookie
        token = request.cookies.get("access_token")
        if token:
            try:
                # Loại bỏ "Bearer " prefix nếu có
                if token.startswith("Bearer "):
                    token = token[7:]
                
                # Decode token
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username = payload.get("sub")
                
                if username:
                    # Lấy user từ database
                    db = SessionLocal()
                    try:
                        user = db.query(User).filter(User.username == username).first()
                        if user:
                            # Thêm user vào request state
                            request.state.user = user
                            return await call_next(request)
                    finally:
                        db.close()
                        
            except JWTError:
                pass
        
        # Nếu không có token hoặc token không hợp lệ, redirect về login
        return RedirectResponse(url="/login", status_code=303)