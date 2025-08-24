from django.contrib import admin
from .models import Reporter, NewsItem, AboutPage, Comment, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'is_reporter', 'last_activity')
    list_filter = ('status', 'is_reporter')
    search_fields = ('user__username',)
    actions = ['make_reporter', 'remove_reporter']
    
    def make_reporter(self, request, queryset):
        queryset.update(is_reporter=True)
    make_reporter.short_description = "Сделать репортёром"
    
    def remove_reporter(self, request, queryset):
        queryset.update(is_reporter=False)
    remove_reporter.short_description = "Убрать статус репортёра"

@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'hire_date')
    search_fields = ('user__username', 'specialization')

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'reporter', 'created_at', 'views')
    list_filter = ('reporter', 'created_at')
    search_fields = ('title', 'text')

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news_item', 'created_at')
    list_filter = ('user', 'news_item')
    search_fields = ('text', 'user__username')