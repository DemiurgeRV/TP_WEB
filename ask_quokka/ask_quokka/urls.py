from app import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('tag/<str:tag_name>', views.tag, name='tag')
]