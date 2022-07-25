from django import urls
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.project_list, name='list'),
    path('add', views.ProjectCreateView.as_view(), name='add'),
    path('<slug:project_slug>', views.project_detail, name='detail'),
]
