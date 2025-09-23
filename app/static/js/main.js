// Main JavaScript file cho Todo List App

document.addEventListener('DOMContentLoaded', function() {
    console.log('Todo List App loaded successfully!');
    
    // Khởi tạo các chức năng
    initializeTooltips();
    initializeConfirmations();
    initializeFormValidation();
    initializeAutoHideAlerts();
    initializeDateInputs();
    initializeColorPickers();
});

/**
 * Khởi tạo Bootstrap tooltips
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Khởi tạo xác nhận trước khi xóa
 */
function initializeConfirmations() {
    // Xác nhận xóa task
    document.querySelectorAll('.delete-task').forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Bạn có chắc chắn muốn xóa công việc này?')) {
                e.preventDefault();
            }
        });
    });
    
    // Xác nhận xóa subject
    document.querySelectorAll('.delete-subject').forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Bạn có chắc chắn muốn xóa chủ đề này? Tất cả công việc trong chủ đề này cũng sẽ bị xóa.')) {
                e.preventDefault();
            }
        });
    });
    
    // Xác nhận xóa label
    document.querySelectorAll('.delete-label').forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Bạn có chắc chắn muốn xóa nhãn này?')) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Khởi tạo validation cho form
 */
function initializeFormValidation() {
    // Bootstrap form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Custom validation cho password
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            if (this.value.length < 6) {
                this.setCustomValidity('Mật khẩu phải có ít nhất 6 ký tự');
            } else {
                this.setCustomValidity('');
            }
        });
    });
}

/**
 * Tự động ẩn alerts sau 5 giây
 */
function initializeAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Khởi tạo date inputs với giá trị mặc định
 */
function initializeDateInputs() {
    const dateInputs = document.querySelectorAll('input[type="datetime-local"]');
    dateInputs.forEach(function(input) {
        // Set minimum date to today
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        
        const minDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
        input.setAttribute('min', minDateTime);
    });
}

/**
 * Khởi tạo color picker cho labels
 */
function initializeColorPickers() {
    const colorInputs = document.querySelectorAll('input[type="color"]');
    colorInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            // Hiển thị preview màu
            const preview = this.nextElementSibling;
            if (preview && preview.classList.contains('color-preview')) {
                preview.style.backgroundColor = this.value;
            }
        });
    });
}

/**
 * Toggle trạng thái task
 */
function toggleTaskStatus(taskId) {
    fetch(`/tasks/${taskId}/toggle`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            alert('Có lỗi xảy ra khi cập nhật trạng thái công việc');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Có lỗi xảy ra khi cập nhật trạng thái công việc');
    });
}

/**
 * Lọc tasks theo thời gian thực
 */
function filterTasks() {
    const searchInput = document.getElementById('search');
    const statusFilter = document.getElementById('status');
    const subjectFilter = document.getElementById('subject_id');
    const labelFilter = document.getElementById('label_id');
    
    if (!searchInput) return;
    
    const searchTerm = searchInput.value.toLowerCase();
    const statusValue = statusFilter ? statusFilter.value : '';
    const subjectValue = subjectFilter ? subjectFilter.value : '';
    const labelValue = labelFilter ? labelFilter.value : '';
    
    const taskItems = document.querySelectorAll('.task-item');
    
    taskItems.forEach(function(item) {
        const title = item.querySelector('.task-title').textContent.toLowerCase();
        const note = item.querySelector('.task-note') ? 
            item.querySelector('.task-note').textContent.toLowerCase() : '';
        const status = item.dataset.status || '';
        const subjectId = item.dataset.subjectId || '';
        const labelId = item.dataset.labelId || '';
        
        let show = true;
        
        // Filter by search term
        if (searchTerm && !title.includes(searchTerm) && !note.includes(searchTerm)) {
            show = false;
        }
        
        // Filter by status
        if (statusValue && status !== statusValue) {
            show = false;
        }
        
        // Filter by subject
        if (subjectValue && subjectId !== subjectValue) {
            show = false;
        }
        
        // Filter by label
        if (labelValue && labelId !== labelValue) {
            show = false;
        }
        
        item.style.display = show ? 'block' : 'none';
    });
}

/**
 * Copy link chia sẻ
 */
function copyShareLink(taskId) {
    const url = `${window.location.origin}/tasks/${taskId}`;
    navigator.clipboard.writeText(url).then(function() {
        showToast('Đã copy link chia sẻ');
    }).catch(function() {
        // Fallback cho trình duyệt cũ
        const textarea = document.createElement('textarea');
        textarea.value = url;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('Đã copy link chia sẻ');
    });
}

/**
 * Hiển thị toast notification
 */
function showToast(message, type = 'success') {
    // Tạo toast element
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert">
            <div class="toast-header">
                <i class="bi bi-${type === 'success' ? 'check-circle-fill text-success' : 'exclamation-triangle-fill text-warning'} me-2"></i>
                <strong class="me-auto">Thông báo</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Tự động xóa toast sau khi ẩn
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

/**
 * Tạo container cho toast
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

/**
 * Load more tasks (pagination)
 */
function loadMoreTasks(page) {
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    
    fetch(url.toString())
        .then(response => response.text())
        .then(html => {
            // Parse HTML và thêm tasks mới
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newTasks = doc.querySelectorAll('.task-item');
            const taskContainer = document.querySelector('.task-container');
            
            newTasks.forEach(task => {
                taskContainer.appendChild(task);
            });
            
            // Cập nhật URL
            window.history.pushState({}, '', url.toString());
        })
        .catch(error => {
            console.error('Error loading more tasks:', error);
            showToast('Có lỗi xảy ra khi tải thêm công việc', 'error');
        });
}

/**
 * Export tasks to CSV
 */
function exportTasks() {
    const tasks = [];
    document.querySelectorAll('.task-item').forEach(item => {
        const title = item.querySelector('.task-title').textContent;
        const status = item.dataset.status;
        const subject = item.dataset.subjectName || '';
        const label = item.dataset.labelName || '';
        const dueDate = item.dataset.dueDate || '';
        
        tasks.push({
            title,
            status,
            subject,
            label,
            dueDate
        });
    });
    
    // Tạo CSV content
    const csvContent = [
        ['Tiêu đề', 'Trạng thái', 'Chủ đề', 'Nhãn', 'Hạn chót'],
        ...tasks.map(task => [
            task.title,
            task.status === 'done' ? 'Hoàn thành' : 'Chưa xong',
            task.subject,
            task.label,
            task.dueDate
        ])
    ].map(row => row.join(',')).join('\n');
    
    // Download file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'tasks.csv';
    link.click();
}