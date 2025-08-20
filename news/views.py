# news/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import login, logout
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse
import datetime
from django.utils import timezone
from .models import NewsItem, AboutPage, Reporter, Comment
from django.contrib.auth.decorators import login_required
import json
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

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
    about_page = AboutPage.objects.first()
    news_items = NewsItem.objects.all().order_by('-created_at')
    
    # Если новости не были созданы, используем жёстко закодированные данные
    if not news_items:
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
        news_items = [
            NewsItem(
                reporter=geo_reporter,
                title='Итоги Аляскинского саммита: Шаг к разрядке или новая глава?',
                text='Саммит на Аляске завершился. Лидеры обсудили вопросы климата, кибербезопасности и торговых отношений.',
                created_at=timezone.now() - datetime.timedelta(hours=6)
            ),
            NewsItem(
                reporter=editor_reporter,
                title='Саммит на Аляске: Первые заявления после встречи',
                text='По итогам встречи на Аляске стороны выступили с короткими, но ёмкими заявлениями.',
                created_at=timezone.now() - datetime.timedelta(hours=4)
            ),
            NewsItem(
                reporter=spec_reporter,
                title='Аляска: Кулуарные настроения саммита',
                text='Наш корреспондент сообщает о напряженной, но в то же время деловой атмосфере.',
                created_at=timezone.now() - datetime.timedelta(hours=2)
            ),
        ]

    # Добавляем комментарии для отображения на главной странице
    for item in news_items:
        item.latest_comments = item.comments.all().order_by('-created_at')[:3]
        item.comment_count = item.comments.count()
    
    context = {
        'about_page': about_page,
        'base_news': news_items,
    }
    
    return render(request, 'landing.html', context)

@login_required
def news_comments(request, news_id):
    """
    Displays the news comments page and handles form submission.
    """
    news_item = get_object_or_404(NewsItem, id=news_id)
    comments = news_item.comments.all()

    context = {
        'news_item': news_item,
        'comments': comments,
    }
    return render(request, 'news/news_comments.html', context)


@login_required
@require_POST
def add_comment(request, news_id):
    """
    Handles the creation of a new comment for a news article.
    """
    news_item = get_object_or_404(NewsItem, pk=news_id)
    comment_text = request.POST.get('comment_text', '')
    
    try:
        comment_data = {
            'user': request.user,
            'news_item': news_item,
        }

        if 'image' in request.FILES and request.FILES['image']:
            comment_data['text'] = comment_text
            comment_data['image'] = request.FILES['image']
        
        elif 'audio' in request.FILES and request.FILES['audio']:
            comment_data['text'] = "Голосовое сообщение"
            comment_data['audio_file'] = request.FILES['audio']
            comment_data['is_voice_message'] = True
            
            # Получаем длительность голосового сообщения из формы
            voice_duration = request.POST.get('voice_duration', 0)
            try:
                comment_data['audio_duration'] = int(voice_duration)
            except (ValueError, TypeError):
                comment_data['audio_duration'] = 0

        elif comment_text:
            comment_data['text'] = comment_text
        
        # Сохраняем комментарий в базе данных
        new_comment = Comment.objects.create(**comment_data)

        # Рендерим HTML для нового комментария
        comment_html = render_to_string('news/comment_partial.html', {'comment': new_comment}, request=request)

        return JsonResponse({'status': 'success', 'message': 'Комментарий отправлен', 'comment_html': comment_html})
    
    except Exception as e:
        print(f"Ошибка при отправке комментария: {e}")
        return JsonResponse({'status': 'error', 'message': f'Ошибка при отправке комментария: {str(e)}'}, status=400)


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
            return redirect('news:landing')
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
            
            if not user.last_login:
                messages.info(request, 'Это ваш первый вход. Рекомендуем сменить пароль в настройках профиля.')
            else:
                messages.info(request, f'Последний раз вы заходили {user.last_login.strftime("%d.%m.%Y в %H:%M")}')
            return redirect('news:landing')
        else:
            messages.error(request, 'Ошибка входа. Проверьте правильность введенных данных.')
            
            if AuthUser.objects.filter(username=request.POST.get('username')).exists():
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
    
    return redirect('news:landing')

@csrf_exempt
def increment_views(request, news_id):
    if request.method == 'POST':
        news_item = get_object_or_404(NewsItem, id=news_id)
        news_item.views += 1
        news_item.save()
        return JsonResponse({'status': 'success', 'views': news_item.views})
    return JsonResponse({'status': 'error'}, status=400)