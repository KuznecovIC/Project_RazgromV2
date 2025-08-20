from django import template

register = template.Library()

@register.filter(name='duration_format')
def duration_format(seconds):
    """
    Форматирует длительность в секундах в формат MM:SS.
    Пример: 125 -> "2:05"
    """
    if seconds is None:
        return "0:00"
    
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        return "0:00"
    
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    
    return f"{minutes}:{remaining_seconds:02d}"