from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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

class SortForm(forms.Form):
    SORT_CHOICES = [
        ('', 'Без сортировки'),
        ('asc', 'По возрастанию зарплаты'),
        ('desc', 'По убыванию зарплаты')
    ]
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Сортировка по')

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].help_text = 'Только буквы, цифры и символы @/./+/-/_'
        self.fields['email'].label = 'Электронная почта'
        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].help_text = (
            '<ul>'
            '<li>Ваш пароль должен содержать не менее 8 символов.</li>'
            '<li>Ваш пароль не должен быть общеупотребительным.</li>'
            '<li>Ваш пароль не должен состоять только из чисел.</li>'
            '</ul>'
        )
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password2'].help_text = 'Введите пароль еще раз для подтверждения.'

class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': (
            "Пожалуйста, введите правильное имя пользователя и пароль. Оба поля могут быть чувствительны к регистру."
        ),
        'inactive': ("This account is inactive."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password'].label = 'Пароль'
