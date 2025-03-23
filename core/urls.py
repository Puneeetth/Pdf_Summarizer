# App URLs (core/urls.py)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('summary/<int:pk>/', views.summary_view, name='summary'),
    path('api/status/<int:pk>/', views.check_processing_status, name='check_status'),
]