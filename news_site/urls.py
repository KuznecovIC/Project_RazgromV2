# Файл: project_name/urls.py (корневой)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Эта строка обрабатывает главный URL (http://127.0.0.1:8000/)
    # и включает в себя все URL-адреса из news/urls.py.
    path('', include('news.urls')),
    
    # Это URL-адрес для админ-панели Django.
    path('admin/', admin.site.urls),
]

# Добавляем маршруты для медиафайлов только в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)