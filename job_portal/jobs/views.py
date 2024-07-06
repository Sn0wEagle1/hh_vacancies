from .models import Job
from .forms import JobFilterForm, UserRegisterForm, UserLoginForm, SortForm
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import SavedJob
from django.contrib import messages

USD_TO_RUB = 88
EUR_TO_RUB = 94

def job_list(request):
    form = JobFilterForm(request.GET)
    jobs = Job.objects.all()


    if form.is_valid():
        if form.cleaned_data['salary_min']:
            salary_min = form.cleaned_data['salary_min']
            salary_filtered_jobs = Job.objects.none()

            for job in jobs:
                salary = job.salary.replace(' ', '').replace(' ', '')  # Удаление пробелов и неразрывных пробелов
                valid_salary = False

                # Определение валюты
                if '$' in salary:
                    currency_rate = USD_TO_RUB
                elif '€' in salary:
                    currency_rate = EUR_TO_RUB
                else:
                    currency_rate = 1  # Если валюта рубли или не указана

                # Извлечение диапазонов и чисел зарплат
                salary_ranges = re.findall(r'(\d+[-\d+]*)', salary)

                for salary_range in salary_ranges:
                    # Разделение диапазонов зарплат, если они есть, и преобразование в числа
                    salaries = list(map(int, re.findall(r'\d+', salary_range)))

                    if len(salaries) == 2:
                        # Конвертация зарплат в рубли
                        salaries = [s * currency_rate for s in salaries]
                        # Проверка, попадает ли минимальная зарплата в диапазон
                        if salaries[1] >= salary_min:
                            valid_salary = True
                    elif len(salaries) == 1:
                        # Конвертация зарплаты в рубли
                        salaries[0] = salaries[0] * currency_rate
                        # Проверка, превышает ли зарплата минимальное значение
                        if salaries[0] >= salary_min:
                            valid_salary = True

                if valid_salary:
                    salary_filtered_jobs |= Job.objects.filter(id=job.id)

            jobs = salary_filtered_jobs

        if form.cleaned_data['keywords']:
            keywords = form.cleaned_data['keywords']
            jobs = jobs.filter(title__icontains=keywords) | jobs.filter(skills__icontains=keywords)

        if form.cleaned_data['metro']:
            metro = form.cleaned_data['metro'].lower()
            filtered_jobs = []
            for job in jobs:
                if 'метро' in job.address.lower():
                    address_parts = job.address.lower().split('метро')
                    for part in address_parts[1:]:
                        if metro in part.strip():
                            filtered_jobs.append(job)
                            break
            jobs = filtered_jobs

        if form.cleaned_data['remote']:
            jobs = jobs.filter(remote__icontains='Можно удалённо')

        if form.cleaned_data['experience'] is not None:
            experience = form.cleaned_data['experience']
            filtered_jobs = []
            for job in jobs:
                job_experience = job.experience.lower()

                # Проверяем вакансии "без опыта"
                if 'без опыта' in job_experience and experience == 0:
                    filtered_jobs.append(job)
                # Проверяем вакансии с "более" n лет опыта
                elif 'более' in job_experience:
                    job_exp_years = int(re.search(r'\d+', job_experience).group())
                    if experience > job_exp_years:
                        filtered_jobs.append(job)
                # Проверяем вакансии с диапазоном опыта (n-m лет)
                elif 'лет' in job_experience:
                    job_exp_years = [int(x) for x in re.findall(r'\d+', job_experience)]
                    if len(job_exp_years) == 2:
                        if job_exp_years[0] <= experience or experience > job_exp_years[1]:
                            filtered_jobs.append(job)
                    elif len(job_exp_years) == 1:
                        if experience == job_exp_years[0]:
                            filtered_jobs.append(job)
                # Проверяем вакансии с точным количеством лет опыта
                else:
                    job_exp_years = [int(x) for x in re.findall(r'\d+', job_experience)]
                    if len(job_exp_years) == 1 and experience == job_exp_years[0]:
                        filtered_jobs.append(job)

            # Добавляем все вакансии, где опыт не требуется (вне зависимости от указанного опыта)
            filtered_jobs.extend([job for job in jobs if 'без опыта' in job.experience.lower()])

            jobs = filtered_jobs

        if form.cleaned_data['city']:
            city = form.cleaned_data['city'].lower()
            filtered_jobs = [job for job in jobs if job.address.lower().startswith(city)]
            jobs = filtered_jobs

        sort_by = form.cleaned_data['sort_by']
        if sort_by == 'asc':
            jobs = sorted(jobs, key=lambda job: get_salary_value(job, sort_by), reverse=False)
        elif sort_by == 'desc':
            jobs = sorted(jobs, key=lambda job: get_salary_value(job, sort_by), reverse=True)

    return render(request, 'job_list.html', {'form': form, 'jobs': jobs})

