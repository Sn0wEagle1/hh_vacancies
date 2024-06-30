# jobs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),   # URL для списка вакансий
]
