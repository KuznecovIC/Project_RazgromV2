from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import Reporter, User, NewsItem, AboutPage, Comment
import datetime


class BaseNewsMiddleware(MiddlewareMixin):

    def process_template_response(self, request, response):
        if hasattr(response, 'context_data'):
            self.create_about_page()
            self.create_news_posts_with_comments()
            
            response.context_data['about_page'] = AboutPage.objects.first()
            
            # Используем NewsItem, как указано в импорте
            base_news = NewsItem.objects.all().order_by('-created_at')[:3]
            response.context_data['base_news'] = base_news
            
            # Добавляем комментарии для каждой новости
            for news_item in base_news:
                comments = news_item.comments.all().order_by('-created_at')[:3]
                news_item.latest_comments = comments
                news_item.comment_count = news_item.comments.count()

        return response
    
    def create_about_page(self):
        about_data = {
            'title': "О нашем новостном ресурсе",
            'description': """ 
            <p>Мы - команда профессиональных журналистов, работающих 24/7,  
            чтобы предоставлять вам самые свежие и достоверные новости.</p> 
            """,
            'stats': {
                'years': 14,
                'readers': '2M+',
                'reporters': 42,
                'awards': 5
            }
        }
        
        AboutPage.objects.update_or_create(
            id=1,
            defaults=about_data
        )

    def create_news_posts_with_comments(self):
        # Создаем или получаем тестовых пользователей
        user1, _ = User.objects.get_or_create(
            username='user1',
            defaults={
                'first_name': 'Алексей',
                'last_name': 'Иванов'
            }
        )
        user2, _ = User.objects.get_or_create(
            username='user2',
            defaults={
                'first_name': 'Елена',
                'last_name': 'Смирнова'
            }
        )
        user3, _ = User.objects.get_or_create(
            username='user3',
            defaults={
                'first_name': 'Никита',
                'last_name': 'Козлов'
            }
        )
        
        # Создаем или получаем тестовых репортеров
        geo_reporter, _ = Reporter.objects.get_or_create(
            user__username='geo_reporter',
            defaults={
                'user': User.objects.create_user(
                    username='geo_reporter',
                    first_name='Иван',
                    last_name='Петров'
                ),
                'specialization': 'Геополитика',
                'bio': 'Опытный международный обозреватель'
            }
        )
        
        editor_reporter, _ = Reporter.objects.get_or_create(
            user__username='editor',
            defaults={
                'user': User.objects.create_user(
                    username='editor',
                    first_name='Редакция',
                    last_name=''
                ),
                'specialization': 'Главный редактор'
            }
        )
        
        spec_reporter, _ = Reporter.objects.get_or_create(
            user__username='spec_correspondent',
            defaults={
                'user': User.objects.create_user(
                    username='spec_correspondent',
                    first_name='Алексей',
                    last_name='Смирнов'
                ),
                'specialization': 'Специальный корреспондент'
            }
        )

        # Базовые новости
        base_news_data = [
            {
                'reporter': geo_reporter,
                'title': 'Итоги Аляскинского саммита: Шаг к разрядке или новая глава?',
                'text': 'Саммит на Аляске завершился. Лидеры обсудили вопросы климата, кибербезопасности и торговых отношений.',
                'created_at': timezone.now() - datetime.timedelta(hours=2)
            },
            {
                'reporter': editor_reporter,
                'title': 'Саммит на Аляске: Первые заявления после встречи',
                'text': 'По итогам встречи на Аляске стороны выступили с короткими, но ёмкими заявлениями.',
                'created_at': timezone.now() - datetime.timedelta(hours=4)
            },
            {
                'reporter': spec_reporter,
                'title': 'Аляска: Кулуарные настроения саммита',
                'text': 'Наш корреспондент сообщает о напряженной, но в то же время деловой атмосфере.',
                'created_at': timezone.now() - datetime.timedelta(hours=6)
            },
        ]
        
        # Создаем или обновляем новости и добавляем комментарии
        for news_item_data in base_news_data:
            # Используем NewsItem
            post, created = NewsItem.objects.update_or_create(
                title=news_item_data['title'],
                defaults=news_item_data
            )
            
            if created:
                # Создаем несколько тестовых комментариев для новой новости
                Comment.objects.create(
                    post=post,
                    user=user1,
                    text="Отличная статья! Спасибо за аналитику."
                )
                Comment.objects.create(
                    post=post,
                    user=user2,
                    text="Интересные подробности, жду продолжения."
                )
                Comment.objects.create(
                    post=post,
                    user=user3,
                    text="Всегда читаю ваши репортажи, очень информативно."
                )