def get_salary_value(job, sort_by):
    salary = job.salary.replace(' ', '').replace(' ', '')  # Удаление пробелов и неразрывных пробелов

    # Определение валюты
    if '$' in salary:
        currency_rate = USD_TO_RUB
    elif '€' in salary:
        currency_rate = EUR_TO_RUB
    else:
        currency_rate = 1  # Если валюта рубли или не указана

    # Извлечение диапазонов и чисел зарплат
    salary_ranges = re.findall(r'(\d+[-\d+]*)', salary)

    max_salary_value = 0

    for salary_range in salary_ranges:
        # Разделение диапазонов зарплат, если они есть, и преобразование в числа
        salaries = list(map(int, re.findall(r'\d+', salary_range)))

        if len(salaries) == 2:
            # Конвертация зарплат в рубли
            salaries = [s * currency_rate for s in salaries]
            max_salary_value = max(max_salary_value, max(salaries))
        elif len(salaries) == 1:
            # Конвертация зарплаты в рубли
            salary_value = salaries[0] * currency_rate
            max_salary_value = max(max_salary_value, salary_value)

    if max_salary_value == 0 and sort_by == 'asc':
        max_salary_value = float('inf')
    elif max_salary_value == 0 and sort_by == 'desc':
        max_salary_value = -float('inf')

    return max_salary_value

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    saved_jobs = SavedJob.objects.filter(user=request.user)
    sort_form = SortForm(request.GET)
    sort_by = None

    if sort_form.is_valid():
        sort_by = sort_form.cleaned_data['sort_by']

        # Сортировка сохраненных вакансий по зарплате
        if sort_by == 'desc':
            saved_jobs = sorted(saved_jobs, key=lambda job: get_salary_value(job, 'desc'), reverse=True)
        elif sort_by == 'asc':
            saved_jobs = sorted(saved_jobs, key=lambda job: get_salary_value(job, 'asc'), reverse=False)

    return render(request, 'profile.html', {'saved_jobs': saved_jobs, 'sort_form': sort_form, 'sort_by': sort_by})

def get_salary_value(job, sort_by):
    salary = job.salary.replace(' ', '').replace(' ', '')  # Удаление пробелов и неразрывных пробелов

    # Определение валюты
    if '$' in salary:
        currency_rate = USD_TO_RUB
    elif '€' in salary:
        currency_rate = EUR_TO_RUB
    else:
        currency_rate = 1  # Если валюта рубли или не указана

    # Извлечение диапазонов и чисел зарплат
    salary_ranges = re.findall(r'(\d+[-\d+]*)', salary)

    max_salary_value = 0

    for salary_range in salary_ranges:
        # Разделение диапазонов зарплат, если они есть, и преобразование в числа
        salaries = list(map(int, re.findall(r'\d+', salary_range)))

        if len(salaries) == 2:
            # Конвертация зарплат в рубли
            salaries = [s * currency_rate for s in salaries]
            max_salary_value = max(max_salary_value, max(salaries))
        elif len(salaries) == 1:
            # Конвертация зарплаты в рубли
            salary_value = salaries[0] * currency_rate
            max_salary_value = max(max_salary_value, salary_value)

    if max_salary_value == 0 and sort_by == 'asc':
        max_salary_value = float('inf')
    elif max_salary_value == 0 and sort_by == 'desc':
        max_salary_value = -float('inf')

    return max_salary_value

@login_required
def save_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    SavedJob.objects.create(
        user=request.user,
        title=job.title,
        link=job.link,
        company=job.company,
        salary=job.salary,
        skills=job.skills,
        address=job.address,
        experience=job.experience,
        remote=job.remote
    )
    messages.success(request, f'Вакансия "{job.title}" добавлена в сохраненные!')
    return redirect(request.META.get('HTTP_REFERER', 'jobs:list'))

@login_required
def delete_saved_job(request, job_id):
    saved_job = get_object_or_404(SavedJob, id=job_id, user=request.user)
    saved_job.delete()
    messages.success(request, f'Вакансия "{saved_job.title}" удалена из сохраненных!')
    return redirect('profile')

