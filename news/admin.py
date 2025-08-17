from django.contrib import admin
from .models import Reporter, NewsPost, AboutPage

@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'hire_date')
    search_fields = ('user__username', 'specialization')

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'reporter', 'created_at')
    list_filter = ('reporter', 'created_at')

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