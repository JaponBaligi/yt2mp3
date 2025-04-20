from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('download/', views.download, name='download'),
    path('downloads/<str:filename>', views.serve_file, name='serve_file'),
] 