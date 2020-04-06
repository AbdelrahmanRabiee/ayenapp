from django.urls import path

from rest_framework import routers

from users import viewsets

app_name = "users"
urlpatterns = [

]

user_router = routers.SimpleRouter()

user_router.register(r'user', viewsets.UserViewSet, base_name='user')
user_router.register(r'users', viewsets.UsersInfoViewSet, base_name='users')

user_router.register(r'files', viewsets.UsersFilesViewSet, base_name='files')