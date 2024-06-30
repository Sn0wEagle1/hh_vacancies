from django.shortcuts import render

# Create your views here.
# jobs/views.py
# Пример views.py
from django.shortcuts import render
from .models import Job

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})



