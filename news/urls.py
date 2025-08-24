from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    path('<int:news_id>/comments/', views.news_comments, name='news_comments'),
    path('<int:news_id>/add_comment/', views.add_comment, name='add_comment'),
    path('news/<int:news_id>/increment_views/', views.increment_views, name='increment_views'),

    path('profile/', views.profile_view, name='profile'),
    path('update_avatar/', views.update_avatar, name='update_avatar'),
    path('update_activity/', views.update_activity, name='update_activity'),
    path('update_status/', views.update_status, name='update_status'),
    path('get_user_status/', views.get_user_status, name='get_user_status'),
        
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