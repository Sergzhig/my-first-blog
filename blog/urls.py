from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('task1/', views.index,name='task_1'),
    path('task2/', views.index_ren,name='task_2'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    #path('arhive/<int:year>/', views.arhive, name='arhive'),
    path('arhive/<int:year>/<int:month>/', views.arhive_month, name='arhive_month'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)