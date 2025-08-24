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
from .models import NewsItem, AboutPage, Reporter, Comment, UserProfile
from django.contrib.auth.decorators import login_required
import json
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .forms import EmailUserCreationForm, UserProfileForm

User = get_user_model()

def landing_page(request):
    about_page = AboutPage.objects.first()
    news_items = NewsItem.objects.all().order_by('-created_at')
    
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

    for item in news_items:
        item.latest_comments = item.comments.all().select_related('user__profile').order_by('-created_at')[:3]
        item.comment_count = item.comments.count()
    
    context = {
        'about_page': about_page,
        'base_news': news_items,
    }
    
    return render(request, 'landing.html', context)

@login_required
def news_comments(request, news_id):
    news_item = get_object_or_404(NewsItem, id=news_id)
    comments = news_item.comments.all().select_related('user__profile')

    context = {
        'news_item': news_item,
        'comments': comments,
    }
    return render(request, 'news/news_comments.html', context)

@login_required
@require_POST
def add_comment(request, news_id):
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
            
            voice_duration = request.POST.get('voice_duration', 0)
            try:
                comment_data['audio_duration'] = int(voice_duration)
            except (ValueError, TypeError):
                comment_data['audio_duration'] = 0

        elif comment_text:
            comment_data['text'] = comment_text
        
        new_comment = Comment.objects.create(**comment_data)
        comment_html = render_to_string('news/comment_partial.html', {'comment': new_comment}, request=request)

        return JsonResponse({'status': 'success', 'message': 'Комментарий отправлен', 'comment_html': comment_html})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Ошибка при отправке комментария: {str(e)}'}, status=400)

def register_user(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            
            UserProfile.objects.create(user=user)
            
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались! Добро пожаловать!')
            return redirect('news:landing')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = EmailUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('news:landing')
        else:
            messages.error(request, 'Ошибка входа. Проверьте правильность введенных данных.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def logout_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f'Вы успешно вышли из системы. До свидания, {username}!')
    return redirect('news:landing')

@csrf_exempt
def increment_views(request, news_id):
    if request.method == 'POST':
        news_item = get_object_or_404(NewsItem, id=news_id)
        news_item.views += 1
        news_item.save()
        return JsonResponse({'status': 'success', 'views': news_item.views})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('news:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form})

@login_required
@require_POST
@csrf_exempt
def update_avatar(request):
    try:
        if 'avatar' in request.FILES:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            if profile.avatar:
                profile.avatar.delete()
            
            profile.avatar = request.FILES['avatar']
            profile.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Аватар успешно обновлен',
                'avatar_url': profile.avatar.url
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Файл не выбран'
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Ошибка при загрузке аватара: {str(e)}'
        }, status=500)

@login_required
@require_POST
def update_activity(request):
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.last_activity = timezone.now()
        profile.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@require_POST
def update_status(request):
    status = request.POST.get('status')
    
    if status in dict(UserProfile.STATUS_CHOICES).keys():
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.status = status
        profile.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Статус обновлен'
        })
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@require_GET
def get_user_status(request):
    """Возвращает JSON с данными о статусе пользователя."""
    try:
        profile = request.user.profile
        return JsonResponse({
            'status': profile.status,
            'status_display': profile.get_status_display(),
            'custom_status': profile.custom_status,
        })
    except UserProfile.DoesNotExist:
        return JsonResponse({'status': 'offline', 'status_display': 'Не в сети'}, status=404)