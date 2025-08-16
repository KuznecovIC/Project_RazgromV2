from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from .views import test_middleware, debug_view
from django.template import Template, Context
from django.http import HttpResponse
from django.urls import path
from .views import (
    landing_page, 
    register_user, 
    login_user, 
    logout_user,
    test_middleware,
    debug_view  # Убедитесь, что это добавлено
)

def middleware_test(request):
    t = Template("""
    <html><body>
        <h1>Middleware Test Page</h1>
        <p>News count: {{ base_news|length }}</p>
        {% for item in base_news %}
        <div style="border:1px solid #ccc; padding:10px; margin:10px;">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
        </div>
        {% endfor %}
    </body></html>
    """)
    return HttpResponse(t.render(Context({})))

urlpatterns = [
    # Основные URL приложения
    path('', views.landing_page, name='landing'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('test-middleware/', views.test_middleware, name='test_middleware'),
    path('debug-test/', debug_view),

    # URL для сброса пароля
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             form_class=CustomPasswordResetForm,
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             success_url=reverse_lazy('password_reset_done'),
             extra_email_context={'site_name': 'Ваш сайт'}  # Добавлено для письма
         ), 
         name='password_reset'),
    
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             form_class=CustomSetPasswordForm,
             template_name='registration/password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete'),  # Исправлено на reverse_lazy
             post_reset_login=True,  # Автоматический вход после смены пароля
             post_reset_login_backend='django.contrib.auth.backends.ModelBackend'
         ),
         name='password_reset_confirm'),
    
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]