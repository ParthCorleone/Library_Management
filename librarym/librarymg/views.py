from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta #, timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .models import Book, CustomUser, BookIssuance, BookRequest, Notification ,Task
from .forms import CustomUserCreationForm, BookForm, BookRequestForm , TaskForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == role:
            login(request, user)
            return redirect(f'{role.lower()}_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials or role'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    if request.user.role != 'Admin':
        return redirect('login')
    users = CustomUser.objects.all()
    books = Book.objects.all()
    issuances = BookIssuance.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users, 'books': books, 'issuances': issuances})

@login_required
def add_book(request):
    if request.user.role != 'Admin':
        return redirect('login')
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

@login_required
def delete_book(request, book_id):
    if request.user.role != 'Admin':
        return redirect('login')
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('admin_dashboard')

@login_required
def add_user(request):
    if request.user.role != 'Admin':
        return redirect('login')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'add_user.html', {'form': form})

@login_required
def delete_user(request, user_id):
    if request.user.role != 'Admin':
        return redirect('login')
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('admin_dashboard')

@login_required
def assign_task(request):
    if request.user.role not in ['Admin', 'Librarian']:
        return redirect('login')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            messages.success(request, f"Task assigned to {task.staff.username}.")
            return redirect('admin_dashboard' if request.user.role == 'Admin' else 'librarian_dashboard')
    else:
        form = TaskForm()
    if request.user.role == 'Admin':
        return render(request, 'assign_task_a.html', {'form': form})
    else:
        return render(request,'assign_task_l.html',{'form':form})

def view_task(request):
    if request.user.role not in ['Admin', 'Librarian']:
        return redirect('login')
    tasks = Task.objects.all()
    if request.user.role == 'Admin':
        return render(request, 'view_task_a.html', {'tasks': tasks})
    else:
        return render(request, 'view_task_l.html', {'tasks': tasks})

@login_required
def customer_dashboard(request):
    if request.user.role != 'Customer':
        return redirect('login')
    books = Book.objects.all()
    issued_books = BookIssuance.objects.filter(issued_to=request.user, returned_date__isnull=True)
    return render(request, 'customer_dashboard.html', {'books': books, 'issued_books': issued_books})

@login_required
def request_book(request, book_id):
    if request.user.role != 'Customer':
        return redirect('login')
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            book_request = form.save(commit=False)
            book_request.book = book
            book_request.requested_by = request.user
            book_request.save()
            return redirect('customer_dashboard')
    else:
        form = BookRequestForm()
    return render(request, 'request_book.html', {'form': form, 'book': book})

@login_required
def send_overdue_notification(request, issuance_id):
    if request.user.role != 'Librarian':
        return redirect('login')
    issuance = get_object_or_404(BookIssuance, id=issuance_id)
    if issuance.is_overdue() and not issuance.returned_date:
        Notification.objects.create(
            user=issuance.issued_to,
            message=f"The book '{issuance.book.title}' is overdue. Please return it immediately to avoid fines.",
        )
        messages.success(request, f"Overdue notification sent to {issuance.issued_to.username}.")
    else:
        messages.error(request, "This book is not overdue.")
    return redirect('librarian_dashboard')

@login_required
def librarian_dashboard(request):
    if request.user.role != 'Librarian':
        return redirect('login')
    
    books = Book.objects.all()
    pending_requests = BookRequest.objects.filter(status='Pending')
    issued_books = BookIssuance.objects.filter(returned_date__isnull=True)
    
    return render(request, 'librarian_dashboard.html', {
        'books': books,
        'pending_requests': pending_requests,
        'issued_books': issued_books,
    })

@login_required
def approve_request(request, request_id):
    if request.user.role != 'Librarian':
        return redirect('login')
    
    book_request = get_object_or_404(BookRequest, id=request_id)
    
    if book_request.book.quantity > 0:
        book_request.status = 'Approved'
        book_request.book.quantity -= 1  # Decrease the quantity
        book_request.book.is_borrowed = True if book_request.book.quantity == 0 else False
        book_request.book.save()
        book_request.save()

        due_date = timezone.now() + timedelta(weeks=2)
        BookIssuance.objects.create(
            book=book_request.book,
            issued_to=book_request.requested_by,
            due_date=due_date,
        )
        messages.success(request, f"{book_request.book.title} has been issued to {book_request.requested_by.username}.")
    else:
        messages.error(request, f"{book_request.book.title} is not available.")
    
    return redirect('librarian_dashboard')

@login_required
def reject_request(request, request_id):
    if request.user.role != 'Librarian':
        return redirect('login')
    book_request = get_object_or_404(BookRequest, id=request_id)
    book_request.status = 'Rejected'
    book_request.save()
    return redirect('librarian_dashboard')

@login_required
def return_book(request, issuance_id):
    issuance = get_object_or_404(BookIssuance, id=issuance_id)
    
    if request.user.role == 'Customer' and issuance.issued_to != request.user:
        messages.error(request, "You are not authorized to return this book.")
        return redirect('customer_dashboard')
    
    # Calculate fine
    fine = issuance.calculate_fine()
    if fine > 0:
        messages.success(request, f"{issuance.book.title} has been returned successfully. Fine: ₹{fine}")
    else:
        messages.success(request, f"{issuance.book.title} has been returned successfully.")
    
    issuance.return_book()
    
    # Increase the book quantity
    issuance.book.quantity += 1
    issuance.book.is_borrowed = False if issuance.book.quantity > 0 else True
    issuance.book.save()
    
    if request.user.role == 'Customer':
        return redirect('customer_dashboard')
    elif request.user.role == 'Librarian':
        return redirect('librarian_dashboard')
       
@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('customer_dashboard')

@login_required
def staff_dashboard(request):
    tasks = Task.objects.filter(staff=request.user)
    return render(request, 'staff_dashboard.html', {'tasks': tasks})

@login_required
def mark_task_done(request, task_id):
    task = get_object_or_404(Task, id=task_id, staff=request.user)
    
    if task.status == 'Not Done':
        task.mark_as_done()
        messages.success(request, f"Task '{task.task_description}' marked as Done.")
    else:
        messages.info(request, "This task is already marked as Done.")

    return redirect('staff_dashboard')

