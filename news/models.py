from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        db_table = 'news_user'  # Уникальное имя таблицы в БД
    
    # Добавляем related_name для групп и разрешений
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

class Reporter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reporter')
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

class NewsPost(models.Model):
    reporter = models.ForeignKey(
        Reporter,
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