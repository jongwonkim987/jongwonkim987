from django.contrib import admin
from todo.models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_completed', 'start_date', 'end_date')
    list_filter = ('is_completed',)
    search_fields = ('title',)
    ordering = ('start_date',)
    fieldsets = [
        ('Todo Info', {
            'fields': ['title', 'description', 'is_completed'],
        }),
        ('Date Range', {
            'fields': ['start_date', 'end_date'],
        }),
    ]