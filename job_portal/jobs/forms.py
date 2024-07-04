from django import forms

class JobFilterForm(forms.Form):
    keywords = forms.CharField(label='Ключевые слова', required=False)
    salary_min = forms.IntegerField(label='Зарплата от (в рублях)', required=False)
    city = forms.CharField(label='Город', required=False)
    metro = forms.CharField(label='Метро', required=False)
    experience = forms.IntegerField(required=False, label='Опыт (лет)')
    remote = forms.BooleanField(label='Удаленная работа', required=False)

    SORT_CHOICES = [
        ('', 'Без сортировки'),
        ('asc', 'По возрастанию зарплаты'),
        ('desc', 'По убыванию зарплаты')
    ]
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Сортировка по')