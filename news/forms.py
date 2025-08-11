from django import forms
from django.contrib.auth.models import User

# Форма для регистрации нового пользователя
class RegistrationForm(forms.ModelForm):
    # Добавляем поля для пароля, так как они не входят в стандартную модель User
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }
    
    # Добавляем валидацию, чтобы убедиться, что пароли совпадают
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

# Форма для входа в систему
class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)