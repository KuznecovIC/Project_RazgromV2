from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    class Meta:
        db_table = 'news_user'
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='news_user_set',
        related_query_name='news_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='news_user_set',
        related_query_name='news_user'
    )

class UserProfile(models.Model):
    STATUS_CHOICES = [
        ('online', 'В сети'),
        ('idle', 'Неактивен'),
        ('dnd', 'Не беспокоить'),
        ('offline', 'Не в сети'),
        ('invisible', 'Невидимый'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name="Аватар",
        blank=True,
        null=True
    )
    bio = models.TextField(verbose_name="Биография", blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='online',
        verbose_name="Статус"
    )
    custom_status = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Пользовательский статус"
    )
    is_reporter = models.BooleanField(
        default=False,
        verbose_name="Репортёр"
    )
    last_activity = models.DateTimeField(
        auto_now=True,
        verbose_name="Последняя активность"
    )
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
    
    def __str__(self):
        return f"Профиль {self.user.username}"
    
    def get_display_status(self):
        """Возвращает отображаемый статус с учетом невидимости"""
        if self.status == 'invisible':
            return 'offline'
        return self.status
    
    def is_online(self):
        """Проверяет, онлайн ли пользователь"""
        if self.status in ['offline', 'invisible']:
            return False
        return timezone.now() - self.last_activity < timezone.timedelta(minutes=5)

class Reporter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reporter_profile')
    bio = models.TextField(verbose_name="Биография", blank=True)
    profile_picture = models.ImageField(
        upload_to='reporters/profile_pics/',
        verbose_name="Фото профиля",
        blank=True,
        null=True
    )
    hire_date = models.DateField(verbose_name="Дата найма", auto_now_add=True)
    specialization = models.CharField(
        max_length=100,
        verbose_name="Специализация",
        blank=True
    )
    
    class Meta:
        verbose_name = "Репортер"
        verbose_name_plural = "Репортеры"
        ordering = ['-hire_date']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

class NewsItem(models.Model):
    views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    reporter = models.ForeignKey(
        'Reporter',
        on_delete=models.SET_NULL,
        verbose_name="Автор",
        null=True,
        blank=True,
        related_name='news_posts'
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст новости")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    image = models.ImageField(
        upload_to='news/images/',
        verbose_name="Изображение",
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = "Новостной пост"
        verbose_name_plural = "Новостные посты"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news_item = models.ForeignKey('NewsItem', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    audio_file = models.FileField(upload_to='voice_messages/', blank=True, null=True)
    is_voice_message = models.BooleanField(default=False)
    audio_duration = models.IntegerField(blank=True, null=True, help_text="Длительность аудио в секундах")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий от {self.user.username} к новости "{self.news_item.title[:30]}..."'

class AboutPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    team_photo = models.ImageField(upload_to='about/', verbose_name="Фото команды", blank=True)
    stats = models.JSONField(verbose_name="Статистика", default=dict, blank=True)
    
    class Meta:
        verbose_name = "Страница 'О нас'"
        verbose_name_plural = "Страницы 'О нас'"

    def __str__(self):
        return self.title