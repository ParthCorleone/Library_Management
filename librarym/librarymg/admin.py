from django.contrib import admin
from .models import CustomUser, Book, WorkSchedule, Task, BookIssuance, BookRequest
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_borrowed')
    list_filter = ('is_borrowed',)
    search_fields = ('title', 'author')

class BookIssuanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'issued_to', 'issued_date', 'returned_date')
    list_filter = ('issued_date', 'returned_date')
    search_fields = ('book__title', 'issued_to__username')

class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('book', 'requested_by', 'request_date', 'status')
    list_filter = ('status', 'request_date')
    search_fields = ('book__title', 'requested_by__username')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(WorkSchedule)
admin.site.register(Task)
admin.site.register(BookIssuance, BookIssuanceAdmin)
admin.site.register(BookRequest, BookRequestAdmin)