from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib import messages


User = get_user_model()

# Кастомная форма регистрации с email
class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже используется")
        return email

def landing_page(request):
    # Приветственное сообщение для новых пользователей
    if request.GET.get('new_user') == 'true':
        messages.info(request, 'Добро пожаловать на наш сайт! Пожалуйста, войдите в свой аккаунт.')
    return render(request, 'landing.html')

def register_user(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались! Добро пожаловать!')
            messages.info(request, 'Пожалуйста, заполните ваш профиль для полного доступа к функциям сайта.')
            return redirect('landing')
        else:
            messages.error(request, 'Ошибка регистрации. Пожалуйста, исправьте следующие ошибки:')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        messages.info(request, 'Пожалуйста, заполните все поля для регистрации.')
        form = EmailUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            
            # Проверка последнего входа
            if not user.last_login:
                messages.info(request, 'Это ваш первый вход. Рекомендуем сменить пароль в настройках профиля.')
            else:
                messages.info(request, f'Последний раз вы заходили {user.last_login.strftime("%d.%m.%Y в %H:%M")}')
                
            return redirect('landing')
        else:
            messages.error(request, 'Ошибка входа. Проверьте правильность введенных данных.')
            
            # Дополнительные подсказки
            if User.objects.filter(username=request.POST.get('username')).exists():
                messages.info(request, 'Забыли пароль? Вы можете <a href="/password_reset/">восстановить его</a>.')
    else:
        messages.info(request, 'Пожалуйста, введите ваши учетные данные для входа.')
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def logout_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f'Вы успешно вышли из системы. До свидания, {username}!')
        messages.info(request, 'Вы можете снова войти в любое время.')
    else:
        messages.warning(request, 'Вы не были авторизованы.')
    
    return redirect('landing')