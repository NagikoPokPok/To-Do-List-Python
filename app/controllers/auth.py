# Controller xử lý authentication (đăng ký, đăng nhập, đăng xuất)
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, User as UserSchema, Token
from app.utils.auth import (
    get_password_hash, 
    authenticate_user, 
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """
    Hiển thị trang đăng ký
    """
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Xử lý đăng ký người dùng mới
    """
    try:
        # Kiểm tra username đã tồn tại
        db_user = db.query(User).filter(User.username == username).first()
        if db_user:
            return templates.TemplateResponse(
                "auth/register.html", 
                {"request": request, "error": "Tên đăng nhập đã tồn tại"}
            )
        
        # Kiểm tra email đã tồn tại
        db_user = db.query(User).filter(User.email == email).first()
        if db_user:
            return templates.TemplateResponse(
                "auth/register.html", 
                {"request": request, "error": "Email đã được sử dụng"}
            )
        
        # Tạo user mới
        hashed_password = get_password_hash(password)
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return RedirectResponse(url="/login?message=Đăng ký thành công", status_code=303)
        
    except Exception as e:
        return templates.TemplateResponse(
            "auth/register.html", 
            {"request": request, "error": "Có lỗi xảy ra khi đăng ký"}
        )

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, message: str = None):
    """
    Hiển thị trang đăng nhập
    """
    return templates.TemplateResponse(
        "auth/login.html", 
        {"request": request, "message": message}
    )

@router.post("/login")
async def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Xử lý đăng nhập người dùng
    """
    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse(
            "auth/login.html", 
            {"request": request, "error": "Tên đăng nhập hoặc mật khẩu không đúng"}
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Tạo response và set cookie
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True
    )
    return response

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    API endpoint tạo access token (cho OAuth2)
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/logout")
async def logout():
    """
    Đăng xuất người dùng
    """
    response = RedirectResponse(url="/login?message=Đã đăng xuất thành công", status_code=303)
    response.delete_cookie(key="access_token")
    return response

@router.get("/profile", response_class=HTMLResponse)
async def profile_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Hiển thị trang hồ sơ người dùng
    """
    current_user = await get_current_active_user(request, db)
    return templates.TemplateResponse(
        "auth/profile.html", 
        {"request": request, "user": current_user}
    )