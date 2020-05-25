from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('', views.post_list, name='post_list'),
                  path('task1/', views.index, name='task_1'),
                  path('task2/', views.index_ren, name='task_2'),
                  path('post/<int:pk>/', views.post_detail, name='post_detail'),
                  path('arhive/<int:year>/<int:month>/', views.arhive_month, name='arhive_month'),
                  path('comment/new/', views.comment_new, name='comment_new'),
                  path('post/new/', views.post_new, name='post_new'),
                  path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
                  path('about_me/', views.about_me, name='about_me'),
                  path('contact/', views.contact, name='contact'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
