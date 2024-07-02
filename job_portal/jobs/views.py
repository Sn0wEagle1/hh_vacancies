from django.shortcuts import render
from .models import Job
from .forms import JobFilterForm
import re

def job_list(request):
    form = JobFilterForm(request.GET)
    jobs = Job.objects.all()

    if form.is_valid():
        if form.cleaned_data['salary_min']:
            salary_min = form.cleaned_data['salary_min']
            filtered_jobs = []
            for job in jobs:
                # Извлекаем все числа из строки зарплаты
                salary_numbers = re.findall(r'\d+', job.salary.replace(' ', ''))
                if salary_numbers:
                    # Преобразуем найденные числа в int и сравниваем с заданным минимумом
                    salary_values = [int(salary) for salary in salary_numbers]
                    if any(salary >= salary_min for salary in salary_values):
                        filtered_jobs.append(job)
            jobs = filtered_jobs

        if form.cleaned_data['keywords']:
            keywords = form.cleaned_data['keywords']
            jobs = jobs.filter(title__icontains=keywords) | jobs.filter(skills__icontains=keywords)

        if form.cleaned_data['metro']:
            metro = form.cleaned_data['metro']
            jobs = jobs.filter(metro__icontains=metro)

        if form.cleaned_data['remote']:
            jobs = jobs.filter(remote__icontains='Можно удалённо')

        if form.cleaned_data['experience']:
            experience = form.cleaned_data['experience']
            filtered_jobs = []
            for job in jobs:
                if 'более' in job.experience:
                    job_experience = int(re.search(r'\d+', job.experience).group())
                    if experience > job_experience:
                        filtered_jobs.append(job)
                elif 'лет' in job.experience:
                    job_experience = [int(x) for x in re.findall(r'\d+', job.experience)]
                    if len(job_experience) == 2:
                        if job_experience[0] <= experience <= job_experience[1]:
                            filtered_jobs.append(job)
                    elif len(job_experience) == 1:
                        if experience == job_experience[0]:
                            filtered_jobs.append(job)
                elif 'без опыта' in job.experience and experience == 0:
                    filtered_jobs.append(job)
            jobs = filtered_jobs

    return render(request, 'jobs/job_list.html', {'form': form, 'jobs': jobs})
