from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Job

def job_list(request):
    query = request.GET.get('q')
    if query:
        jobs = Job.objects.filter(title__icontains=query)
    else:
        jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})




