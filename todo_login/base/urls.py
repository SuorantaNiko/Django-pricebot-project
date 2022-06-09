from unicodedata import name
from importlib.resources import path
from urllib import request
from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView



from . import views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/',TaskCreate.search_product, name="form"),
    #path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    
    #path('task-create/search_product/', TaskCreate.search_product, name="script"),
    
    
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),

]