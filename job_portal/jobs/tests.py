from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from .models import Job, SavedJob
from django.contrib.auth.models import User

class JobListTestCase(TestCase):
    def setUp(self):
        # Create test jobs
        Job.objects.create(
            title='Software Engineer',
            company='TestCompany',
            salary='100000-150000 руб.',
            skills='Python, Django',
            address='Москва, метро Тверская',
            experience='3-5 лет',
            remote='Можно удалённо'
        )
        Job.objects.create(
            title='Data Scientist',
            company='DataCorp',
            salary='$3000-5000',
            skills='Python, Machine Learning',
            address='Санкт-Петербург, метро Площадь Восстания',
            experience='1-3 года',
            remote='Можно удалённо'
        )

        self.client = Client()

    def test_job_list_view(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_list.html')
        self.assertIn('form', response.context)
        self.assertIn('jobs', response.context)

    def test_job_filter_by_salary(self):
        response = self.client.get(reverse('job_list'), {'salary_min': 4000})
        self.assertEqual(response.status_code, 200)
        jobs = response.context['jobs']
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].title, 'Data Scientist')

    def test_job_filter_by_keywords(self):
        response = self.client.get(reverse('job_list'), {'keywords': 'Python'})
        self.assertEqual(response.status_code, 200)
        jobs = response.context['jobs']
        self.assertEqual(len(jobs), 2)

    def test_job_filter_by_city(self):
        response = self.client.get(reverse('job_list'), {'city': 'Москва'})
        self.assertEqual(response.status_code, 200)
        jobs = response.context['jobs']
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].title, 'Software Engineer')

class UserProfileTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

        # Create test job
        self.job = Job.objects.create(
            title='Frontend Developer',
            company='WebCorp',
            salary='2000-4000 €',
            skills='JavaScript, React',
            address='Казань, метро Кремлевская',
            experience='1-2 года',
            remote='Можно удалённо'
        )

    def test_save_job(self):
        response = self.client.post(reverse('save_job', args=[self.job.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SavedJob.objects.filter(user=self.user, job=self.job).exists())

    def test_delete_saved_job(self):
        saved_job = SavedJob.objects.create(user=self.user, job=self.job)
        response = self.client.post(reverse('delete_saved_job', args=[saved_job.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(SavedJob.objects.filter(user=self.user, job=self.job).exists())

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertIn('saved_jobs', response.context)

