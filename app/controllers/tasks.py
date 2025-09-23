# Controller xử lý Task (công việc)
from fastapi import APIRouter, Depends, HTTPException, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, date
from typing import List, Optional
from app.database import get_db
from app.models import Task, Subject, Label, User
from app.schemas import TaskCreate, Task as TaskSchema
from app.utils.auth import get_current_active_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/tasks", response_class=HTMLResponse)
async def list_tasks(
    request: Request,
    subject_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    label_id: Optional[int] = Query(None),
    due_today: Optional[bool] = Query(None),
    overdue: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Hiển thị danh sách task với các bộ lọc
    """
    current_user = await get_current_active_user(request, db)
    # Query cơ bản
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    # Áp dụng các bộ lọc
    if subject_id:
        query = query.filter(Task.subject_id == subject_id)
    
    if status:
        query = query.filter(Task.status == status)
    
    if label_id:
        query = query.filter(Task.label_id == label_id)
    
    if due_today:
        today = date.today()
        query = query.filter(Task.due_date >= today).filter(Task.due_date < today.replace(day=today.day + 1))
    
    if overdue:
        today = datetime.now()
        query = query.filter(Task.due_date < today).filter(Task.status == "todo")
    
    if search:
        query = query.filter(
            or_(
                Task.title.contains(search),
                Task.note.contains(search)
            )
        )
    
    # Lấy kết quả và sắp xếp
    tasks = query.order_by(Task.created_at.desc()).all()
    
    # Lấy danh sách subject và label để hiển thị trong filter
    subjects = db.query(Subject).filter(Subject.user_id == current_user.id).all()
    labels = db.query(Label).filter(Label.user_id == current_user.id).all()
    
    return templates.TemplateResponse(
        "tasks/list.html", 
        {
            "request": request, 
            "tasks": tasks, 
            "subjects": subjects,
            "labels": labels,
            "user": current_user,
            "filters": {
                "subject_id": subject_id,
                "status": status,
                "label_id": label_id,
                "due_today": due_today,
                "overdue": overdue,
                "search": search
            }
        }
    )

@router.get("/tasks/create", response_class=HTMLResponse)
async def create_task_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Hiển thị trang tạo task mới
    """
    current_user = await get_current_active_user(request, db)
    subjects = db.query(Subject).filter(Subject.user_id == current_user.id).all()
    labels = db.query(Label).filter(Label.user_id == current_user.id).all()
    
    return templates.TemplateResponse(
        "tasks/create.html", 
        {
            "request": request, 
            "subjects": subjects,
            "labels": labels,
            "user": current_user
        }
    )

@router.post("/tasks/create")
async def create_task(
    request: Request,
    title: str = Form(...),
    note: str = Form(None),
    subject_id: int = Form(...),
    label_id: Optional[str] = Form(None),  # Đổi thành str để xử lý chuỗi rỗng
    due_date: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Tạo task mới
    """
    current_user = await get_current_active_user(request, db)
    try:
        # Kiểm tra subject có thuộc về user không
        subject = db.query(Subject).filter(
            Subject.id == subject_id,
            Subject.user_id == current_user.id
        ).first()
        
        if not subject:
            subjects = db.query(Subject).filter(Subject.user_id == current_user.id).all()
            labels = db.query(Label).filter(Label.user_id == current_user.id).all()
            return templates.TemplateResponse(
                "tasks/create.html",
                {
                    "request": request,
                    "subjects": subjects,
                    "labels": labels,
                    "error": "Chủ đề không hợp lệ",
                    "user": current_user
                }
            )
        
        # Xử lý label_id - chuyển chuỗi rỗng thành None
        parsed_label_id = None
        if label_id and label_id.strip():
            try:
                parsed_label_id = int(label_id)
                # Kiểm tra label có thuộc về user không
                label = db.query(Label).filter(
                    Label.id == parsed_label_id,
                    Label.user_id == current_user.id
                ).first()
                if not label:
                    parsed_label_id = None
            except ValueError:
                parsed_label_id = None
        
        # Chuyển đổi due_date nếu có
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
            except ValueError:
                try:
                    parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    pass
        
        # Tạo task mới
        db_task = Task(
            title=title,
            note=note,
            subject_id=subject_id,
            label_id=parsed_label_id,
            due_date=parsed_due_date,
            user_id=current_user.id,
            status="todo"
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        return RedirectResponse(url="/tasks?message=Tạo công việc thành công", status_code=303)
        
    except Exception as e:
        subjects = db.query(Subject).filter(Subject.user_id == current_user.id).all()
        labels = db.query(Label).filter(Label.user_id == current_user.id).all()
        return templates.TemplateResponse(
            "tasks/create.html",
            {
                "request": request,
                "subjects": subjects,
                "labels": labels,
                "error": "Có lỗi xảy ra khi tạo công việc",
                "user": current_user
            }
        )

@router.get("/tasks/{task_id}/edit", response_class=HTMLResponse)
async def edit_task_page(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Hiển thị trang chỉnh sửa task
    """
    current_user = await get_current_active_user(request, db)
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Không tìm thấy công việc")
    
    subjects = db.query(Subject).filter(Subject.user_id == current_user.id).all()
    labels = db.query(Label).filter(Label.user_id == current_user.id).all()
    
    return templates.TemplateResponse(
        "tasks/edit.html", 
        {
            "request": request, 
            "task": task,
            "subjects": subjects,
            "labels": labels,
            "user": current_user
        }
    )

@router.post("/tasks/{task_id}/edit")
async def update_task(
    task_id: int,
    request: Request,
    title: str = Form(...),
    note: str = Form(None),
    subject_id: int = Form(...),
    label_id: Optional[str] = Form(None),  # Đổi thành str để xử lý chuỗi rỗng
    due_date: Optional[str] = Form(None),
    status: str = Form("todo"),
    db: Session = Depends(get_db)
):
    """
    Cập nhật thông tin task
    """
    current_user = await get_current_active_user(request, db)
    try:
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == current_user.id
        ).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Không tìm thấy công việc")
        
        # Kiểm tra subject có thuộc về user không
        subject = db.query(Subject).filter(
            Subject.id == subject_id,
            Subject.user_id == current_user.id
        ).first()
        
        if not subject:
            subjects = db.query(Subject).filter(Subject.user_id == current_user.id).all()
            labels = db.query(Label).filter(Label.user_id == current_user.id).all()
            return templates.TemplateResponse(
                "tasks/edit.html",
                {
                    "request": request,
                    "task": task,
                    "subjects": subjects,
                    "labels": labels,
                    "error": "Chủ đề không hợp lệ",
                    "user": current_user
                }
            )
        
        # Xử lý label_id - chuyển chuỗi rỗng thành None
        parsed_label_id = None
        if label_id and label_id.strip():
            try:
                parsed_label_id = int(label_id)
                # Kiểm tra label có thuộc về user không
                label = db.query(Label).filter(
                    Label.id == parsed_label_id,
                    Label.user_id == current_user.id
                ).first()
                if not label:
                    parsed_label_id = None
            except ValueError:
                parsed_label_id = None
        
        # Chuyển đổi due_date nếu có
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
            except ValueError:
                try:
                    parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    pass
        
        # Cập nhật task
        task.title = title
        task.note = note
        task.subject_id = subject_id
        task.label_id = parsed_label_id
        task.due_date = parsed_due_date
        task.status = status
        db.commit()
        
        return RedirectResponse(url="/tasks?message=Cập nhật công việc thành công", status_code=303)
        
    except Exception as e:
        subjects = db.query(Subject).filter(Subject.user_id == current_user.id).all()
        labels = db.query(Label).filter(Label.user_id == current_user.id).all()
        return templates.TemplateResponse(
            "tasks/edit.html",
            {
                "request": request,
                "task": task,
                "subjects": subjects,
                "labels": labels,
                "error": "Có lỗi xảy ra khi cập nhật công việc",
                "user": current_user
            }
        )

@router.post("/tasks/{task_id}/toggle")
async def toggle_task_status(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Toggle trạng thái task (todo <-> done)
    """
    current_user = await get_current_active_user(request, db)
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Không tìm thấy công việc")
    
    # Toggle status
    task.status = "done" if task.status == "todo" else "todo"
    db.commit()
    
    return RedirectResponse(url="/tasks", status_code=303)

@router.post("/tasks/{task_id}/delete")
async def delete_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Xóa task
    """
    current_user = await get_current_active_user(request, db)
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Không tìm thấy công việc")
    
    db.delete(task)
    db.commit()
    
    return RedirectResponse(url="/tasks?message=Xóa công việc thành công", status_code=303)