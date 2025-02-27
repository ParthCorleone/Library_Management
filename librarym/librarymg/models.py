from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timezone, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Customer', 'Customer'),
        ('Librarian', 'Librarian'),
        ('Staff', 'Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    is_borrowed = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)

    def is_available(self):
        return self.quantity > 0

class WorkSchedule(models.Model):
    librarian = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    schedule = models.TextField()

def get_default_admin():
    admin_user = get_user_model().objects.filter(role='Admin').first()
    return admin_user.id if admin_user else None

class Task(models.Model):
    STATUS_CHOICES = (
        ('Not Done','Not Done'),
        ('Done', 'Done'),
    )
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'Staff'})
    task_description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # Use default instead of auto_now_add
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        default=get_default_admin,
        null=True, blank=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Not Done')

    def mark_as_done(self):
        self.status = 'Done'
        self.save()

class BookIssuance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    issued_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()  # Add this field
    returned_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} issued to {self.issued_to.username}"

    def return_book(self):
        self.returned_date = timezone.now()
        self.book.is_borrowed = False
        self.book.save()
        self.save()

    def is_overdue(self):
        """Check if the book is overdue."""
        return timezone.now() > self.due_date

    def calculate_fine(self):
        """Calculate the fine if the book is returned late."""
        if self.returned_date and self.returned_date > self.due_date:
            overdue_days = (self.returned_date - self.due_date).days
            # Fine starts after 1 week (7 days)
            if overdue_days > 7:
                return (overdue_days - 7) * 1  # ₹1 per day after 1 week
        return 0

class BookRequest(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ), default='Pending')

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"