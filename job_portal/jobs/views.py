from django.shortcuts import render
from .models import Job
from .forms import JobFilterForm
import re


def job_list(request):
    form = JobFilterForm(request.GET)
    jobs = Job.objects.all()  # Изначально получаем все вакансии

    if form.is_valid():
        if form.cleaned_data['salary_min']:
            salary_min = form.cleaned_data['salary_min']
            salary_filtered_jobs = Job.objects.none()  # Инициализируем пустой QuerySet
            for job in jobs:
                # Извлекаем все числа из строки зарплаты
                salary_numbers = re.findall(r'\d+', job.salary.replace(' ', ''))
                if salary_numbers:
                    # Преобразуем найденные числа в int и сравниваем с заданным минимумом
                    salary_values = [int(salary) for salary in salary_numbers]
                    if any(salary >= salary_min for salary in salary_values):
                        salary_filtered_jobs |= Job.objects.filter(id=job.id)
            jobs = salary_filtered_jobs

        if form.cleaned_data['keywords']:
            keywords = form.cleaned_data['keywords']
            jobs = jobs.filter(title__icontains=keywords) | jobs.filter(skills__icontains=keywords)

        if form.cleaned_data['metro']:
            metro = form.cleaned_data['metro']
            jobs = jobs.filter(metro__icontains=metro)

        if form.cleaned_data['remote']:
            jobs = jobs.filter(remote__icontains='Можно удалённо')

        if form.cleaned_data['experience'] is not None:
            experience = form.cleaned_data['experience']
            experience_filtered_jobs = Job.objects.none()  # Инициализируем пустой QuerySet
            for job in jobs:
                experience_text = job.experience.lower()
                experience_numbers = re.findall(r'\d+', experience_text)

                if experience == 0 and "без опыта" in experience_text:
                    experience_filtered_jobs |= Job.objects.filter(id=job.id)
                elif experience_numbers:
                    if "более" in experience_text:
                        if int(experience_numbers[0]) <= experience:
                            experience_filtered_jobs |= Job.objects.filter(id=job.id)
                    elif len(experience_numbers) == 2:
                        if int(experience_numbers[0]) <= experience <= int(experience_numbers[1]):
                            experience_filtered_jobs |= Job.objects.filter(id=job.id)
                    elif len(experience_numbers) == 1:
                        if int(experience_numbers[0]) == experience:
                            experience_filtered_jobs |= Job.objects.filter(id=job.id)
            jobs = experience_filtered_jobs

    return render(request, 'jobs/job_list.html', {'form': form, 'jobs': jobs})
