from django.contrib import admin
from task_management.models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    """Admin View for :model:`task_management.Task`."""

    list_display = ('id', 'title', 'description', 'status')
    list_filter = ('status', )

    search_fields = ('title', )


admin.site.register(Task, TaskAdmin)

