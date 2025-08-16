from django.core.signals import request_finished
from django.dispatch import receiver
from django.template.response import TemplateResponse

@receiver(request_finished)
def debug_middleware(sender, **kwargs):
    if hasattr(sender, 'context_data'):
        print(f"\nSIGNAL DEBUG: Context keys - {list(sender.context_data.keys())}")