# Controller xử lý Label (nhãn công việc)
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Label, User
from app.schemas import LabelCreate, Label as LabelSchema
from app.utils.auth import get_current_active_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/labels", response_class=HTMLResponse)
async def list_labels(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Hiển thị danh sách tất cả label của user
    """
    current_user = await get_current_active_user(request, db)
    labels = db.query(Label).filter(Label.user_id == current_user.id).all()
    return templates.TemplateResponse(
        "labels/list.html", 
        {"request": request, "labels": labels, "user": current_user}
    )

@router.get("/labels/create", response_class=HTMLResponse)
async def create_label_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Hiển thị trang tạo label mới
    """
    current_user = await get_current_active_user(request, db)
    return templates.TemplateResponse(
        "labels/create.html", 
        {"request": request, "user": current_user}
    )

@router.post("/labels/create")
async def create_label(
    request: Request,
    name: str = Form(...),
    color: str = Form("#FF6B6B"),
    db: Session = Depends(get_db)
):
    """
    Tạo label mới
    """
    current_user = await get_current_active_user(request, db)
    try:
        # Kiểm tra tên label đã tồn tại cho user này
        existing_label = db.query(Label).filter(
            Label.name == name,
            Label.user_id == current_user.id
        ).first()
        
        if existing_label:
            return templates.TemplateResponse(
                "labels/create.html",
                {"request": request, "error": "Tên nhãn đã tồn tại", "user": current_user}
            )
        
        # Tạo label mới
        db_label = Label(
            name=name,
            color=color,
            user_id=current_user.id
        )
        db.add(db_label)
        db.commit()
        db.refresh(db_label)
        
        return RedirectResponse(url="/labels?message=Tạo nhãn thành công", status_code=303)
        
    except Exception as e:
        return templates.TemplateResponse(
            "labels/create.html",
            {"request": request, "error": "Có lỗi xảy ra khi tạo nhãn", "user": current_user}
        )

@router.get("/labels/{label_id}/edit", response_class=HTMLResponse)
async def edit_label_page(
    label_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Hiển thị trang chỉnh sửa label
    """
    current_user = await get_current_active_user(request, db)
    label = db.query(Label).filter(
        Label.id == label_id,
        Label.user_id == current_user.id
    ).first()
    
    if not label:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhãn")
    
    return templates.TemplateResponse(
        "labels/edit.html", 
        {"request": request, "label": label, "user": current_user}
    )

@router.post("/labels/{label_id}/edit")
async def update_label(
    label_id: int,
    request: Request,
    name: str = Form(...),
    color: str = Form("#FF6B6B"),
    db: Session = Depends(get_db)
):
    """
    Cập nhật thông tin label
    """
    current_user = await get_current_active_user(request, db)
    try:
        label = db.query(Label).filter(
            Label.id == label_id,
            Label.user_id == current_user.id
        ).first()
        
        if not label:
            raise HTTPException(status_code=404, detail="Không tìm thấy nhãn")
        
        # Kiểm tra tên label đã tồn tại (trừ label hiện tại)
        existing_label = db.query(Label).filter(
            Label.name == name,
            Label.user_id == current_user.id,
            Label.id != label_id
        ).first()
        
        if existing_label:
            return templates.TemplateResponse(
                "labels/edit.html",
                {
                    "request": request, 
                    "label": label,
                    "error": "Tên nhãn đã tồn tại",
                    "user": current_user
                }
            )
        
        # Cập nhật label
        label.name = name
        label.color = color
        db.commit()
        
        return RedirectResponse(url="/labels?message=Cập nhật nhãn thành công", status_code=303)
        
    except Exception as e:
        return templates.TemplateResponse(
            "labels/edit.html",
            {
                "request": request, 
                "label": label,
                "error": "Có lỗi xảy ra khi cập nhật nhãn",
                "user": current_user
            }
        )

@router.post("/labels/{label_id}/delete")
async def delete_label(
    label_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Xóa label
    """
    current_user = await get_current_active_user(request, db)
    label = db.query(Label).filter(
        Label.id == label_id,
        Label.user_id == current_user.id
    ).first()
    
    if not label:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhãn")
    
    # Xóa label (các task sẽ có label_id = null)
    db.delete(label)
    db.commit()
    
    return RedirectResponse(url="/labels?message=Xóa nhãn thành công", status_code=303)

# API endpoints
@router.get("/api/labels", response_model=List[LabelSchema])
async def get_labels_api(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    API lấy danh sách label của user
    """
    current_user = await get_current_active_user(request, db)
    labels = db.query(Label).filter(Label.user_id == current_user.id).all()
    return labels