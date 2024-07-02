from django import forms

class JobFilterForm(forms.Form):
    keywords = forms.CharField(label='Ключевые слова', required=False)
    salary_min = forms.IntegerField(label='Зарплата от (в тысячах рублей)', required=False)
    metro = forms.CharField(label='Метро', required=False)
    experience = forms.IntegerField(required=False, label='Опыт (лет)')
    remote = forms.BooleanField(label='Удаленная работа', required=False)

