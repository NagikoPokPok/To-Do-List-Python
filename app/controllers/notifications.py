# Controller xử lý Notification (thông báo nhắc việc)
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, date, timedelta
from app.database import get_db
from app.models import Task, User
from app.utils.auth import get_current_active_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/notifications", response_class=HTMLResponse)
async def notifications_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Hiển thị trang thông báo nhắc việc
    """
    current_user = await get_current_active_user(request, db)
    today = date.today()
    now = datetime.now()
    three_days_ago = now - timedelta(days=3)
    
    # Lấy task đến hạn hôm nay
    due_today_tasks = db.query(Task).filter(
        and_(
            Task.user_id == current_user.id,
            Task.status == "todo",
            Task.due_date >= today,
            Task.due_date < today + timedelta(days=1)
        )
    ).order_by(Task.due_date.asc()).all()
    
    # Lấy task quá hạn >= 3 ngày
    overdue_tasks = db.query(Task).filter(
        and_(
            Task.user_id == current_user.id,
            Task.status == "todo",
            Task.due_date < three_days_ago
        )
    ).order_by(Task.due_date.asc()).all()
    
    # Lấy task quá hạn < 3 ngày (để hiển thị riêng)
    recent_overdue_tasks = db.query(Task).filter(
        and_(
            Task.user_id == current_user.id,
            Task.status == "todo",
            Task.due_date < now,
            Task.due_date >= three_days_ago
        )
    ).order_by(Task.due_date.asc()).all()
    
    return templates.TemplateResponse(
        "notifications/index.html", 
        {
            "request": request, 
            "due_today_tasks": due_today_tasks,
            "overdue_tasks": overdue_tasks,
            "recent_overdue_tasks": recent_overdue_tasks,
            "user": current_user,
            "today": today,
            "now": now
        }
    )

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Hiển thị trang dashboard chính
    """
    current_user = await get_current_active_user(request, db)
    today = date.today()
    now = datetime.now()
    
    # Thống kê tổng quan
    total_tasks = db.query(Task).filter(Task.user_id == current_user.id).count()
    todo_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.status == "todo"
    ).count()
    done_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.status == "done"
    ).count()
    
    # Task đến hạn hôm nay
    due_today_count = db.query(Task).filter(
        and_(
            Task.user_id == current_user.id,
            Task.status == "todo",
            Task.due_date >= today,
            Task.due_date < today + timedelta(days=1)
        )
    ).count()
    
    # Task quá hạn
    overdue_count = db.query(Task).filter(
        and_(
            Task.user_id == current_user.id,
            Task.status == "todo",
            Task.due_date < now
        )
    ).count()
    
    # Task gần đây (5 task mới nhất)
    recent_tasks = db.query(Task).filter(
        Task.user_id == current_user.id
    ).order_by(Task.created_at.desc()).limit(5).all()
    
    return templates.TemplateResponse(
        "dashboard.html", 
        {
            "request": request, 
            "user": current_user,
            "stats": {
                "total_tasks": total_tasks,
                "todo_tasks": todo_tasks,
                "done_tasks": done_tasks,
                "due_today_count": due_today_count,
                "overdue_count": overdue_count
            },
            "recent_tasks": recent_tasks
        }
    )