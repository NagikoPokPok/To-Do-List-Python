# Controller xử lý Subject (chủ đề công việc)
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Subject, User
from app.schemas import SubjectCreate, Subject as SubjectSchema
from app.utils.auth import get_current_active_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/subjects", response_class=HTMLResponse)
async def list_subjects(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Hiển thị danh sách tất cả subject của user
    """
    current_user = await get_current_active_user(request, db)
    subjects = db.query(Subject).filter(Subject.user_id == current_user.id).all()
    return templates.TemplateResponse(
        "subjects/list.html", 
        {"request": request, "subjects": subjects, "user": current_user}
    )

@router.get("/subjects/create", response_class=HTMLResponse)
async def create_subject_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Hiển thị trang tạo subject mới
    """
    current_user = await get_current_active_user(request, db)
    return templates.TemplateResponse(
        "subjects/create.html", 
        {"request": request, "user": current_user}
    )

@router.post("/subjects/create")
async def create_subject(
    request: Request,
    name: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Tạo subject mới
    """
    current_user = await get_current_active_user(request, db)
    try:
        # Kiểm tra tên subject đã tồn tại cho user này
        existing_subject = db.query(Subject).filter(
            Subject.name == name,
            Subject.user_id == current_user.id
        ).first()
        
        if existing_subject:
            return templates.TemplateResponse(
                "subjects/create.html",
                {"request": request, "error": "Tên chủ đề đã tồn tại", "user": current_user}
            )
        
        # Tạo subject mới
        db_subject = Subject(
            name=name,
            description=description,
            user_id=current_user.id
        )
        db.add(db_subject)
        db.commit()
        db.refresh(db_subject)
        
        return RedirectResponse(url="/subjects?message=Tạo chủ đề thành công", status_code=303)
        
    except Exception as e:
        return templates.TemplateResponse(
            "subjects/create.html",
            {"request": request, "error": "Có lỗi xảy ra khi tạo chủ đề", "user": current_user}
        )

@router.get("/subjects/{subject_id}/edit", response_class=HTMLResponse)
async def edit_subject_page(
    subject_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Hiển thị trang chỉnh sửa subject
    """
    current_user = await get_current_active_user(request, db)
    subject = db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.user_id == current_user.id
    ).first()
    
    if not subject:
        raise HTTPException(status_code=404, detail="Không tìm thấy chủ đề")
    
    return templates.TemplateResponse(
        "subjects/edit.html", 
        {"request": request, "subject": subject, "user": current_user}
    )

@router.post("/subjects/{subject_id}/edit")
async def update_subject(
    subject_id: int,
    request: Request,
    name: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Cập nhật thông tin subject
    """
    current_user = await get_current_active_user(request, db)
    try:
        subject = db.query(Subject).filter(
            Subject.id == subject_id,
            Subject.user_id == current_user.id
        ).first()
        
        if not subject:
            raise HTTPException(status_code=404, detail="Không tìm thấy chủ đề")
        
        # Kiểm tra tên subject đã tồn tại (trừ subject hiện tại)
        existing_subject = db.query(Subject).filter(
            Subject.name == name,
            Subject.user_id == current_user.id,
            Subject.id != subject_id
        ).first()
        
        if existing_subject:
            return templates.TemplateResponse(
                "subjects/edit.html",
                {
                    "request": request, 
                    "subject": subject,
                    "error": "Tên chủ đề đã tồn tại",
                    "user": current_user
                }
            )
        
        # Cập nhật subject
        subject.name = name
        subject.description = description
        db.commit()
        
        return RedirectResponse(url="/subjects?message=Cập nhật chủ đề thành công", status_code=303)
        
    except Exception as e:
        return templates.TemplateResponse(
            "subjects/edit.html",
            {
                "request": request, 
                "subject": subject,
                "error": "Có lỗi xảy ra khi cập nhật chủ đề",
                "user": current_user
            }
        )

@router.post("/subjects/{subject_id}/delete")
async def delete_subject(
    subject_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Xóa subject
    """
    current_user = await get_current_active_user(request, db)
    subject = db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.user_id == current_user.id
    ).first()
    
    if not subject:
        raise HTTPException(status_code=404, detail="Không tìm thấy chủ đề")
    
    # Xóa subject (các task liên quan sẽ bị xóa theo cascade)
    db.delete(subject)
    db.commit()
    
    return RedirectResponse(url="/subjects?message=Xóa chủ đề thành công", status_code=303)

# API endpoints
@router.get("/api/subjects", response_model=List[SubjectSchema])
async def get_subjects_api(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    API lấy danh sách subject của user
    """
    current_user = await get_current_active_user(request, db)
    subjects = db.query(Subject).filter(Subject.user_id == current_user.id).all()
    return subjects