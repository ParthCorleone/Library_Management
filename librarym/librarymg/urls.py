from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('librarian_dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('add_book/', views.add_book, name='add_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('request_book/<int:book_id>',views.request_book, name='request_book'),
    path('approve_request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('return_book/<int:issuance_id>/', views.return_book, name='return_book'),
    path('send_overdue_notification/<int:issuance_id>/', views.send_overdue_notification, name='send_overdue_notification'),
    path('mark_notification_read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('assign_task/', views.assign_task, name='assign_task'),
    path('view_task/',views.view_task,name='view_task'),
    path('mark_task_done/<int:task_id>/',views.mark_task_done, name='mark_task_done'),
]