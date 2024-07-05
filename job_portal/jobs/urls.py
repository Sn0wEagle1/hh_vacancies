from django.urls import path
from .views import job_list
from . import views

urlpatterns = [
    path('', job_list, name='job_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('save_job/<int:job_id>/', views.save_job, name='save_job'),
    path('delete_saved_job/<int:job_id>/', views.delete_saved_job, name='delete_saved_job'),
]

