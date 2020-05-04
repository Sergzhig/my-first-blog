from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('task1/', views.index,name='task_1'),
    path('task2/', views.index_ren,name='task_2'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

]