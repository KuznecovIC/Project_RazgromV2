from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Теперь мы используем только маршруты из приложения 'news'
    path('', include('news.urls')),
]