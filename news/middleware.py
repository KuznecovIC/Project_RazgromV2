# news/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
import datetime

class BaseNewsMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if hasattr(response, 'context_data'):
            # Убедитесь, что этот список не пуст!
            base_news = [
                {
                    'reporter': 'Геополитический обозреватель',
                    'title': 'Итоги Аляскинского саммита: Шаг к разрядке или новая глава?',
                    'text': 'Саммит на Аляске завершился. Лидеры обсудили вопросы климата, кибербезопасности и торговых отношений. Несмотря на отсутствие прорывных соглашений, эксперты отмечают конструктивный тон переговоров.',
                    'created_at': timezone.now() - datetime.timedelta(hours=2)
                },
                {
                    'reporter': 'Редакция',
                    'title': 'Саммит на Аляске: Первые заявления после встречи',
                    'text': 'По итогам встречи на Аляске стороны выступили с короткими, но ёмкими заявлениями. Особое внимание уделялось вопросу сотрудничества в Арктике. Подробности ожидаются в течение дня.',
                    'created_at': timezone.now() - datetime.timedelta(hours=4)
                },
                {
                    'reporter': 'Специальный корреспондент',
                    'title': 'Аляска: Кулуарные настроения саммита',
                    'text': 'Наш корреспондент, работающий "в полях", сообщает о напряженной, но в то же время деловой атмосфере. За закрытыми дверями обсуждались санкционные вопросы и будущие инвестиции.',
                    'created_at': timezone.now() - datetime.timedelta(hours=6)
                },
            ]
            
            # Теперь, когда новости есть, сортируем их
            sorted_news = sorted(base_news, key=lambda x: x['created_at'], reverse=True)
            
            # И добавляем в контекст
            response.context_data['base_news'] = sorted_news
        
        return response