from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.template import Template, Context
from django.template.response import TemplateResponse
import datetime
from django.utils import timezone
from .models import NewsPost, AboutPage, Reporter, User

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
    """
    Отображает главную страницу с новостями и информацией "О нас".
    """
    # Получаем последнюю страницу "О нас" из базы данных
    about_page = AboutPage.objects.first()
    
    # Получаем 3 самые свежие новости из базы данных
    news_posts = NewsPost.objects.all().order_by('-created_at')[:3]
    
    # Если новости не были созданы, используем жёстко закодированные данные
    if not news_posts:
        geo_reporter, _ = Reporter.objects.get_or_create(
            user__username='geo_reporter',
            defaults={
                'user': User.objects.create_user(username='geo_reporter', first_name='Иван', last_name='Петров'),
                'specialization': 'Геополитика',
                'bio': 'Опытный международный обозреватель'
            }
        )
        editor_reporter, _ = Reporter.objects.get_or_create(
            user__username='editor',
            defaults={
                'user': User.objects.create_user(username='editor', first_name='Редакция', last_name=''),
                'specialization': 'Главный редактор'
            }
        )
        spec_reporter, _ = Reporter.objects.get_or_create(
            user__username='spec_correspondent',
            defaults={
                'user': User.objects.create_user(username='spec_correspondent', first_name='Алексей', last_name='Смирнов'),
                'specialization': 'Специальный корреспондент'
            }
        )
        news_posts = [
            NewsPost(
                reporter=geo_reporter,
                title='Итоги Аляскинского саммита: Шаг к разрядке или новая глава?',
                text='Саммит на Аляске завершился. Лидеры обсудили вопросы климата, кибербезопасности и торговых отношений.',
                created_at=timezone.now() - datetime.timedelta(hours=6)
            ),
            NewsPost(
                reporter=editor_reporter,
                title='Саммит на Аляске: Первые заявления после встречи',
                text='По итогам встречи на Аляске стороны выступили с короткими, но ёмкими заявлениями.',
                created_at=timezone.now() - datetime.timedelta(hours=4)
            ),
            NewsPost(
                reporter=spec_reporter,
                title='Аляска: Кулуарные настроения саммита',
                text='Наш корреспондент сообщает о напряженной, но в то же время деловой атмосфере.',
                created_at=timezone.now() - datetime.timedelta(hours=2)
            ),
        ]
    
    context = {
        'about_page': about_page,
        'base_news': news_posts,
    }
    
    return render(request, 'landing.html', context)

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

def test_middleware(request):
    """Тестовая страница для проверки middleware"""
    return TemplateResponse(
        request,
        'test_template.html',
        {'test_value': 'Тестовое значение из view'}
    )

def debug_view(request):
    """Простая view для тестирования middleware"""
    return HttpResponse("""
    <html>
    <body>
        <h1>Тест Middleware</h1>
        <p>Это обычный HttpResponse для проверки работы middleware</p>
    </body>
    </html>
    """)


def force_middleware_test(request):
    """View, который точно работает с middleware"""
    response = TemplateResponse(request, 'test_template.html', {})
    # Явно указываем, что ответ не обработан
    response._is_rendered = False
    return response