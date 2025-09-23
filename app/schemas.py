# Pydantic schemas để validate và serialize dữ liệu
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# ===== USER SCHEMAS =====
class UserBase(BaseModel):
    """Schema cơ bản cho User"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """Schema tạo User mới"""
    password: str

class UserUpdate(BaseModel):
    """Schema cập nhật thông tin User"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class User(UserBase):
    """Schema trả về thông tin User"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ===== SUBJECT SCHEMAS =====
class SubjectBase(BaseModel):
    """Schema cơ bản cho Subject"""
    name: str
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    """Schema tạo Subject mới"""
    pass

class SubjectUpdate(BaseModel):
    """Schema cập nhật Subject"""
    name: Optional[str] = None
    description: Optional[str] = None

class Subject(SubjectBase):
    """Schema trả về thông tin Subject"""
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ===== LABEL SCHEMAS =====
class LabelBase(BaseModel):
    """Schema cơ bản cho Label"""
    name: str
    color: str = "#FF6B6B"

class LabelCreate(LabelBase):
    """Schema tạo Label mới"""
    pass

class LabelUpdate(BaseModel):
    """Schema cập nhật Label"""
    name: Optional[str] = None
    color: Optional[str] = None

class Label(LabelBase):
    """Schema trả về thông tin Label"""
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ===== TASK SCHEMAS =====
class TaskBase(BaseModel):
    """Schema cơ bản cho Task"""
    title: str
    note: Optional[str] = None
    due_date: Optional[datetime] = None
    subject_id: int
    label_id: Optional[int] = None

class TaskCreate(TaskBase):
    """Schema tạo Task mới"""
    pass

class TaskUpdate(BaseModel):
    """Schema cập nhật Task"""
    title: Optional[str] = None
    note: Optional[str] = None
    due_date: Optional[datetime] = None
    subject_id: Optional[int] = None
    label_id: Optional[int] = None
    status: Optional[str] = None

class Task(TaskBase):
    """Schema trả về thông tin Task"""
    id: int
    status: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    # Thông tin từ các bảng liên quan
    subject: Optional[Subject] = None
    label: Optional[Label] = None
    
    class Config:
        from_attributes = True

# ===== AUTH SCHEMAS =====
class Token(BaseModel):
    """Schema cho JWT token"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema dữ liệu trong token"""
    username: Optional[str] = None

class LoginRequest(BaseModel):
    """Schema đăng nhập"""
    username: str
    password: str