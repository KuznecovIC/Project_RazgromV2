from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import Reporter, User, NewsPost, AboutPage
import datetime

class BaseNewsMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if hasattr(response, 'context_data'):
            # Создаем или обновляем страницу "О нас"
            self.create_about_page()
            
            # Создаем или обновляем тестовые новости и репортеров
            self.create_news_posts()
            
            # Добавляем данные в контекст
            response.context_data['about_page'] = AboutPage.objects.first()
            response.context_data['base_news'] = NewsPost.objects.all().order_by('-created_at')[:3]
        
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
            id=1,  # Фиксированный ID для единственной страницы
            defaults=about_data
        )
    
    def create_news_posts(self):
        # Создаём или получаем тестовых репортёров
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
        
        # Создаём или обновляем новости
        for news_item in base_news_data:
            NewsPost.objects.update_or_create(
                title=news_item['title'],
                defaults={
                    'reporter': news_item['reporter'],
                    'text': news_item['text'],
                    'created_at': news_item['created_at']
                }
            )