# news/admin.py

from django.contrib import admin
from .models import Reporter, NewsItem, AboutPage, Comment

# Регистрация модели Reporter
@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'hire_date')
    search_fields = ('user__username', 'specialization')

# Регистрация модели NewsItem
@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'reporter', 'created_at')
    list_filter = ('reporter', 'created_at')

# Регистрация модели AboutPage
@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'team_photo')
        }),
        ('Статистика', {
            'fields': ('stats',),
            'classes': ('collapse',)
        }),
    )

# Регистрация модели Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news_item', 'created_at')
    list_filter = ('user', 'news_item')
    search_fields = ('text', 'user__username')