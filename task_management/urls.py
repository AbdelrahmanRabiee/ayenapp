from django.urls import path

from rest_framework import routers

from task_management import viewsets

app_name = "task_management"
urlpatterns = [

]

task_router = routers.SimpleRouter()

task_router.register(r'tasks', viewsets.TasksViewSet, base_name='tasks')