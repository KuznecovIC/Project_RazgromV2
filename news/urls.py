# Файл: news/urls.py (внутри вашего приложения news)

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
# from .forms import CustomPasswordResetForm, CustomSetPasswordForm # Убедитесь, что эти формы существуют

app_name = 'news' # Пространство имен для приложения 'news'

urlpatterns = [
    # Основные URL приложения
    path('', views.landing_page, name='landing'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # URL для страницы комментариев
    path('<int:news_id>/comments/', views.news_comments, name='news_comments'),
    
    # URL для добавления комментария
    path('<int:news_id>/add_comment/', views.add_comment, name='add_comment'),

    path('news/<int:news_id>/increment_views/', views.increment_views, name='increment_views'),
    
    # URL для сброса пароля (здесь я оставил его как у вас, но важно убедиться, 
    # что CustomPasswordResetForm и CustomSetPasswordForm импортируются или что вы используете стандартные формы Django).
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             success_url=reverse_lazy('news:password_reset_done')
         ), 
         name='password_reset'),
    
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url=reverse_lazy('news:password_reset_complete')
         ),
         name='password_reset_confirm'),
    
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]